import argparse
from typing import Callable

from src.config.config import Config

callback_function = Callable[[argparse.Namespace], None]


def build_argument_parser(config: callback_function, fetch: callback_function):
    argument_parser = argparse.ArgumentParser()

    subparsers = argument_parser.add_subparsers(required=True)

    config_parser = subparsers.add_parser("config", help="setup the configuration")
    config_parser.set_defaults(func=config)

    fetch_parser = subparsers.add_parser('fetch', help="fetch pods")
    fetch_parser.add_argument("patterns", help="pattern(s) for filtering services", nargs="+")
    fetch_parser.add_argument("-d", "--detailed", action="store_true", help="show details of each pod")
    fetch_parser.add_argument("-p", "--prod", action="store_true", help="fetch pods from production environment")
    fetch_parser.add_argument("-w", "--watch", action="store_true", help="fetch details in every 10 seconds")
    fetch_parser.add_argument("-n", "--namespace", action="store", default=Config().get("DEFAULT_NAMESPACE"),
                              help="k8s namespace")
    fetch_parser.set_defaults(func=fetch)

    return argument_parser
