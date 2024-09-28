import asyncio
import aiohttp

from utils.files import read_txt_file, write_txt_file
from typing import List
from colorama import Fore


async def get_subdomain(url: str, wordlist: str, verbose: bool, maxConcurrency: int = 10) -> None:
    data: List[str] | None = read_txt_file(wordlist)

    if not data:
        return

    connector = aiohttp.TCPConnector(limit=maxConcurrency)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_subs(session, url, sub, verbose) for sub in data]
        results = await asyncio.gather(*tasks)

    successful_subs: List[str] = [f"http://{sub}.{url}" for sub in results if sub]
    if successful_subs:
        # Save successful subdomains
        write_txt_file(successful_subs, "output/subdomains.txt")

    print(f"{Fore.BLUE}[i] Info: {len(successful_subs)} subdomain found for {url}{Fore.RESET}")


async def fetch_subs(session: aiohttp.ClientSession, url: str, sub: str, verbose: bool) -> str | None:
    subdomain_http = f"http://{sub}.{url}"
    subdomain_https = f"https://{sub}.{url}"

    # Try both HTTP and HTTPS
    for protocol, subdomain in zip(["HTTP", "HTTPS"], [subdomain_http, subdomain_https]):
        try:
            async with session.get(subdomain) as res:
                if res.status == 200:
                    if verbose:
                        print(f"{Fore.GREEN}[V]: {protocol} Subdomain found: {subdomain}{Fore.RESET}")
                    return subdomain  # Return the full URL (either http or https)
                else:
                    if verbose:
                        print(f"{Fore.RED}[X]: {protocol} Subdomain ({subdomain}) not found [{res.status}] {Fore.RESET}")
        except asyncio.TimeoutError:
            if verbose:
                print(f"{Fore.RED}[X] Error: Timeout error for {protocol} subdomain {subdomain}{Fore.RESET}")
        except aiohttp.ClientError as e:
            if verbose:
                print(f"{Fore.RED}[X] Error: {protocol} subdomain {subdomain} - {e}{Fore.RESET}")

    return None  # No successful response from either protocol

