"""Handle some random choices"""
import random

from pysyte.cli import app


def flip() -> bool:
    return random.choice((True, False))


def coin() -> str:
    return "heads" if flip() else "tails"


def main():
    result = coin()
    assert result == "heads", f"{result=}"


if __name__ == "__main__":
    app.exit(main)
