import yaml
import hashlib
import os
import lancedb
import pyarrow as pa
import json
from typing import List
import pandas as pd

from defs.etl_convert import convert_document
from baml_client.sync_client import b
from baml_client.types import Idea
from baml_client.types import Assertion
from dataclasses import dataclass
from defs import etl_gliner  # Add import for etl_gliner function

@dataclass
class NodeEntry:
    filename: str
    node_name: str
    index: int
    text: str

def parse_json(jd, filename) -> List[NodeEntry]:

    # Read and parse the JSON file
    data = json.loads(jd)

    results = []

    # Iterate through each node (key) in the JSON
    for node_name, entries in data.items():
        # Skip if the value is not a list/array
        if not isinstance(entries, list):
            continue

        # Process each entry in the node's array
        for index, text in enumerate(entries):
            entry = NodeEntry(
                filename=filename,
                node_name=node_name,
                index=index,
                text=text
            )
            results.append(entry)

    return results

def generate_content_hash(content):
    """
    Generate a hash based on content.

    Args:
        content (str): The content to hash

    Returns:
        str: MD5 hash of the content as a hexadecimal string
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def process_sources():
    # Read the sourcelist.yaml file
    with open('stores/sourcelist.yaml', 'r') as file:
        sources = yaml.safe_load(file)

    # Initialize LanceDB
    db = lancedb.connect("./lancedb")

    # Create or get the sources table
    schema = pa.schema([
        pa.field("filename", pa.string()),
        pa.field("id", pa.string()),
        pa.field("location", pa.string()),
        pa.field("markdown", pa.string())
    ])

    # Always recreate the table to avoid duplicates
    if "sources" in db.table_names():
        db.drop_table("sources")

    table = db.create_table("sources", schema=schema)

    # Process each source
    for source_name, location in sources.items():
        print(f"Processing {source_name}: {location}")

        # Determine if it's a local file or URL
        is_local = location.startswith("file://")

        if is_local:
            # Remove the file:// prefix and convert to local path
            local_path = location[7:]  # Remove "file://" prefix
            markdown = convert_document(local_file=local_path)
            filename = os.path.basename(local_path)
        else:
            # It's a URL
            markdown = convert_document(url=location)
            filename = source_name  # Use the source name as filename for URLs

        if markdown:
            # Generate a content hash as ID
            content_id = generate_content_hash(markdown)

            # Store in LanceDB
            data = {
                "filename": filename,
                "id": content_id,
                "location": location,
                "markdown": markdown
            }

            # Add to table (using upsert to avoid duplicates)
            table.add([data])

            print(f"Successfully processed {source_name} with ID {content_id}")
        else:
            print(f"Failed to process {source_name}")

def workOnIdea(mdtext: str) -> Idea:
  response = b.ExtractIdea(mdtext)
  return response

def workOnAssertion(mdtext: str) -> Assertion:
  response = b.ExtractAssertion(mdtext)
  return response

def process_claims():
    db = lancedb.connect("./lancedb")

    if "sources" not in db.table_names():
        print("Sources table not found!")
        return

    # Define schema for the claims table based on NodeEntry class
    claims_schema = pa.schema([
        pa.field("filename", pa.string()),
        pa.field("node_name", pa.string()),
        pa.field("index", pa.int32()),
        pa.field("text", pa.string())
    ])

    # Create or recreate the claims table
    if "claims" in db.table_names():
        db.drop_table("claims")
    
    claims_table = db.create_table("claims", schema=claims_schema)
    
    # Process source data
    table = db.open_table("sources")
    records = table.to_pandas()
    print(f"Total records: {len(records)}")

    for i, record in records.iterrows():
        # Process assertions
        ra = workOnAssertion(record['markdown'])
        pra = parse_json(ra.model_dump_json(), record['filename'])
        
        # Process ideas
        ri = workOnIdea(record['markdown'])
        pri = parse_json(ri.model_dump_json(), record['filename'])
        
        # Combine both types of claims
        all_claims = []
        
        # Convert NodeEntry objects to dictionaries for LanceDB
        for entry in pra:
            all_claims.append({
                "filename": entry.filename,
                "node_name": entry.node_name,
                "index": entry.index,
                "text": entry.text
            })
            
        for entry in pri:
            all_claims.append({
                "filename": entry.filename,
                "node_name": entry.node_name,
                "index": entry.index,
                "text": entry.text
            })
        
        # Add the claims to the table if there are any
        if all_claims:
            claims_table.add(all_claims)
            print(f"Added {len(all_claims)} claims from {record['filename']}")

def process_entities():
    db = lancedb.connect("./lancedb")

    if "claims" not in db.table_names():
        print("Claims table not found!")
        return

    table = db.open_table("claims")
    records = table.to_pandas()
    print(f"Total records in claims: {len(records)}")

    all_entities_dfs = []  # Initialize a list to store individual DataFrames

    for i, record in records.iterrows():
        ent = etl_gliner.process(str(record['text']))
        df = pd.DataFrame(ent) # df contains columns from ent, e.g., 'entity_text', 'entity_type'
        
        if not df.empty: # Proceed only if etl_gliner found entities
            df['filename'] = record['filename']
            df['nodename'] = record['node_name'] # Corrected from node_name to nodename to match user's request
            df['index'] = record['index'] # Corrected from index to idex
            all_entities_dfs.append(df)
        # else:
        #     print(f"No entities found for text in {record['filename']}, node {record['node_name']}, index {record['index']}")


    if not all_entities_dfs:
        print("No entities processed. 'entities' table will not be created.")
        return

    # Concatenate all DataFrames into one
    final_df = pd.concat(all_entities_dfs, ignore_index=True)
    print(f"Total entities processed: {len(final_df)}")
    # print(final_df.head()) # Optional: print head of the final DataFrame
    # print(final_df.info()) # Optional: print info of the final DataFrame

    # Define schema for the new "entities" table
    # We need to know the columns and types from 'ent' (output of etl_gliner.process)
    # For now, let's assume 'ent' produces 'entity_text' (string) and 'entity_type' (string)
    # You MUST adjust this schema based on the actual columns and types in `df` from `etl_gliner.process`
    
    # Dynamically create schema from the final_df
    if not final_df.empty:
        pa_fields = []
        for column_name, dtype in final_df.dtypes.items():
            if pd.api.types.is_integer_dtype(dtype):
                pa_fields.append(pa.field(column_name, pa.int64())) # or pa.int32() if appropriate
            elif pd.api.types.is_float_dtype(dtype):
                pa_fields.append(pa.field(column_name, pa.float64()))
            elif pd.api.types.is_bool_dtype(dtype):
                pa_fields.append(pa.field(column_name, pa.bool_()))
            else: # Default to string for object types or other unhandled types
                pa_fields.append(pa.field(column_name, pa.string()))
        
        entities_schema = pa.schema(pa_fields)

        # Create or recreate the entities table
        if "entities" in db.table_names():
            db.drop_table("entities")
        
        entities_table = db.create_table("entities", schema=entities_schema)
        print(entities_table.schema)

        # Add data to the "entities" table
        entities_table.add(final_df)
        print(f"Successfully created 'entities' table and added {len(final_df)} records.")
    else:
        print("Final DataFrame is empty. 'entities' table not created.")


if __name__ == "__main__":
    # process_sources()
    # process_claims()
    process_entities()