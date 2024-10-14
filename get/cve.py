import nvdlib 

from os import getenv
from dotenv import load_dotenv
load_dotenv()

from utils.files import read_json, write_json

from colorama import Fore
from typing import Generator, Dict, List, Any

# Api key
api_key: str | None = getenv("NDV_API_KEY")

def get_cve(verbose: bool) -> None:
    cms: Dict[str, str] | None = read_json("output/cms.json")

    if not cms:
        print(f"{Fore.YELLOW}[!] Warn: Cannot read cms files ({cms}){Fore.RESET}")
        return

    cve_data: Dict[str, List[Dict[str, Any]]] = {}

    try:
        if not api_key:
            print(f"{Fore.RED}[!] Error: NVD API key not found in .env{Fore.RESET}")

        for tech, data in cms.items():
            rawVersion = data.get("version", [])
            version: str = "".join(rawVersion)

            cve_data[tech] = []

            # If a version is found search for cve with that version
            res: Generator = nvdlib.searchCVE_V2(key=api_key,keywordSearch=tech)

            if res:
                for cve in res:
                    cve_info: Dict = {
                        "id": str(cve.id),
                        "published": str(cve.published),
                        "lastModified": str(cve.lastModified),
                        "description": str(cve.descriptions[0].value),
                        "score": [
                            float(cve.score[1]) if cve.score[1] else 0.0,
                            str(cve.score[2] if cve.score[2] else "Not found")
                        ],
                        "url": str(cve.url)
                    }

                    cve_data[tech].append(cve_info)

            if verbose:
                print(f"{Fore.GREEN}[V]: CVE found for {tech} {f'v{version}' if version else '(No version found)'}{Fore.RESET}")

            cve_data[tech] = sorted(cve_data[tech], key=lambda x: x['score'][0], reverse=True)[:5]
        
        write_json(cve_data, "output/cve.json")

    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Fore.RESET}")

