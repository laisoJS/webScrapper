import aiohttp
import asyncio

from utils.files import write_json

from colorama import Fore
from typing import Dict


async def check_security_header(domain: str, maxConcurrency: int, verbose: bool) -> None:
    headers_to_check: Dict[str, str] = {
        "Strict-Transport-Security": "Missing",
        "Content-Security-Policy": "Missing",
        "X-Content-Type-Options": "Missing",
        "X-Frame-Options": "Missing",
        "X-XSS-Protection": "Missing",
        "Referrer-Policy": "Missing",
    }

    url: str = f"http://{domain}"

    try:
        connector = aiohttp.TCPConnector(limit=maxConcurrency)
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.get(url) as res:
                headers = res.headers

                for header in headers_to_check:
                    if header in headers:
                        headers_to_check[header] = "Present"

                        if verbose:
                            print(f"{Fore.GREEN}[V]: Header {header} found.{Fore.RESET}")

                write_json(headers_to_check, "output/headers.json")

    except Exception as e:
        print(f"{Fore.RED}[X] Error: Coudn't fetch headers for {url}:\n{e}\n{Fore.RESET}")
