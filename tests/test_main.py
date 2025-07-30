import json
import sys
import os

import pytest

sys.path.insert(0, os.path.abspath('.'))
import src.main as cli


def test_parse_args():
    test_args = ['prog', '--query', 'python', '--num', '3']
    with pytest.MonkeyPatch.context() as m:
        m.setattr(sys, 'argv', test_args)
        parsed = cli.parse_args()
    assert parsed.query == 'python'
    assert parsed.num == 3


def test_parse_args_default_num():
    test_args = ['prog', '--query', 'python']
    with pytest.MonkeyPatch.context() as m:
        m.setattr(sys, 'argv', test_args)
        parsed = cli.parse_args()
    assert parsed.num == 5


def test_main_output(capsys, monkeypatch):
    async def fake_search(query: str, num: int):
        return [{"title": "T", "href": "/t", "body": "B"}]

    monkeypatch.setattr(cli, 'search_elibrary', fake_search)
    test_args = ['prog', '--query', 'python', '--num', '1']
    monkeypatch.setattr(sys, 'argv', test_args)
    cli.main()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data[0]['title'] == 'T'
