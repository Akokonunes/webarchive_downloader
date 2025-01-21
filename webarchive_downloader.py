import argparse
import requests
import time
import socket
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure Cloudflare DNS
def set_cloudflare_dns():
    def custom_dns_resolver(hostname, port, family=socket.AF_INET):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('1.1.1.1', 443))]
    socket.getaddrinfo = custom_dns_resolver

# Display banner
def display_banner():
    print("""
 /$$$$$$$            /$$                             /$$              
| $$__  $$          | $$                            | $$              
| $$  \\ $$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$ 
| $$$$$$$/ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$|_  $$_/   /$$__  $$
| $$__  $$| $$  \\ $$| $$  \\ $$| $$$$$$$$| $$  \\__/  | $$    | $$  \\ $$
| $$  \\ $$| $$  | $$| $$  | $$| $$_____/| $$        | $$ /$$| $$  | $$
| $$  | $$|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$        |  $$$$/|  $$$$$$/
|__/  |__/ \\______/ |_______/  \\_______/|__/         \\___/   \\______/ 
                                                                      
                                                                      
    """)

# Function to download URLs
def download_urls(domain, output_file, retries=3, timeout=20):
    url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"*.{domain}/*",
        "collapse": "urlkey",
        "output": "text",
        "fl": "original"
    }

    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    try:
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()

        with open(output_file, "a") as f:
            for line in response.text.splitlines():
                f.write(f"{line}\\n")

        print(f"[+] Successfully downloaded URLs for domain: {domain}")
    except (requests.RequestException, urllib3.exceptions.RequestError) as e:
        print(f"[-] Failed to download URLs for domain: {domain}. Error: {e}")

# Main function
def main():
    set_cloudflare_dns()
    display_banner()

    parser = argparse.ArgumentParser(description="Download all URLs and parameters from web.archive.org for domains.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing root domains, one per line.")
    parser.add_argument("-o", "--output", required=True, help="Output file to save all results.")

    args = parser.parse_args()
    input_file = args.file
    output_file = args.output

    # Read domains from input file
    try:
        with open(input_file, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Input file not found: {input_file}")
        return

    # Process each domain with throttling
    for domain in domains:
        download_urls(domain, output_file)
        time.sleep(1)  # Throttle requests to avoid rate limiting

if __name__ == "__main__":
    main()
