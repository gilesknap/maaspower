import json
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from maaspower import __version__
from maaspower.__main__ import cli

runner = CliRunner()


def test_cli_version():
    cmd = [sys.executable, "-m", "maaspower", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__


def test_pmac_schema(tmp_path: Path, samples: Path):
    """generate the schema file for maaspower configuration YAML"""
    schema_path = tmp_path / "maaspower.schema.json"
    result = runner.invoke(cli, ["schema", str(schema_path)])
    assert result.exit_code == 0, f"schema failed with: {result}"

    with open(samples / "maaspower.schema.json") as stream:
        expected = json.loads(stream.read())

    with open(schema_path) as stream:
        actual = json.loads(stream.read())

    assert expected == actual
