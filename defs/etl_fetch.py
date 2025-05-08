from io import StringIO
from pathlib import Path

import lancedb
import polars as pl
import requests

import asyncio
from crawl4ai import *


async def fetch_resources(source):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            # url="https://www.waterqualitydata.us"
            url="https://www.hydrosheds.org/hydrosheds-core-downloads",
        )

    print(result.markdown)