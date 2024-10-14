import aiohttp
import asyncio

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

from utils.files import write_txt_file

from colorama import Fore
from typing import Set, List


def normalize_url(url: str) -> str:
    parse_url = urlparse(url)

    # Force the HTTP to avoid crawling http and https
    scheme = "http"

    # Strip the www to avoid crawling a page twice
    netloc = parse_url.netloc
    if netloc.startswith("www."):
        netloc = netloc[4:]

    # Ensure consistent path format (trailing slash if not a file)
    path = parse_url.path
    if not path.endswith("/") and ("." not in path.split("/")[-1]):
        path += "/"

    # Rebuild the parsed url
    normalize_url = urlunparse((scheme, netloc, path, "", "", ""))
    return normalize_url


async def crawl_website(domain: str, verbose: bool, maxConcurrency: int = 10) -> None:
    try:
        domain_url: str = f"http://{domain}/"
        visited_urls: Set[str] = set()

        pages_to_visit: List[str] = [domain_url]

        connector = aiohttp.TCPConnector(limit=maxConcurrency)
        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while pages_to_visit:
                url = pages_to_visit.pop(0)

                normalized_url = normalize_url(url)
                if normalized_url in visited_urls:
                    continue
                visited_urls.add(normalized_url)

                links = await crawl_pages(session, url, verbose)

                if not links:
                    continue

                for link in links:
                    normalized_link = normalize_url(link)
                    parse_link = urlparse(normalized_link)

                    if parse_link.netloc in (domain, domain.lstrip("www.")):
                        if normalized_link not in visited_urls and normalized_link not in pages_to_visit:
                            pages_to_visit.append(normalized_link)

                if verbose:
                    print(f"{Fore.GREEN}[V]: Crawled {url} {Fore.RESET}")

        urls: List[str] = [link for link in visited_urls]
        write_txt_file(urls, "output/links.txt")

    except Exception as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occured:\n{e}\n{Fore.RESET}")


async def crawl_pages(session: aiohttp.ClientSession, page: str, verbose: bool) -> List[str]:
    try:
        visited_pages: Set = set()
        async with session.get(page) as res:
            if res.status == 200:
                html = await res.text()
                soup = BeautifulSoup(html, "html.parser")
                
                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href and ("#" not in href):
                        if href.startswith(("http", "https")):
                            full_url = normalize_url(href)
                            visited_pages.add(full_url)
                        else:
                            full_url = normalize_url(urljoin(page, href))
                            visited_pages.add(full_url)

                links: List[str] = [link for link in visited_pages if not link.startswith(("mailto:", "tel:"))]
                return links

            elif verbose:
                print(f"{Fore.YELLOW}[!]: Page {page} not found [{res.status}] {Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occured:\n{e}\n{Fore.RESET}")


