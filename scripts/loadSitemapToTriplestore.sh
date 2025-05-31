#!/bin/bash
set -e # Exit on error

# Check if jsonld command exists
if ! command -v jsonld &> /dev/null; then
    echo "Error: jsonld command not found. Please install it." >&2
    exit 1
fi

# Check if curl command exists
if ! command -v curl &> /dev/null; then
    echo "Error: curl command not found. Please install it." >&2
    exit 1
fi

# A script for loading JSON-LD from a sitemap into a triplestore
# Usage
# ./loadSitemapToTriplestore.sh ../output/jld-sitemap.xml  http://homelab.lan:7878/store

# Check if required parameters are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <sitemap_file> <triplestore_endpoint>" >&2
    echo "Example: $0 ../output/jld-sitemap.xml  http://homelab.lan:7878/store" >&2
    exit 1
fi

SITEMAP_FILE=$1
TRIPLESTORE_ENDPOINT=$2

# Check if the sitemap file exists
if [ ! -f "$SITEMAP_FILE" ]; then
    echo "Error: Sitemap file '$SITEMAP_FILE' not found." >&2
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
processed_count=0
failed_downloads=0
failed_formatting=0
failed_uploads=0

total_urls=$(echo "$URLS" | wc -l | xargs) # xargs to trim whitespace

echo "Found $total_urls URLs to process"

for url in $URLS; do
    count=$((count + 1))
    echo "-------------start-------------"
    echo "[$count/$total_urls] Processing: $url"
    
    # Download the content
    echo "Downloading content..."
    # Add timestamp to basename to avoid name clashes if sitemap has duplicate basenames
    TEMP_FILE="$TEMP_DIR/$(basename "$url")_$(date +%s%N)" 
    
    curl -s -L "$url" -o "$TEMP_FILE" # Added -L to follow redirects
    curl_download_exit_code=$?

    if [ $curl_download_exit_code -ne 0 ]; then
        echo "Error downloading content from $url (exit code: $curl_download_exit_code). Skipping." >&2
        echo "-------------done (failed download)--------------" >&2
        failed_downloads=$((failed_downloads + 1))
        continue
    fi
    
    if [ -s "$TEMP_FILE" ]; then
        echo "Processing and uploading to triplestore..."
        
        # Attempt to format the file with jsonld
        # Capture stdout and stderr separately for jsonld
        jsonld_output=$(cat "$TEMP_FILE" | jsonld format -q 2> /tmp/sitemap_jsonld_error.log)
        jsonld_exit_code=$?

        if [ $jsonld_exit_code -ne 0 ]; then
            echo "Error formatting content from $url with jsonld (exit code: $jsonld_exit_code). Skipping." >&2
            if [ -s /tmp/sitemap_jsonld_error.log ]; then
                cat /tmp/sitemap_jsonld_error.log >&2
            fi
            rm -f /tmp/sitemap_jsonld_error.log
            echo "-------------done (failed formatting)--------------" >&2
            failed_formatting=$((failed_formatting + 1))
            continue
        fi
        rm -f /tmp/sitemap_jsonld_error.log # Clean up error log if successful
        
        # Attempt to upload the formatted data
        # Capture stdout and stderr separately for curl
        curl_upload_output=$(echo "$jsonld_output" | curl -X POST -H 'Content-Type:text/x-nquads' --data-binary @- "$TRIPLESTORE_ENDPOINT" 2> /tmp/sitemap_curl_error.log)
        curl_upload_exit_code=$?

        if [ $curl_upload_exit_code -ne 0 ]; then
            echo "Error uploading content from $url to $TRIPLESTORE_ENDPOINT (exit code: $curl_upload_exit_code). Skipping." >&2
            if [ -s /tmp/sitemap_curl_error.log ]; then
                cat /tmp/sitemap_curl_error.log >&2
            fi
            rm -f /tmp/sitemap_curl_error.log
            echo "-------------done (failed upload)--------------" >&2
            failed_uploads=$((failed_uploads + 1))
            continue
        fi
        rm -f /tmp/sitemap_curl_error.log # Clean up error log if successful
        
        echo "Upload complete for $url."
        # Optionally print curl output for success
        # echo "Server response: $curl_upload_output"
        processed_count=$((processed_count + 1))
    else
        echo "Error: Failed to download content from $url (empty file received). Skipping." >&2
        echo "-------------done (empty download)--------------" >&2
        failed_downloads=$((failed_downloads + 1))
    fi
    
    echo "-------------done--------------"
done

# Clean up
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"
echo "All done!"
echo "Summary:"
echo "Total URLs found: $total_urls"
echo "Successfully processed and uploaded: $processed_count"
echo "Failed downloads: $failed_downloads"
echo "Failed formatting (jsonld): $failed_formatting"
echo "Failed uploads (curl): $failed_uploads"

# Exit with a non-zero code if any failures occurred for easier scripting
if [ $((failed_downloads + failed_formatting + failed_uploads)) -gt 0 ]; then
    exit 1
fi