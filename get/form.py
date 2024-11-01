import os

from bs4 import BeautifulSoup
from typing import List, Dict, Any

from utils.files import write_json

from colorama import Fore


def extract_form(html: str, verbose: bool) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    forms = []

    for form in soup.find_all("form"):
        if verbose:
            print(f"{Fore.GREEN}[V]: Form found{Fore.RESET}")

        form_details: Dict[str, str] = {
            "action": form.get("action"),
            "method": form.get("method", "get").lower(),
            "inputs": []
        }

        for input_tag in form.find_all("input"):
            input_type = input_tag.get("type", "text")
            input_name = input_tag.get("name")
            input_value = input_tag.get("value", "")

            form_details["inputs"].append({
                "type": input_type,
                "name": input_name,
                "value": input_value
            })

        for textarea in form.find_all("textarea"):
            form_details["inputs"].append({
                "type": "textarea",
                "name": textarea.get("name"),
                "value": textarea.text
            })

        for select in form.find_all("select"):
            options = [option.get("value", option.text) for option in select.find_all("option")]
            form_details["inputs"].append({
                "type": "select",
                "name": select.get("name"),
                "options": options
            })

        forms.append(form_details)

    return forms


def analyze_forms_in_html(domain: str, verbose: bool) -> None:
    forms_data = {}

    try:
        if not os.path.exists("output/html"):
            print(f"{Fore.YELLOW}[!] Warn: output/html not found.{Fore.RESET}")
            return

        for file_name in os.listdir("output/html"):
            file_path = os.path.join("output/html", file_name)

            file_name = f"{domain}{file_name}".replace("_", "/").rstrip(".html")

            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                forms = extract_form(html_content, verbose)
                forms_data[file_name] = forms

        write_json(forms_data, "output/forms.json")
        if verbose:
            print(f"{Fore.GREEN}[V]: Forms data writed in output/forms.json{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.RED}[X] Error:{Fore.RESET}")
