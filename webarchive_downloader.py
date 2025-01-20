import argparse
import requests

def display_banner():
    print("""
 /$$$$$$$            /$$                             /$$              
| $$__  $$          | $$                            | $$              
| $$  \ $$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$ 
| $$$$$$$/ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$|_  $$_/   /$$__  $$
| $$__  $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/  | $$    | $$  \ $$
| $$  \ $$| $$  | $$| $$  | $$| $$_____/| $$        | $$ /$$| $$  | $$
| $$  | $$|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$        |  $$$$/|  $$$$$$/
|__/  |__/ \______/ |_______/  \_______/|__/         \___/   \______/ 
                                                                      
                                                                      
    """)

def download_urls(domain, output_file):
    """Download all URLs and parameters for a given domain from web.archive.org."""
    url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"*.{domain}/*",
        "collapse": "urlkey",
        "output": "text",
        "fl": "original"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Write results to output file
        with open(output_file, "a") as f:
            for line in response.text.splitlines():
                f.write(f"{line}\n")

        print(f"[+] Successfully downloaded URLs for domain: {domain}")
    except requests.RequestException as e:
        print(f"[-] Failed to download URLs for domain: {domain}. Error: {e}")

def main():
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

    # Process each domain
    for domain in domains:
        download_urls(domain, output_file)

if __name__ == "__main__":
    main()
