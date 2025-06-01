import unittest
import os
import shutil # For cleaning up the fixtures directory
from defs.etl_convert import convert_document, html_to_markdown

# Attempt to import reportlab, which is needed for creating a dummy PDF
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class TestEtlConvert(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.base_dir = os.path.dirname(__file__)
        self.fixtures_dir = os.path.join(self.base_dir, "fixtures")
        if not os.path.exists(self.fixtures_dir):
            os.makedirs(self.fixtures_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.fixtures_dir):
            shutil.rmtree(self.fixtures_dir)

    def test_html_to_markdown_conversion(self):
        """Test direct HTML to Markdown conversion using html_to_markdown."""
        html_content = "<h1>Test Heading</h1><p>This is a test paragraph.</p>"
        # html2text uses # for H1
        expected_markdown = "# Test Heading\n\nThis is a test paragraph."
        markdown_content = html_to_markdown(html_content)
        # Normalize newlines and strip whitespace for comparison
        normalized_markdown = "\n".join(line.strip() for line in markdown_content.strip().splitlines() if line.strip())
        normalized_expected = "\n".join(line.strip() for line in expected_markdown.strip().splitlines() if line.strip())
        self.assertEqual(normalized_markdown, normalized_expected)

    def test_convert_document_html_local_file(self):
        """Test converting a local HTML file to Markdown using convert_document."""
        dummy_html_path = os.path.join(self.fixtures_dir, "dummy.html")
        html_content = "<html><body><h1>Local HTML Test</h1><p>A paragraph here.</p></body></html>"
        # html2text uses # for H1
        expected_markdown_fragment = "# Local HTML Test\n\nA paragraph here."
        
        with open(dummy_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        markdown_content = convert_document(local_file=dummy_html_path)
        self.assertIsNotNone(markdown_content)
        # Normalize for comparison
        normalized_markdown = "\n".join(line.strip() for line in markdown_content.strip().splitlines() if line.strip())
        normalized_expected = "\n".join(line.strip() for line in expected_markdown_fragment.strip().splitlines() if line.strip())
        self.assertIn(normalized_expected, normalized_markdown)

    @unittest.skipIf(not REPORTLAB_AVAILABLE, "reportlab is not installed, skipping PDF test.")
    def test_convert_document_pdf_local_file(self):
        """Test converting a local PDF file to Markdown using convert_document."""
        dummy_pdf_path = os.path.join(self.fixtures_dir, "dummy.pdf")
        pdf_text_content = "This is a test PDF document for conversion."

        # Create a dummy PDF using reportlab
        c = canvas.Canvas(dummy_pdf_path, pagesize=letter)
        c.drawString(100, 750, pdf_text_content)
        c.save()

        self.assertTrue(os.path.exists(dummy_pdf_path), "Dummy PDF file was not created.")

        markdown_content = convert_document(local_file=dummy_pdf_path)
        self.assertIsNotNone(markdown_content, "Markdown conversion returned None.")
        
        # PyPDF2 adds "## Page X" headers. We need to check if the text content is present.
        # The exact output can vary, so we check for the presence of the core text.
        self.assertIn(pdf_text_content, markdown_content, 
                      f"Expected text '{pdf_text_content}' not found in converted Markdown:\n{markdown_content}")

    def test_convert_document_no_source(self):
        """Test convert_document with no source provided."""
        # Expecting it to print an error and return None
        with unittest.mock.patch('builtins.print') as mocked_print:
            result = convert_document()
            self.assertIsNone(result)
            mocked_print.assert_any_call("Error: Please provide either a URL or a local file.")

    def test_convert_document_both_sources(self):
        """Test convert_document with both URL and local_file provided."""
        dummy_html_path = os.path.join(self.fixtures_dir, "dummy_both.html")
        with open(dummy_html_path, "w") as f:
            f.write("<p>test</p>")
        
        with unittest.mock.patch('builtins.print') as mocked_print:
            result = convert_document(url="http://example.com", local_file=dummy_html_path)
            self.assertIsNone(result)
            mocked_print.assert_any_call("Error: Please provide either a URL or a local file, not both.")

if __name__ == '__main__':
    unittest.main()
