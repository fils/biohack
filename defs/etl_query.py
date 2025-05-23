from io import StringIO
from pathlib import Path

import lancedb
import polars as pl
import requests
import logging

logger = logging.getLogger(__name__)

def query_mode(source, sink, query, table):
    """Handle query mode operations"""
    logger.info(f"Query mode: Processing data from {source} to {sink}")
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
    try:
        # df = pl.read_csv(StringIO(response.text))
        df = pl.read_csv(StringIO(response.text), truncate_ragged_lines=False)
    except pl.exceptions.ShapeError as e:
        logger.exception(
            "Failed to parse CSV response from SPARQL query due to ragged lines. "
            "The number of columns is inconsistent across rows. "
            f"Polars error: {e}"
        )
        # Re-raise the exception as per requirement
        raise
    except Exception as e:
        logger.exception(f"An unexpected error occurred while parsing CSV response: {e}")
        raise

    # logger.info(df)

    # # Create or get LanceDB table and write data
    logger.info(f"Saving LanceDB table: {table}")
    db = lancedb.connect("./stores/lancedb")
    tbl = db.create_table(table, data=df, mode="overwrite")
    logger.info(tbl)
