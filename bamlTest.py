from baml_client.sync_client import b
from baml_client.types import Idea
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

def main():
  # Set up command line argument parsing
  parser = argparse.ArgumentParser(description='Process markdown text and extract ideas.')
  parser.add_argument('--input', '-i', required=True, 
                     help='Input markdown file path')
  parser.add_argument('--output', '-o', required=True, 
                     help='Output file path for JSON results')
  
  args = parser.parse_args()
  
  markdown = read_text_file(args.input)
  if markdown is None:
    sys.exit(1)
    
  r = workOnIdea(markdown)
  
  # Save to output-file
  try:
    with open(args.output, 'w') as outfile:
      outfile.write(r.model_dump_json(indent=2))
    print(f"Results saved to {args.output}")
  except Exception as e:
    print(f"Error saving to output file: {e}")

if __name__ == "__main__":
     main()