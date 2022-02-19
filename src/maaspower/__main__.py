import json
from pathlib import Path
from typing import Optional

import jsonschema
import typer
from apischema.json_schema import deserialization_schema
from ruamel.yaml import YAML

from . import __version__

# import all sublasses of SwitchDevice so ApiSchema sees them
from .devices.shell_cmd import CommandLine
from .devices.smart_thing import SmartThing
from .maasconfig import MaasConfig
from .webhook import run_web_hook

# avoid linter complaints
required_to_find_subclasses = [SmartThing, CommandLine]

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


@cli.command()
def run(
    config: Path = typer.Argument(..., help="configuration for the webhook server")
):
    """Read the configuration file and stand up a web hook server"""

    config_dict = YAML().load(config)
    schema_config = deserialization_schema(MaasConfig)
    jsonschema.validate(config_dict, schema_config)

    maas_config = MaasConfig.deserialize(config_dict)

    run_web_hook(maas_config)


# allow tests with:
#     pipenv run python -m maaspower
if __name__ == "__main__":
    cli()
