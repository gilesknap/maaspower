import json
from pathlib import Path
from typing import Optional

import typer
from apischema.json_schema import deserialization_schema
from ruamel.yaml import YAML

from maaspower.config import MaasConfig

from . import __version__

cli = typer.Typer()
yaml = YAML()


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print the version of maaspower and exit",
    )
):
    """MAAS Power control webhook service"""


@cli.command()
def schema(
    output: Path = typer.Argument(..., help="The filename to write the schema to")
):
    """Produce the JSON global schema for mmaaspower config files"""
    schema = json.dumps(deserialization_schema(MaasConfig), indent=2)
    output.write_text(schema)
