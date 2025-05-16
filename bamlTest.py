from baml_client.sync_client import b
from baml_client.types import Idea

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

  markdown = read_text_file("secret/agingText.md")
  r = workOnIdea(markdown)

  print("----------------")
  print(r.model_dump_json(indent=2))

if __name__ == "__main__":
     main()

