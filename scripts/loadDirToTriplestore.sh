#!/bin/bash
# A wrapper script for loading RDF from a directory into a triplestore
# Usage
# ./jsonldDirLoader.sh ./jsonld/depth_strict http://nas.lan:49153/blazegraph/namespace/kb/sparql

mc_cmd() {
    find $1 -type f  # kinda basic, might add a filter to it
}

# If you use this for ntriples, be sure to compute and/or add in a graph in the URL target
for i in $(mc_cmd $1); do
    echo "-------------start-------------"
    echo Next: $i
    cat $i | jsonld format -q | curl -X POST -H 'Content-Type:text/x-nquads' --data-binary  @- $2
    echo "-------------done--------------"
done

