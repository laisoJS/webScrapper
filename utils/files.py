import json

from colorama import Fore
from typing import List, Dict


"""
    WRITE FILES
"""
def write_txt_file(data: List[str], path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            for line in data:
                f.write(f"{line}\n");

    except FileExistsError:
        print(f"{Fore.RED}[!] Error: File already exist ({path}){Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Can't write to file {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: I/O error occured{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: A not recognize error occured:\n{e}\n{Fore.RESET}")

def write_raw_txt(data, path) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    except FileExistsError:
        print(f"{Fore.RED}[!] Error: File already exist ({path}){Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Can't write to file {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: I/O error occured{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: A not recognize error occured:\n{e}\n{Fore.RESET}")

def write_byte(data, path: str) -> None:
    try:
        with open(path, "wb") as f:
            f.write(data)

    except FileExistsError:
        print(f"{Fore.RED}[!] Error: File already exist ({path}){Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Can't write to file {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: I/O error occured{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: A not recognize error occured:\n{e}\n{Fore.RESET}")

def write_json(data: Dict[str, str], path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    except FileExistsError:
        print(f"{Fore.RED}[!] Error: File already exist ({path}){Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Can't write to file {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: I/O error occured{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: A not recognize error occured:\n{e}\n{Fore.RESET}")

        
"""
    READ FILES
"""

def read_txt_file(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        return lines

    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: File ({path}) not found{Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Don't have permission to read {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: Can't read {path}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: An unexpected error occurred:\n{e}\n{Fore.RESET}")

def read_json(path: str) -> Dict[str, str] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: File ({path}) not found{Fore.RESET}")
    except PermissionError:
        print(f"{Fore.RED}[!] Error: Can't write to file {path}{Fore.RESET}")
    except IOError:
        print(f"{Fore.RED}[!] Error: I/O error occured{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: A not recognize error occured:\n{e}\n{Fore.RESET}")

