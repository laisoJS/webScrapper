import asyncio
import aiohttp

from colorama import Fore

from utils.files import read_txt_file, write_txt_file

async def get_admin_page(url: str, dataPath: str, verbose: bool, maxConcurrency: int = 10 ) -> None:
    data: list[str] = read_txt_file(dataPath)

    connector = aiohttp.TCPConnector(limit=maxConcurrency)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_page(session, url, page, verbose) for page in data]
        res = await asyncio.gather(*tasks)

    successful_pages = [page for page in res if page]
    if successful_pages:
        write_txt_file(successful_pages, "output/admin.txt")


async def fetch_page(session: aiohttp.ClientSession, url: str, page: str, verbose: bool) -> str | None:
    try:
        async with session.get(f"http://{url}/{page}") as res:
            if res.status == 200:
                if verbose:
                    print(f"{Fore.GREEN}[V]: Page found: {page}{Fore.RESET}")
                return page
            else:
                if verbose:
                    print(f"{Fore.RED}[X]: Page {page} not found [{res.status}] {Fore.RESET}")
                return None

    except asyncio.TimeoutError:
        print(f"{Fore.RED}[X] Error: Timeout error for page {page}{Fore.RESET}")
    except aiohttp.ClientError as e:
        print(f"{Fore.RED}[X] Error: {page} - {e}{Fore.RESET}")
        return None

