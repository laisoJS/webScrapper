import asyncio
import aiohttp

from typing import List
from colorama import Fore

from utils.files import read_txt_file, write_txt_file

async def get_admin_page(url: str, dataPath: str, verbose: bool, maxConcurrency: int = 10 ) -> None:
    data: List[str] | None = read_txt_file(dataPath)

    if not data:
        return

    connector = aiohttp.TCPConnector(limit=maxConcurrency)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_page(session, url, page, verbose) for page in data]
        res = await asyncio.gather(*tasks)

    successful_pages = [page for page in res if page]
    if successful_pages:
        write_txt_file(successful_pages, "output/admin.txt")

    print(f"{Fore.BLUE}[i] Info: {len(successful_pages)} pages found for {url}{Fore.RESET}")


async def fetch_page(session: aiohttp.ClientSession, url: str, page: str, verbose: bool) -> str | None:
    try:
        async with session.get(f"http://{url}/{page}") as res:
            if res.status == 200:
                if verbose:
                    print(f"{Fore.GREEN}[V]: Page found: {page}{Fore.RESET}")
                return page
            else:
                if verbose:
                    print(f"{Fore.YELLOW}[!]: Page {page} not found [{res.status}] {Fore.RESET}")
                return None

    except asyncio.TimeoutError:
        if verbose:
            print(f"{Fore.RED}[X] Error: Timeout error for page {page}{Fore.RESET}")
    except aiohttp.ClientError as e:
        if verbose:
            print(f"{Fore.RED}[X] Error: {page} - {e}{Fore.RESET}")
        return None

