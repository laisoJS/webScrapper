from typing import Tuple, Dict, Set
import dns.resolver

from utils.files import write_json

from colorama import Fore


def dns_query(domain: str, verbose: bool) -> None:
    resolver = dns.resolver.Resolver()    
    records: Tuple[str, ...] = ("A", "AAAA", "MX", "NS", "TXT", "SRV", "PTR", "AFSDB", "CAA", "CERT", "DHCID", "DNAME", "DNSKEY", "DS", "HINFO", "ISDN")

    success: Dict[str, Set[str]] = {record: set() for record in records}

    for record in records:
        try: 
            answer = resolver.resolve(domain, record)

            for data in answer:
                success[record].add(str(data))

                if verbose:
                    print(f"{Fore.GREEN}[+]: Record of type {record} found.{Fore.RESET}")

        except dns.resolver.NoAnswer:
            if verbose:
                print(f"{Fore.YELLOW}[!]: No record ({record}) found for {domain}.{Fore.RESET}")
        except dns.resolver.NXDOMAIN:
            print(f"{Fore.RED}[-]: Domain {domain} not found.{Fore.RESET}")
            break
        except dns.resolver.Timeout:
            print(f"{Fore.YELLOW}[!] Warn: DNS query for {domain} ({record}) timed out.{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: An unexpected error occured on record {record}:\n{e}\n{Fore.RESET}")

    # Convert sets to lists to make them JSON serializable
    success_serializable = {record: list(data) for record, data in success.items()}

    write_json(success_serializable, "output/DNS.json")

    if verbose:
        print(f"{Fore.BLUE}[i] Info: {len(success)} DNS records found for {domain}{Fore.RESET}")
