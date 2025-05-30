import argparse
import regex
import os
from urllib.parse import urlparse

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True, help='File containing all URLs to clean')
parser.add_argument("--output", "-o", type=str, required=False, help='Output file path')
args = parser.parse_args()

# Initialize data structure to track seen URLs
alreadySeen = {}

# Regex patterns
globalUrlFootprint = regex.compile(r'(?<=(\?|\&).*=)(.*?)(?=(\&|$))')
parametersName = regex.compile(r'(?<=(\?|&))(.*?)(?==)')
doubleSlashes = regex.compile(r'(?<=[a-z0-9])(\/.*?\/.*?)(?=(\/|\?))')

# Output file handling
output_path = args.output if args.output else "cleaned-URLS.txt"
output = open(output_path, "w")

def getGlobalFootprint(url):
    return globalUrlFootprint.sub('', url)

def getParameterNames(url):
    match = parametersName.findall(url)
    return [elem[1] for elem in match]

def getBetweenTwoSlashes(url):
    contentBetweenTwoSlashes = doubleSlashes.search(url)
    return contentBetweenTwoSlashes.group() if contentBetweenTwoSlashes else None

def isDuplicate(url, alreadySeen):
    parsing = urlparse(url)
    completeHostname = parsing.netloc
    hostDirectory = alreadySeen.get(completeHostname)

    if hostDirectory:
        footprintSet = hostDirectory[0]
        globalFootprint = getGlobalFootprint(url)

        if globalFootprint in footprintSet:
            return True  # Heuristic 2

        footprintSet.add(globalFootprint)
        doubleSlashesContent = getBetweenTwoSlashes(url)
        paramNames = getParameterNames(url)

        twoSlashesContentDirectory = hostDirectory[1].get(doubleSlashesContent)
        if twoSlashesContentDirectory:
            if frozenset(paramNames) in twoSlashesContentDirectory:
                return True  # Heuristic 3
            else:
                twoSlashesContentDirectory.add(frozenset(paramNames))
                return False
        else:
            hostDirectory[1][doubleSlashesContent] = {frozenset(paramNames)}
            return False

    else:
        doubleSlashesContent = getBetweenTwoSlashes(url)
        if doubleSlashesContent:
            dictContent = {doubleSlashesContent: {frozenset(getParameterNames(url))}}
        else:
            dictContent = {}
        alreadySeen[completeHostname] = (set([getGlobalFootprint(url)]), dictContent)
        return False

def main():
    try:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as URLS:
            for url in URLS:
                url = url.strip()
                if not isDuplicate(url, alreadySeen):
                    print(url)
                    output.write(f"{url}\n")
    finally:
        output.close()

if __name__ == '__main__':
    main()
