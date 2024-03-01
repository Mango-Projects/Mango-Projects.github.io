import tomllib
from pathlib import Path
import re

import pretty_errors

import json


def pprint(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


CURRENT_PATH = Path(__file__).parent

with open(CURRENT_PATH / "data.toml", "rb") as file:
    _data = tomllib.load(file)

    TRANSFER_URL_BASE = _data["transfer_url_base"]
    HTML_BASE = _data["html_base"]
    MARKDOWN_BASE = _data["markdown_base"]
    TABLE_BASE = _data["table_base"]
    URL_MAPPING = _data["url_mapping"]

with open(CURRENT_PATH / "url.toml", "rb") as file:
    URL = tomllib.load(file)


def generate_markdown():
    lines = []
    for namespace, data in URL.items():
        for url_type, path in data.items():
            lines.append(
                TABLE_BASE.format(
                    namespace=namespace,
                    path=path,
                    original_url=URL_MAPPING[url_type] + path,
                    transfer_url=TRANSFER_URL_BASE.format(
                        namespace=namespace, type=url_type
                    ),
                )
            )
    with open(CURRENT_PATH / "index.md", "w", encoding="utf8") as file:
        file.write(MARKDOWN_BASE + "\n".join(lines))


def generate_html():
    for namespace, data in URL.items():
        namespace_path = CURRENT_PATH / namespace
        namespace_path.mkdir(exist_ok=True)
        for url_type, path in data.items():
            with open(namespace_path / f"{url_type}.html", "w") as file:
                file.write(HTML_BASE.format(url=URL_MAPPING[url_type] + path))


def main():
    generate_html()
    generate_markdown()


if __name__ == "__main__":
    main()
