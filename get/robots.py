from colorama import Fore
import requests as req

from utils.files import write_txt_file

def get_robots(url: str, verbose: bool) -> None:
    url = f"http://{url}/robots.txt"
    try:
        res = req.get(url)
        write_txt_file(res, "output/robots.txt")
        if verbose:
            print(f"{Fore.GREEN}[V]: Properly fetched robots.txt{Fore.RESET}")

    except req.exceptions.HTTPError:
        print(f"{Fore.RED}[!] Error: HTTP error{Fore.RESET}")
    except req.exceptions.Timeout:
        print(f"{Fore.RED}[!] Error: Timed out{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occured:\n{e}\n{Fore.RESET}")

