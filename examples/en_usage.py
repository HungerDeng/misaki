"""
1. Install the English extra ONCE:
```
uv sync --extra en
```

2. Install the spaCy model ONCE:
uv run --extra en python -m spacy download en_core_web_sm

3. Then Run:
uv run --extra en examples/en_usage.py ["text"]


examples:
uv run --extra en examples/en_usage.py "Hello, world."

uv run --extra en examples/en_usage.py "Misaki is a G2P engine designed for Kokoro models."

uv run --extra en examples/en_usage.py "OpenAI's GPT-5 launches on September 9, 2026."

uv run --extra en examples/en_usage.py 'The price is $1,234.56.'

uv run --extra en examples/en_usage.py "Email test@example.com or visit https://example.com."

"""

import argparse

from misaki.en import G2P
from misaki.espeak import EspeakFallback


DEFAULT_TEXT = "Hello, world."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "text",
        nargs="*",
        help=f"English text to convert (defaults to {DEFAULT_TEXT})",
        default=None,
    )
    args = parser.parse_args()
    text = " ".join(args.text) if args.text else DEFAULT_TEXT

    print(f"Input: {text}")
    g2p = G2P(trf=False, british=False, fallback=EspeakFallback(british=False))
    phonemes, tokens = g2p(text)
    print(f"phonemes text: {phonemes}")
    if tokens is None:
        print("tokens: None")
        return
    print("tokens:")
    for token in tokens:
        print(f"  {token}")


if __name__ == "__main__":
    main()
