import argparse
import asyncio
import json

try:
    from .elibrary import search_elibrary
except ImportError:  # pragma: no cover - allow running as script
    from elibrary import search_elibrary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search articles on eLibrary")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--num", type=int, default=5, help="Number of results")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = asyncio.run(search_elibrary(args.query, args.num))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
