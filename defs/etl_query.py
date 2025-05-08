from io import StringIO
from pathlib import Path

import lancedb
import polars as pl
import requests


def query_mode(source, sink, query, table):
    """Handle query mode operations"""
    print(f"Query mode: Processing data from {source} to {sink}")
    # Add query-specific logic here

    # Qlever params, not needed for oxigraph
    params = {
        "timeout": "600s",
        "access-token": "odis_7643543846_6dMISzlPrD7i"
    }
    headers = {
        "Accept": "text/csv",
        "Content-type": "application/sparql-query"
    }


    # Read the SPARQL query from file
    with open(query, "r") as file:
        query = file.read()

    # Send the request
    response = requests.post(source, params=params, headers=headers, data=query)

    # Load response into Polars DataFrame
    # df = pl.read_csv(StringIO(response.text))
    df = pl.read_csv(StringIO(response.text), truncate_ragged_lines=False)

    # print(df)

    # # Create or get LanceDB table and write data
    print("Saving LanceDB table: ", table, "")
    db = lancedb.connect("./stores/lancedb")
    tbl = db.create_table(table, data=df, mode="overwrite")
    print(tbl)
