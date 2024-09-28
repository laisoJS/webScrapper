from colorama import Fore
import requests as req

from utils.files import write_txt_file

def get_sitemap(url: str, verbose: bool) -> None:
    url: str = f"https://{url}/sitemap.xml"
    try:
        res: req.Response = req.get(url)
        res.raise_for_status()
        write_txt_file(res, "output/sitemap.xml")
        if verbose:
            print(f"{Fore.GREEN}[V]: Properly fetched sitemap.xml{Fore.RESET}")

    except req.exceptions.HTTPError:
        print(f"{Fore.RED}[!] Error: HTTP error{Fore.RESET}")
    except req.exceptions.Timeout:
        print(f"{Fore.RED}[!] Error: Timed out{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occured:\n{e}\n{Fore.RESET}")

