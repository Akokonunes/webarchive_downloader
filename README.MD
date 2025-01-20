# Web Archive Downloader

A Python script to download all URLs and parameters from [web.archive.org](https://web.archive.org) for a list of root domains. This tool is useful for bug bounty hunting and security research.

## Features
- Download URLs and parameters for any domain archived on web.archive.org.
- Process multiple domains from a file.
- Save results to a specified output file.

## Prerequisites
- Python 3.x
- `requests` library (install with `pip install requests`)

## Usage

### Command Syntax
```bash
python3 webarchive_downloader.py -f <input_file> -o <output_file>
