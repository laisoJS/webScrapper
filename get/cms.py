import requests as req
from Wappalyzer import Wappalyzer, WebPage

from utils.files import write_json

from colorama import Fore

# Delete Wappalyzer warnings
import warnings
warnings.filterwarnings("ignore", message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning)

def wappalyzer_cms(domain: str, verbose: bool):
    datas: dict = {}
    try:
        wapp =  Wappalyzer.latest()
        
        page = WebPage.new_from_url(f"http://{domain}")
        results: dict[str, str] = wapp.analyze_with_versions_and_categories(page)        
        
        for tech, data in results.items():
            datas[tech] = {
                "category": data["categories"],
                "version": data["versions"]
            }

        write_json(datas, f"output/cms.json")
        if verbose:
            print(f"{Fore.GREEN}[V]: {len(datas)} CMS found on {domain}{Fore.RESET}")
        return datas

    except req.exceptions.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}[!] Error: {e}\n{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[!] Error: {e}\n{Fore.RESET}")


