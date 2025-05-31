import requests
import os
import logging
import tempfile
from urllib.parse import urlparse

# We'll need to install these libraries
# pip install html2text PyPDF2 requests

try:
    import html2text
    import PyPDF2
except ImportError:
    logger.exception("Failed to import html2text or PyPDF2. Please install them using: pip install html2text PyPDF2")
    exit(1)

logger = logging.getLogger(__name__)

def is_url(path):
    """Check if the given path is a URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_pdf(path):
    """Check if the given path is a PDF file."""
    if is_url(path):
        # For URLs, check the file extension
        return path.lower().endswith('.pdf')
    else:
        # For local files, check the file extension
        return os.path.splitext(path)[1].lower() == '.pdf'

def download_file(url):
    """Download a file from a URL to a temporary file."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_path = temp_file.name
        
        # Write the content to the temporary file
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        
        temp_file.close()
        return temp_file_path
    except Exception as e:
        logger.exception(f"Error downloading file: {e}")
        return None

def html_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap text
    return h.handle(html_content)

def pdf_to_markdown(pdf_path):
    """Convert PDF content to Markdown."""
    try:
        markdown_text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Add page header
                markdown_text += f"## Page {page_num + 1}\n\n"
                
                # Add page content
                markdown_text += text + "\n\n"
        
        return markdown_text
    except Exception as e:
        logger.exception(f"Error converting PDF to Markdown: {e}")
        return None

def convert_to_markdown(source, is_local=False):
    """Convert HTML or PDF to Markdown."""
    try:
        if is_local:
            # Local file
            file_path = source
        else:
            # URL
            file_path = download_file(source)
            if not file_path:
                return None
        
        # Check if it's a PDF
        if is_pdf(source):
            return pdf_to_markdown(file_path)
        else:
            # Assume it's HTML
            if is_local:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
            
            # Delete the temporary file if it was downloaded
            if not is_local:
                os.unlink(file_path)
                
            return html_to_markdown(html_content)
    except Exception as e:
        logger.exception(f"Error converting to Markdown: {e}")
        return None

def convert_document(url=None, local_file=None, output_file=None):
    """
    Convert a document (HTML or PDF) to Markdown.
    
    Args:
        url (str, optional): URL of the document to convert.
        local_file (str, optional): Path to a local document to convert.
        output_file (str, optional): Path to save the Markdown output.
        
    Returns:
        str: The Markdown content or None if conversion failed.
    """
    if url and local_file:
        logger.error("Error: Please provide either a URL or a local file, not both.")
        return None
    
    if not url and not local_file:
        logger.error("Error: Please provide either a URL or a local file.")
        return None
    
    # Convert the document
    if url:
        markdown_content = convert_to_markdown(url, is_local=False)
    else:
        markdown_content = convert_to_markdown(local_file, is_local=True)
    
    if not markdown_content:
        return None
    
    # Save to file if output_file is provided
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            logger.info(f"Markdown saved to {output_file}")
        except Exception as e:
            logger.exception(f"Error saving Markdown to file: {e}")
    
    return markdown_content