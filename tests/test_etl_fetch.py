import asyncio
import unittest
from unittest.mock import AsyncMock, patch

# Adjust the import path based on your project structure if necessary
# This assumes that the 'defs' directory is in the PYTHONPATH
# or that tests are run from the root directory.
from defs.etl_fetch import fetch_resources

class TestEtlFetch(unittest.IsolatedAsyncioTestCase): # Changed to IsolatedAsyncioTestCase

    @patch('defs.etl_fetch.AsyncWebCrawler')
    async def test_fetch_resources_uses_source_url(self, MockAsyncWebCrawler):
        # Configure the mock
        mock_crawler_instance = MockAsyncWebCrawler.return_value
        # For async context manager __aenter__ and __aexit__ needs to be AsyncMock
        mock_crawler_instance.__aenter__ = AsyncMock(return_value=mock_crawler_instance)
        mock_crawler_instance.__aexit__ = AsyncMock(return_value=None) 
        
        # arun should also be an AsyncMock if it's awaited
        mock_crawler_instance.arun = AsyncMock(return_value=type('obj', (object,), {'markdown': 'mocked markdown'})()) 

        test_url = "http://example.com/test_source"
        
        await fetch_resources(test_url)

        mock_crawler_instance.arun.assert_called_once_with(url=test_url)

# Removed the if __name__ == '__main__': block to rely on test discovery
