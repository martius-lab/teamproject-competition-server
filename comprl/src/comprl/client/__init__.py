"""API for implementing a comprl client."""

from __future__ import annotations

import argparse
import os
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Callable

from .agent import Agent


class EnvDefault(argparse.Action):
    """argparse action to get default values from environment variables.

    By Russell Heilling, License: CC BY-SA 4.0
    https://stackoverflow.com/a/10551190/2095383
    """

    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):  # noqa: D102
        setattr(namespace, self.dest, values)


def launch_client(initialize_agent_func: Callable[[list[str]], Agent]):
    """Launch the comprl client and connect to the server.

    This function parses command line arguments to get the server connection information
    (url, port and access token).  Alternatively, these arguments can also be set via
    environment variables ``COMPRL_SERVER_URL``, ``COMPRL_SERVER_PORT`` and
    ``COMPRL_ACCESS_TOKEN``.
    It then initializes an Agent instance using the given function.

    Custom arguments for ``initialize_agent_func`` can be passed on the command line
    using ``--args``.

    Args:
        initialize_agent_func: Function that returns an initialized Agent instance.
            The function takes as argument a (possibly empty) list of command line
            arguments that are passed after ``--args``.
            It is expected to return an instance of a subclass of ``Agent``.
    """
    parser = argparse.ArgumentParser(description="comprl client launcher")
    parser.add_argument(
        "--server-url",
        type=str,
        action=EnvDefault,
        envvar="COMPRL_SERVER_URL",
        help="""URL of the server.  Can also be set via the environment variable
            COMPRL_SERVER_URL.
        """,
    )
    parser.add_argument(
        "--server-port",
        type=int,
        action=EnvDefault,
        envvar="COMPRL_SERVER_PORT",
        help="""Port of the server.  Can also be set via the environment variable
            COMPRL_SERVER_PORT.
        """,
    )
    parser.add_argument(
        "--token",
        type=str,
        action=EnvDefault,
        envvar="COMPRL_ACCESS_TOKEN",
        metavar="ACCESS_TOKEN",
        help="""Your access token.  Can also be set via the environment variable
            COMPRL_ACCESS_TOKEN.
        """,
    )
    parser.add_argument(
        "--args",
        dest="agent_args",
        nargs=argparse.REMAINDER,
        help="Any additional arguments are passed to the agent.",
    )
    args = parser.parse_args()

    agent = initialize_agent_func(args.agent_args)

    agent.run(token=args.token, host=args.server_url, port=args.server_port)


__all__ = ["Agent", "launch_client"]
