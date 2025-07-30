from __future__ import annotations

import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

SEARCH_URL = "https://elibrary.ru/querybox.asp?searchtype=simple&query={query}"

async def fetch_search_html(query: str) -> str:  # pragma: no cover - requires network
    """Fetch raw HTML for a search query using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(SEARCH_URL.format(query=query))
        html = await page.content()
        await browser.close()
    return html


def parse_search_results(html: str, num: int) -> List[Dict[str, str]]:
    """Parse eLibrary search results from HTML and return up to ``num`` items."""
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('.search-result')
    results: List[Dict[str, str]] = []
    for item in items[:num]:
        title_el = item.select_one('.title a')
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = title_el.get('href', '')
        abstract_el = item.select_one('.abstract')
        body = abstract_el.get_text(strip=True) if abstract_el else ''
        results.append({
            "title": title,
            "href": href,
            "body": body,
        })
    return results


async def search_elibrary(query: str, num: int) -> List[Dict[str, str]]:
    """Search elibrary and return parsed results."""
    html = await fetch_search_html(query)
    return parse_search_results(html, num)


if __name__ == "__main__":  # pragma: no cover - manual execution
    # Simple manual test
    import json
    import sys

    q = sys.argv[1] if len(sys.argv) > 1 else "test"
    result = asyncio.run(search_elibrary(q, 5))
    print(json.dumps(result, ensure_ascii=False, indent=2))
