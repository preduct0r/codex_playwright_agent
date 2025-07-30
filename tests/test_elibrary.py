import os
import sys
import pytest

sys.path.insert(0, os.path.abspath("src"))
import elibrary


HTML_SAMPLE = """
<div class="search-result">
  <div class="title"><a href="/paper1.pdf">Paper 1</a></div>
  <div class="abstract">Abstract 1</div>
</div>
<div class="search-result">
  <div class="title"><a href="/paper2.pdf">Paper 2</a></div>
  <div class="abstract">Abstract 2</div>
</div>
"""


def test_parse_search_results():
    results = elibrary.parse_search_results(HTML_SAMPLE, 2)
    assert results == [
        {"title": "Paper 1", "href": "/paper1.pdf", "body": "Abstract 1"},
        {"title": "Paper 2", "href": "/paper2.pdf", "body": "Abstract 2"},
    ]


def test_parse_search_results_no_abstract():
    html = """
    <div class="search-result">
      <div class="title"><a href="/paper.pdf">Paper</a></div>
    </div>
    """
    results = elibrary.parse_search_results(html, 1)
    assert results == [
        {"title": "Paper", "href": "/paper.pdf", "body": ""}
    ]


@pytest.mark.asyncio
async def test_search_elibrary(monkeypatch):
    async def fake_fetch(query: str) -> str:
        assert query == "python"
        return HTML_SAMPLE

    monkeypatch.setattr(elibrary, "fetch_search_html", fake_fetch)
    results = await elibrary.search_elibrary("python", 1)
    assert results == [
        {"title": "Paper 1", "href": "/paper1.pdf", "body": "Abstract 1"}
    ]
