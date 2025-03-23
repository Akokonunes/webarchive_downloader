#!/bin/bash

# Prompt for the root domains file
read -p "Enter the root domains file name (e.g., root.txt): " domains_file

# Check if the file exists
if [[ ! -f "$domains_file" ]]; then
  echo "File '$domains_file' not found."
  exit 1
fi

# Prompt for the output file
read -p "Enter the output file name (e.g., out.txt): " output_file

# Optional: Clear the output file if it already exists
> "$output_file"

# Loop through each domain in the provided file
while IFS= read -r domain || [ -n "$domain" ]; do
  echo "Processing: $domain"
  curl -G "https://web.archive.org/cdx/search/cdx" \
       --data-urlencode "url=*.$domain/*" \
       --data-urlencode "collapse=urlkey" \
       --data-urlencode "output=text" \
       --data-urlencode "fl=original" >> "$output_file"
done < "$domains_file"

echo "All domains processed. Check '$output_file' for the results."
