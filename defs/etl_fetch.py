from io import StringIO
from pathlib import Path

import lancedb
import polars as pl
import requests

import asyncio
from crawl4ai import *
import logging

logger = logging.getLogger(__name__)

async def fetch_resources(source):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=source,
        )

    logger.info(result.markdown)