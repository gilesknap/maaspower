from argparse import ArgumentParser

from . import __version__
from .hello import HelloClass, run_test

__all__ = ["main"]


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("token", help="SmartThings API token")
    args = parser.parse_args(args)
    run_test(args.token)


# test with: pipenv run python -m maaspower
if __name__ == "__main__":
    main()
