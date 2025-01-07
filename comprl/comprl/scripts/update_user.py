#!/usr/bin/env python3
"""Update user entries in the database."""

import argparse
import contextlib
import getpass
import logging
import pprint
import sys

import sqlalchemy as sa

from comprl.server.data.sql_backend import User, hash_password
from comprl.server.data.interfaces import UserRole


def main() -> int:
    """Main."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=str, help="Path to the database file.")
    parser.add_argument("username", type=str, help="Name of the user")
    parser.add_argument("--set-password", action="store_true", help="Set new password")
    parser.add_argument(
        "--set-role",
        type=str,
        choices=[UserRole.USER.value, UserRole.ADMIN.value, UserRole.BOT.value],
        help="Set new role",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(asctime)s] [%(name)s | %(levelname)s] %(message)s",
    )

    engine = sa.create_engine(f"sqlite:///{args.database}")

    with sa.orm.Session(engine) as session:
        changed = False
        user = session.scalar(sa.select(User).where(User.username == args.username))

        if user is None:
            logging.error("User '%s' does not exist", args.username)
            return 1

        if args.set_password:
            new_pw = getpass.getpass(f"New password for user {args.username}:")
            new_pw2 = getpass.getpass("Repeat new password:")
            if new_pw != new_pw2:
                print("FAILURE: Passwords do not match.")
                return 1
            user.password = hash_password(new_pw)
            changed = True

        if args.set_role:
            user.role = args.set_role
            changed = True

        if changed:
            session.commit()
            session.refresh(user)

    # print the user entry
    pprint.pprint(user)

    return 0


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        sys.exit(main())
