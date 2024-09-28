import os
import argparse
import asyncio

from get.robots import get_robots
from get.sitemap import get_sitemap
from get.adminPages import get_admin_page
from get.subdomains import get_subdomain
from get.dns import dns_query

from colorama import Fore

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="webSrapper",
        description="A simple automated multitool for scraping website."
    )

    parser.add_argument("domain", type=str, help="The domain name without the http(s) (e.g. google.com)")
    
    parser.add_argument("-a", "--admin", type=str, help="Wordlist for the admin pages")
    parser.add_argument("-s", "--subs", type=str, help="Wordlist for subdomain enumeration")

    parser.add_argument("-c", "--concurrency", type=int, help="Set the max concurrency for the async function")
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help="Add verbose to the output")

    args = parser.parse_args()
    domain:str = args.domain

    adminList: str = args.admin
    subdomainList: str = args.subs

    maxConcurrency: int = args.concurrency
    verbose: bool = args.verbose

    if not os.path.exists("output/"):
        os.makedirs("output")

    print(f"{Fore.BLUE}[i] Info: Gathering robots.txt{Fore.RESET}")
    get_robots(domain, verbose)

    print(f"{Fore.BLUE}[i] Info: Gathering sitemap.xml{Fore.RESET}")
    get_sitemap(domain, verbose)

    if adminList:
        print(f"{Fore.BLUE}[i] Info: Gathering admin pages{Fore.RESET}")
        if maxConcurrency:
            asyncio.run(get_admin_page(domain, adminList, verbose, maxConcurrency))
        else: 
            asyncio.run(get_admin_page(domain, adminList, verbose))

    print(f"{Fore.BLUE}[i] Info: Querying DNS{Fore.RESET}")
    dns_query(domain, verbose)

    if subdomainList:
        print(f"{Fore.BLUE}[i] Info: Searching for subdomains{Fore.RESET}")
        if maxConcurrency:
            asyncio.run(get_subdomain(domain, subdomainList, verbose, maxConcurrency))
        else:
            asyncio.run(get_subdomain(domain, subdomainList, verbose))

if __name__ == "__main__":
    main()

