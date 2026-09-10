"""
1. Install the Chinese extra ONCE:
```
uv sync --extra zh
```

2. Then Run:
uv run --extra zh examples/zh_usage.py ["text"]


testing examples:
uv run --extra zh examples/zh_usage.py "北京天安门广场今天阳光明媚。"

uv run --extra zh examples/zh_usage.py "欢迎使用 OpenAI 的 GPT-5。"

uv run --extra zh examples/zh_usage.py "我们将于2026年9月9日发布新版本。"

uv run --extra zh examples/zh_usage.py "价格是1,234.56元，打九折。"

uv run --extra zh examples/zh_usage.py "客服电话是400-123-4567，邮箱是test@example.com。"

uv run --extra zh examples/zh_usage.py "详情请访问 https://example.com。"

"""

import argparse

from misaki.zh import ZHG2P


DEFAULT_TEXT = "你好，世界。"
VERSIONS = (("legacy", None), ("frontend", "1.1"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "text",
        nargs="*",
        help=f"Chinese text to convert (defaults to {DEFAULT_TEXT})",
        default=None,
    )
    args = parser.parse_args()
    text = " ".join(args.text) if args.text else DEFAULT_TEXT

    print(f"Input: {text}")
    for name, version in VERSIONS:
        print(f"{name}: ---------------------------------------")
        phonemes, tokens = ZHG2P(version=version)(text)
        print(f"phonemes text: {phonemes}")
        if tokens is None:
            print("tokens: None")
            continue
        print("tokens:")
        for token in tokens:
            print(f"  {token}")


if __name__ == "__main__":
    main()
