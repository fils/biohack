import yaml
import hashlib
import os
import lancedb
import pyarrow as pa
from defs.etl_convert import convert_document

def verify_sources():
    """
    Verify the data in the LanceDB table.

    This function:
    1. Connects to the LanceDB database
    2. Opens the 'sources' table
    3. Retrieves all records
    4. Prints a summary of the records
    5. Prints details of each record (filename, ID, location, markdown preview)

    Returns:
        None
    """
    print("\nVerifying data in LanceDB table...")

    # Initialize LanceDB
    db = lancedb.connect("./lancedb")

    if "sources" not in db.table_names():
        print("Sources table not found!")
        return

    # Open the table
    table = db.open_table("sources")

    # Get all records
    records = table.to_pandas()

    # Print summary
    print(f"Total records: {len(records)}")

    # Print details of each record
    for i, record in records.iterrows():
        print(f"\nRecord {i+1}:")
        print(f"  Filename: {record['filename']}")
        print(f"  ID: {record['id']}")
        print(f"  Location: {record['location']}")
        print(f"  Markdown length: {len(record['markdown'])} characters")
        # print(f"  Markdown preview: {record['markdown'][:100]}...")

def verify_claims():
    """
    Verify the data in the LanceDB table.

    This function:
    1. Connects to the LanceDB database
    2. Opens the 'sources' table
    3. Retrieves all records
    4. Prints a summary of the records
    5. Prints details of each record (filename, ID, location, markdown preview)

    Returns:
        None
    """
    print("\nVerifying data in LanceDB table...")

    # Initialize LanceDB
    db = lancedb.connect("./lancedb")

    if "sources" not in db.table_names():
        print("Sources table not found!")
        return

    # Open the table
    table = db.open_table("claims")

    # Get all records
    records = table.to_pandas()

    # Print summary
    print(f"Total records: {len(records)}")

    # Print details of each record
    for i, record in records.iterrows():
        print(f"\nRecord {i+1}:")
        print(f"  Filename: {record['filename']}")
        print(f"  node_name: {record['node_name']}")
        print(f"  index: {record['index']}")
        print(f"  text preview: {record['text'][:100]}...")


def verify_entities():
    """
    Verify the data in the LanceDB table.

    This function:
    1. Connects to the LanceDB database
    2. Opens the 'sources' table
    3. Retrieves all records
    4. Prints a summary of the records
    5. Prints details of each record (filename, ID, location, markdown preview)

    Returns:
        None
    """
    print("\nVerifying data in LanceDB table...")

    # Initialize LanceDB
    db = lancedb.connect("./lancedb")

    if "sources" not in db.table_names():
        print("Sources table not found!")
        return

    # Open the table
    table = db.open_table("entities")

    # Get all records
    records = table.to_pandas()

    # Print summary
    print(f"Total records: {len(records)}")

    # Print details of each record
    for i, record in records.iterrows():
        print(f"\nRecord {i+1}:")
        print(f"  start: {record['start']}")
        print(f"  end: {record['end']}")
        print(f"  text: {record['text']}")
        print(f"  label: {record['label']}")
        print(f"  score: {record['score']}")
        print(f"  filename: {record['filename']}")
        print(f"  nodename: {record['nodename']}")
        print(f"  index: {record['index']}")


def tables():
    db = lancedb.connect("./lancedb")

    tables = db.table_names()
    print(tables)

    for t in tables:
        print("----------------------------------------")
        print(t)
        entities_table = db.open_table("entities")
        print(entities_table.schema)


        # print(db.table(t).schema)

if __name__ == "__main__":
    tables()
    # verify_sources()
    # verify_claims()
    # verify_entities()
