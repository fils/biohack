import json
import os
from dataclasses import dataclass
from typing import List
import pandas as pd
from defs import etl_gliner  # Add import for etl_gliner function


@dataclass
class NodeEntry:
    filename: str
    node_name: str
    index: int
    text: str


def parse_json_file(file_path: str) -> List[NodeEntry]:
    """
    Parse a JSON file and extract structured information from it.

    Args:
        file_path: Path to the JSON file to parse

    Returns:
        List of NodeEntry objects containing the extracted information
    """
    # Get the filename from the path
    filename = os.path.basename(file_path)

    # Read and parse the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

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


# Example usage
if __name__ == "__main__":
    # Replace with your actual file path
    file_path = "./secret/idea_2409.09239v1.json"
    entries = parse_json_file(file_path)

    for entry in entries:
        print("-" * 80)
        print(f"Text: {entry.text}")
        results = etl_gliner.process(entry.text)
        df = pd.DataFrame(results)
        print(df)

    # Print the parsed entries
    # for entry in entries:
    #     print(f"File: {entry.filename}")
    #     print(f"Node: {entry.node_name}")
    #     print(f"Index: {entry.index}")
    #     print(f"Text: {entry.text}")
    #     print("-" * 80)