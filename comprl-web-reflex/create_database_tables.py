#!/usr/bin/env python3
"""Create the database for a given configuration."""

import argparse
import contextlib
import logging
import pathlib
import sys

import sqlalchemy as sa

from comprl_web.reflex_local_auth.local_auth import LocalAuthSession


def main() -> int:
    """Main."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("db", type=pathlib.Path, help="Path to the database file.")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(asctime)s] [%(name)s | %(levelname)s] %(message)s",
    )

    engine = sa.create_engine(f"sqlite:///{args.db}")
    LocalAuthSession.metadata.create_all(engine)

    return 0


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        sys.exit(main())
