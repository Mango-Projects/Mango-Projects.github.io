import tomllib
from pathlib import Path


CURRENT_PATH = Path(__file__).parent

_data = tomllib.loads((CURRENT_PATH / "data.toml").read_text(encoding="utf8"))
TRANSFER_URL_BASE = _data["transfer_url_base"]
HTML_BASE = _data["html_base"]
MARKDOWN_BASE = _data["markdown_base"]
TABLE_BASE = _data["table_base"]
URL_MAPPING = _data["url_mapping"]

URL = tomllib.loads((CURRENT_PATH / "url.toml").read_text(encoding="utf8"))


def process_urls(process_func):
    for namespace, data in URL.items():
        for url_type, path in data.items():
            process_func(namespace, url_type, path)


def generate_markdown():
    lines = []

    def process_func(namespace: str, url_type: str, path: str):
        lines.append(
            TABLE_BASE.format(
                namespace=namespace,
                path=path,
                original_url=f"{URL_MAPPING[url_type]}{path}",
                transfer_url=f"{TRANSFER_URL_BASE.format(namespace=namespace, type=url_type)}",
            )
        )

    process_urls(process_func)
    (CURRENT_PATH / "index.md").write_text(
        MARKDOWN_BASE + "\n".join(lines), encoding="utf8"
    )


def generate_html():

    def process_func(namespace: str, url_type: str, path: str):
        namespace_path = CURRENT_PATH / namespace
        namespace_path.mkdir(exist_ok=True)
        (namespace_path / f"{url_type}.html").write_text(
            HTML_BASE.format(url=f"{URL_MAPPING[url_type]}{path}"), encoding="utf8"
        )

    process_urls(process_func)


def main():
    generate_html()
    generate_markdown()


if __name__ == "__main__":
    main()
