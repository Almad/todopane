"""
Main entry point for the application.
"""

import sys
import tomli

from planner import get_daily_plan


def load_config(filename: str) -> dict:
    try:
        with open(filename, "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        print(f"Config file {filename} not found")
        sys.exit(1)


def main():
    config = load_config("config.toml")

    plan = get_daily_plan(config)
    print(plan)


if __name__ == "__main__":
    main()
