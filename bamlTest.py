from baml_client.sync_client import b
from baml_client.types import Idea
from baml_client.types import Assertion
from baml_client.types import Nanograph

import argparse
import json
import sys

def read_text_file(filepath):
  try:
    with open(filepath, 'r') as file:
      content = file.read()
    return content
  except FileNotFoundError:
    print(f"Error: File not found at '{filepath}'")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

def workOnIdea(mdtext: str) -> Idea:
  response = b.ExtractIdea(mdtext)
  return response

def workOnAssertion(mdtext: str) -> Assertion:
  response = b.ExtractAssertion(mdtext)
  return response

def workOnNanograph(mdtext: str) -> Nanograph:
  response = b.ExtractNanopubs(mdtext)
  return response

def main():
  # Set up command line argument parsing
  parser = argparse.ArgumentParser(description='Process markdown text and extract ideas or assertions.')
  parser.add_argument('--input', '-i', required=True, 
                     help='Input markdown file path')
  parser.add_argument('--output', '-o', required=True, 
                     help='Output file path for JSON results')
  parser.add_argument('--mode', '-m', choices=['idea', 'assertion', 'nanograph'], default='idea',
                     help='Processing mode: "idea" for ExtractIdea or "assertion" for ExtractAssertion or Nanograph for triples (default: idea)')
  
  args = parser.parse_args()
  
  markdown = read_text_file(args.input)
  if markdown is None:
    sys.exit(1)
    
  # Choose the processing function based on the mode argument
  if args.mode == 'assertion':
    r = workOnAssertion(markdown)
  elif args.mode == 'nanograph':
    r = workOnNanograph(markdown)
    # convert this to a dataframe with the columns: start end text label score
  else:  # Default to 'idea'
    r = workOnIdea(markdown)
  
  # Save to an output-file
  try:
    with open(args.output, 'w') as outfile:
      outfile.write(r.model_dump_json(indent=2))
    print(f"Results saved to {args.output}")
  except Exception as e:
    print(f"Error saving to output file: {e}")

if __name__ == "__main__":
     main()