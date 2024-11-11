import os
import argparse
import asyncio

from get.robots import get_robots
from get.sitemap import get_sitemap
from get.adminPages import get_admin_page
from get.subdomains import get_subdomain
from get.dns import dns_query
from get.cms import wappalyzer_cms
from get.form import analyze_forms_in_html
from get.crawler import crawl_website
from get.cve import get_cve
from get.ssl import check_ssl_cert
from get.security_header import check_security_header

from colorama import Fore


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="webSrapper",
        description="A simple automated multitool for scraping website.",
    )

    parser.add_argument("domain", type=str, help="The domain name without the http(s) (e.g. google.com)")

    parser.add_argument("-a", "--admin", type=str, help="Wordlist for the admin pages")
    parser.add_argument("-s", "--subs", type=str, help="Wordlist for subdomain enumeration")
    parser.add_argument("--ssl", action="store_true", default=False, help="Gather data from the ssl certificate")
    
    parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        default=10,
        help="Set the max concurrency for the async function",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Add verbose to the output",
    )

    args = parser.parse_args()
    domain: str = args.domain

    ssl: bool = args.ssl
    adminList: str = args.admin
    subdomainList: str = args.subs

    maxConcurrency: int = args.concurrency
    verbose: bool = args.verbose

    if not os.path.exists("output/"):
        os.makedirs("output")

    try:
        if not os.path.exists("output/robots.txt"):
            print(f"{Fore.BLUE}[i] Info: Gathering robots.txt{Fore.RESET}")
            get_robots(domain, verbose)

        if not os.path.exists("output/sitemap_urls.txt"):
            print(f"{Fore.BLUE}[i] Info: Gathering sitemap.xml{Fore.RESET}")
            get_sitemap(domain, verbose)

        if adminList and not os.path.exists("output/admin.txt"):
            print(f"{Fore.BLUE}[i] Info: Gathering admin pages{Fore.RESET}")
            asyncio.run(get_admin_page(domain, adminList, verbose, maxConcurrency))

        if not os.path.exists("output/DNS.json"):
            print(f"{Fore.BLUE}[i] Info: Querying DNS{Fore.RESET}")
            dns_query(domain, verbose)

        if not os.path.exists("output/links.txt"):
            print(f"{Fore.BLUE}[i] Info: Crawling website{Fore.RESET}")
            asyncio.run(crawl_website(domain, verbose, maxConcurrency))

        if subdomainList and not os.path.exists("output/subdomains.txt"):
            print(f"{Fore.BLUE}[i] Info: Searching for subdomains{Fore.RESET}")
            asyncio.run(get_subdomain(domain, subdomainList, verbose, maxConcurrency))

        if not os.path.exists("output/cms.json"):
            print(f"{Fore.BLUE}[i] Info: Scanning for CMS{Fore.RESET}")
            wappalyzer_cms(domain, verbose)

        if not os.path.exists("output/forms.json"):
            print(f"{Fore.BLUE}[i] Info: Crawling pages for forms{Fore.RESET}")
            analyze_forms_in_html(domain, verbose)

        if not os.path.exists("output/cve.json"):
            print(f"{Fore.BLUE}[i] Info: Searching for cve based on cms{Fore.RESET}")
            get_cve(verbose)

        if ssl and not os.path.exists("output/cert.json"):
            print(f"{Fore.BLUE}[i] Info: Checking the SSL cert{Fore.RESET}")
            check_ssl_cert(domain, verbose)

        if not os.path.exists("output/headers.json"):
            print(f"{Fore.BLUE}[i] Info: Searching for security headers{Fore.RESET}")
            asyncio.run(check_security_header(domain, maxConcurrency, verbose))

    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}[!] Keyboard interruption detected, quitting...{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: An error occured:\n{e}\n{Fore.RESET}")


if __name__ == "__main__":
    main()
