import ssl
import socket

from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec

from utils.files import write_json, write_byte

from colorama import Fore


def get_public_key_info(cert_bytes, verbose: bool):
    # Load the certificate from bytes
    cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
    
    # Extract the public key
    public_key = cert.public_key()
    
    # Determine the algorithm and key length
    key_info = {}
    
    if isinstance(public_key, rsa.RSAPublicKey):
        key_info['algorithm'] = 'RSA'
        key_info['key_length'] = public_key.key_size
    elif isinstance(public_key, dsa.DSAPublicKey):
        key_info['algorithm'] = 'DSA'
        key_info['key_length'] = public_key.key_size
    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        key_info['algorithm'] = 'ECDSA'
        key_info['key_length'] = public_key.key_size
    else:
        key_info['algorithm'] = 'Unknown'
        key_info['key_length'] = None
    
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    write_byte(pem, "output/cert_key.pem")
    if verbose:
        print(f"{Fore.GREEN}[V]: Certificat public key saved in output/cert_key.pem{Fore.RESET}")

    return key_info

def check_ssl_cert(domain: str, verbose: bool) -> None:
    ssl_info = {}

    try:
        context = ssl.create_default_context()  # Create a socket connection

        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Fetch the SSL certificate
                cert = ssock.getpeercert(True)  # Get the certificate in DER format

                # Validate Certificate
                cert_dict = ssock.getpeercert()  # Get the certificate in dict format for details
                cert_not_before = datetime.strptime(cert_dict['notBefore'], '%b %d %H:%M:%S %Y GMT')
                cert_not_after = datetime.strptime(cert_dict['notAfter'], '%b %d %H:%M:%S %Y GMT')
                current_time = datetime.now()

                ssl_info['domain'] = domain
                ssl_info['issuer'] = cert_dict['issuer']
                ssl_info['valid_from'] = cert_not_before.isoformat()
                ssl_info['valid_until'] = cert_not_after.isoformat()

                if current_time < cert_not_before:
                    ssl_info['status'] = 'Not Valid Yet'
                elif current_time > cert_not_after:
                    ssl_info['status'] = 'Expired'
                else:
                    ssl_info['status'] = 'Valid'

                # Get public key info
                public_key_info = get_public_key_info(cert, verbose)
                ssl_info['public_key'] = public_key_info

                # Analyze Cipher Suite
                cipher = ssock.cipher()
                ssl_info['cipher'] = cipher[0]

                write_json(ssl_info, "output/cert.json")
                if verbose:
                    print(f"{Fore.GREEN}[+] SSL Certificate for {domain} retrieved and saved successfully.{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error checking SSL/TLS for {domain}: \n{e}\n{Fore.RESET}")
