import os
import asyncio
import aiohttp

from bs4 import BeautifulSoup

from utils.files import write_json, read_txt_file

from typing import List
from colorama import Fore

crawlerPath = "output/links.txt"


async def get_forms(verbose: bool, maxConcurrency: int = 10) -> None:
    forms_data = {}

    if not os.path.exists(crawlerPath):
        print(f"{Fore.RED}[!] Error: Can't load {crawlerPath}{Fore.RESET}")
        return

    urls: List[str] = read_txt_file(crawlerPath)

    try:
        connector = aiohttp.TCPConnector(limit=maxConcurrency)
        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [fetch_pages(session, url, verbose) for url in urls if url ]
            results = await asyncio.gather(*tasks)
            
        for result in results:
            if result:
                forms_data[result['url']] = result['html']

        write_json(forms_data, "output/forms.json")
        if verbose:
            print(f"{Fore.GREEN}[V]: Found forms on {len(forms_data)} pages{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.RED}[X] Error: An unexpected error occured:\n{e}\n{Fore.RESET}")
    return


async def fetch_pages(session: aiohttp.ClientSession, url: str, verbose: bool) -> dict | None:
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                forms = soup.find_all("form")

                if forms:
                    form_html = ''.join(str(form) for form in forms)
                    form_list = []

                    for form in forms:
                        form_info = {
                            "action": form.get("action", ""),
                            "method": form.get("method", "GET"),
                            "inputs": [
                                {
                                    "name": input_tag.get("name"),
                                    "type": input_tag.get("type", "text")
                                } for input_tag in form.find_all("input")
                            ]
                        }

                        form_list.append(form_info)

                    if verbose:
                        print(f"{Fore.GREEN}[V]: {len(form_list)} forms found on {url}{Fore.RESET}")

                    return {
                        "url": url,
                        "html": form_html
                    }
            else:
                if verbose:
                    print(f"{Fore.YELLOW}[!] Warn: Failed to fetch {url} (Status: {response.status}){Fore.RESET}")
                return None

    except Exception as e:
        print(f"{Fore.RED}[X] Error fetching {url}:\n{e}{Fore.RESET}")
        return None

