from argparse import Namespace
import os
import sys


def config_callback(args: Namespace):
    from src.config.config import config
    config.setup_config_file()
    exit(0)


def fetch_callback(args: Namespace):
    from src.k8s.watcher import Watcher
    from src.util.utils import get_kubectl_context

    context = get_kubectl_context(args.prod)
    namespace = args.namespace
    patterns = args.patterns
    is_periodic = args.watch
    is_detailed = args.detailed

    Watcher(context, namespace, is_periodic, is_detailed, patterns)


if __name__ == "__main__":
    dirname = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(dirname)

    from src.util.argument_parser import build_argument_parser

    argument_parser = build_argument_parser(config_callback, fetch_callback)
    parsed_args = argument_parser.parse_args()
    parsed_args.func(parsed_args)
