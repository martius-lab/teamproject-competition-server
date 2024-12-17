#!/usr/bin/env python3
"""Create the database for a given configuration."""

import argparse
import contextlib
import logging
import pathlib
import sys

from comprl.server.data import sql_backend

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]


def main() -> int:
    """main."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config", type=pathlib.Path, help="Path to the configuration file."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(asctime)s] [%(name)s | %(levelname)s] %(message)s",
    )

    with open(args.config, "rb") as f:
        config = tomllib.load(f)["CompetitionServer"]

    if config["user_db_path"] != config["game_db_path"]:
        print(
            "ERROR: user_db_path and game_db_path must be the same."
            "  Separate databases are not supported anymore.",
            file=sys.stderr,
        )
        return 1

    db_path = config["user_db_path"]

    if (
        "user_db_name" in config
        and config["user_db_name"] != sql_backend.User.__tablename__
    ):
        print(
            f"ERROR: user_db_name must be '{sql_backend.User.__tablename__}'."
            "  Custom names are not supported anymore.",
            file=sys.stderr,
        )
        return 1

    if (
        "game_db_name" in config
        and config["game_db_name"] != sql_backend.Game.__tablename__
    ):
        print(
            f"ERROR: game_db_name must be '{sql_backend.Game.__tablename__}'."
            "  Custom names are not supported anymore.",
            file=sys.stderr,
        )
        return 1

    if pathlib.Path(db_path).exists():
        print(f"ERROR: Database '{db_path}' already exists.", file=sys.stderr)
        return 1
    sql_backend.create_database_tables(db_path)

    return 0


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        sys.exit(main())