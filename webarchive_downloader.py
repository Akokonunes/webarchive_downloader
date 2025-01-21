import argparse
import requests
import time
from itertools import cycle

# Display ASCII Art Banner
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

# Download URLs
def download_urls(domain, output_file, proxies=None, retries=3, timeout=20):
    """Download all URLs and parameters for a given domain from web.archive.org."""
    url = "https://web.archive.org/cdx/search/cdx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "url": f"*.{domain}/*",
        "collapse": "urlkey",
        "output": "text",
        "fl": "original"
    }

    proxy_cycle = cycle(proxies) if proxies else None

    for attempt in range(retries):
        try:
            proxy = {"http": next(proxy_cycle), "https": next(proxy_cycle)} if proxy_cycle else None
            response = requests.get(url, headers=headers, params=params, timeout=timeout, proxies=proxy)
            response.raise_for_status()

            # Write results to output file
            with open(output_file, "a") as f:
                for line in response.text.splitlines():
                    f.write(f"{line}\\n")

            print(f"[+] Successfully downloaded URLs for domain: {domain}")
            return  # Exit the function if successful

        except requests.RequestException as e:
            print(f"[-] Attempt {attempt + 1} failed for domain: {domain}. Error: {e}")
            if attempt < retries - 1:  # Wait before retrying, if attempts remain
                time.sleep(2)
            else:
                print(f"[-] Giving up on domain: {domain} after {retries} attempts.")

# Main Function
def main():
    display_banner()
    parser = argparse.ArgumentParser(description="Download all URLs and parameters from web.archive.org for domains.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing root domains, one per line.")
    parser.add_argument("-o", "--output", required=True, help="Output file to save all results.")
    parser.add_argument("-p", "--proxies", help="Optional: File containing proxy list (one per line).")

    args = parser.parse_args()
    input_file = args.file
    output_file = args.output
    proxy_file = args.proxies

    # Load proxies
    proxies = None
    if proxy_file:
        try:
            with open(proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            print(f"[+] Loaded {len(proxies)} proxies.")
        except FileNotFoundError:
            print(f"[-] Proxy file not found: {proxy_file}")
            return

    # Read domains from input file
    try:
        with open(input_file, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Input file not found: {input_file}")
        return

    # Process each domain with throttling
    for domain in domains:
        download_urls(domain, output_file, proxies)
        time.sleep(1)  # Throttle requests to avoid rate limiting

if __name__ == "__main__":
    main()
