import argparse
import asyncio

from colorama import Fore

from get.robots import get_robots
from get.sitemap import get_sitemap
from get.adminPages import get_admin_page
from get.dns import dns_query

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="webSrapper",
        description="A simple automated multitool for scraping website."
    )

    parser.add_argument("domain", type=str, help="The domain name without the http(s) (e.g. google.com)")
    parser.add_argument("--admin", type=str, help="Wordlist for the admin pages")
    parser.add_argument("-c", "--concurrency", type=int, help="Set the max concurrency")
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help="Add verbose to the output")

    args = parser.parse_args()
    domain:str = args.domain
    adminList: str = args.admin
    maxConcurrency: int = args.concurrency
    verbose: bool = args.verbose
    
    get_robots(domain, verbose)
    get_sitemap(domain, verbose)

    if adminList:
        if maxConcurrency:
            asyncio.run(get_admin_page(domain, adminList, verbose, maxConcurrency))
        else: 
            asyncio.run(get_admin_page(domain, adminList, verbose))

    dns_query(domain, verbose)

if __name__ == "__main__":
    main()

