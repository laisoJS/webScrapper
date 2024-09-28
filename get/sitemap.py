from colorama import Fore
import requests as req
import xml.etree.ElementTree as ET

from utils.files import write_txt_file

def get_sitemap(url: str, verbose: bool) -> None:
    sitemap_url: str = f"https://{url}/sitemap.xml"
    
    try:
        # Step 1: Fetch the sitemap XML
        res: req.Response = req.get(sitemap_url)
        res.raise_for_status()  # Raise exception for any HTTP errors
        content: str = res.text  # Get the response content as a string
        
        # Step 2: Parse the XML content
        try:
            root = ET.fromstring(content)  # Parse the XML content

            # Step 3: Extract URLs from the sitemap
            urls = []
            for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                url_text = url_elem.text
                if url_text:
                    urls.append(url_text)
                    if verbose:
                        print(f"{Fore.GREEN}[V]: Found URL: {url_text}{Fore.RESET}")

            # Step 4: Save extracted URLs to a file (optional step)
            write_txt_file(urls, "output/sitemap_urls.txt")
            
            if verbose:
                print(f"{Fore.GREEN}[V]: Successfully parsed and saved sitemap URLs{Fore.RESET}")

        except ET.ParseError:
            print(f"{Fore.RED}[!] Error: Failed to parse XML content{Fore.RESET}")
    
    except req.exceptions.HTTPError as http_err:
        print(f"{Fore.RED}[!] Error: HTTP error occurred ({http_err}){Fore.RESET}")
    except req.exceptions.Timeout:
        print(f"{Fore.RED}[!] Error: Timed out{Fore.RESET}")
    except req.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occurred:\n{e}\n{Fore.RESET}")
