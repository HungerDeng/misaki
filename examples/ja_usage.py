"""
1. prerequisite: Download unidic ONCE. skip this step if the dictionary is already installed
```
unidic is already declared in pyproject.toml (ja = [..., "unidic", ...]). However, the Python package and the actual dictionary data are separate. The dictionary is very large, so upstream requires a separate download step after installation. UniDic’s documentation (https://github.com/polm/unidic-py) explicitly documents this workflow.

Therefore, run this once per environment:

uv run --extra ja python -m unidic download
```

2. Then Run:
uv run --extra ja examples/ja_usage.py ["text"]


testing examples:
uv run --extra ja examples/ja_usage.py  "東京・渋谷のＮＨＫ放送センターに建設した新たな施設・情報棟で、ニュースセンターとラジオセンターなどが、きょうから本格的に運用を開始しました。"

uv run --extra ja examples/ja_usage.py "ローマ字で konnichiwa sekai と書きます。"

uv run --extra ja examples/ja_usage.py "OpenAIのGPT-5を試します。"

uv run --extra ja examples/ja_usage.py "東京とTokyoを比較します。"

uv run --extra ja examples/ja_usage.py "2026年9月9日に発売します。"

uv run --extra ja examples/ja_usage.py "価格は1,234円です。"

uv run --extra ja examples/ja_usage.py "電話番号は03-1234-5678です。"

uv run --extra ja examples/ja_usage.py "AIモデル v2.0 は100%日本語に対応します。"

uv run --extra ja examples/ja_usage.py "メールはtest@example.comです。"

uv run --extra ja examples/ja_usage.py "URLはhttps://example.comです。"

uv run --extra ja examples/ja_usage.py "ABC xyz Tokyo 42nd Street"

"""

import argparse

from misaki.ja import JAG2P


DEFAULT_TEXT = "こんにちは、世界。"
VERSIONS = ("cutlet", "pyopenjtalk")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "text",
        nargs="*",
        help=f"Japanese text to convert (defaults to {DEFAULT_TEXT})",
        default=None,
    )
    args = parser.parse_args()
    text = " ".join(args.text) if args.text else DEFAULT_TEXT

    print(f"Input: {text}")
    for version in VERSIONS:
        print(f"{version}: ---------------------------------------")
        phonemes, tokens = JAG2P(version=version)(text, return_pitch=False)
        print(f"phonemes text: {phonemes}")
        if tokens is None:
            print("tokens: None")
            continue
        print("tokens:")
        for token in tokens:
            print(f"  {token}")


if __name__ == "__main__":
    main()
