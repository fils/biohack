#!/bin/bash
# A script for loading JSON-LD from a sitemap into a triplestore
# Usage
# ./loadSitemapToTriplestore.sh ../output/jld-sitemap.xml  http://homelab.lan:7878/store

# Check if required parameters are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <sitemap_file> <triplestore_endpoint>"
    echo "Example: $0 ../output/jld-sitemap.xml  http://homelab.lan:7878/store"
    exit 1
fi

SITEMAP_FILE=$1
TRIPLESTORE_ENDPOINT=$2

# Check if the sitemap file exists
if [ ! -f "$SITEMAP_FILE" ]; then
    echo "Error: Sitemap file '$SITEMAP_FILE' not found."
    exit 1
fi

# Create a temporary directory for downloaded files
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Extract URLs from the sitemap
echo "Extracting URLs from sitemap: $SITEMAP_FILE"
URLS=$(grep -o '<loc>.*</loc>' "$SITEMAP_FILE" | sed 's/<loc>\(.*\)<\/loc>/\1/')

# Process each URL
count=0
total=$(echo "$URLS" | wc -l)
echo "Found $total URLs to process"

for url in $URLS; do
    count=$((count + 1))
    echo "-------------start-------------"
    echo "[$count/$total] Processing: $url"
    
    # Download the content
    echo "Downloading content..."
    TEMP_FILE="$TEMP_DIR/$(basename "$url")"
    curl -s "$url" -o "$TEMP_FILE"
    
    if [ -s "$TEMP_FILE" ]; then
        # Process and upload to triplestore
        echo "Processing and uploading to triplestore..."
        cat "$TEMP_FILE" | jsonld format -q | curl -X POST -H 'Content-Type:text/x-nquads' --data-binary @- "$TRIPLESTORE_ENDPOINT"
        echo "Upload complete."
    else
        echo "Error: Failed to download content from $url"
    fi
    
    echo "-------------done--------------"
done

# Clean up
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"
echo "All done! Processed $count URLs."