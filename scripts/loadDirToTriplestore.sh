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

# A wrapper script for loading RDF from a directory into a triplestore
# Usage
# ./jsonldDirLoader.sh ./jsonld/depth_strict http://nas.lan:49153/blazegraph/namespace/kb/sparql

mc_cmd() {
    find "$1" -type f  # kinda basic, might add a filter to it
}

# If you use this for ntriples, be sure to compute and/or add in a graph in the URL target
for i in $(mc_cmd "$1"); do
    echo "-------------start-------------"
    echo "Processing: $i"
    
    # Attempt to format the file with jsonld
    # Capture stdout and stderr separately for jsonld
    jsonld_output=$(cat "$i" | jsonld format -q 2> /tmp/jsonld_error.log)
    jsonld_exit_code=$? 

    if [ $jsonld_exit_code -ne 0 ]; then
        echo "Error formatting $i with jsonld (exit code: $jsonld_exit_code). Skipping." >&2
        # Print jsonld error log if it exists
        if [ -s /tmp/jsonld_error.log ]; then
            cat /tmp/jsonld_error.log >&2
        fi
        rm -f /tmp/jsonld_error.log # Clean up error log
        echo "-------------done (failed formatting)--------------" >&2
        continue
    fi
    rm -f /tmp/jsonld_error.log # Clean up error log if successful
    
    # Attempt to upload the formatted data
    # Capture stdout and stderr separately for curl
    curl_output=$(echo "$jsonld_output" | curl -X POST -H 'Content-Type:text/x-nquads' --data-binary @- "$2" 2> /tmp/curl_error.log)
    curl_exit_code=$?

    if [ $curl_exit_code -ne 0 ]; then
        echo "Error uploading $i to $2 (exit code: $curl_exit_code). Skipping." >&2
        # Print curl error log if it exists
        if [ -s /tmp/curl_error.log ]; then
            cat /tmp/curl_error.log >&2
        fi
        rm -f /tmp/curl_error.log # Clean up error log
        echo "-------------done (failed upload)--------------" >&2
        continue
    fi
    rm -f /tmp/curl_error.log # Clean up error log if successful
    
    echo "Successfully processed and uploaded $i"
    # Optionally print curl output if needed for success confirmation
    # echo "Server response: $curl_output"
    echo "-------------done--------------"
done
