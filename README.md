[![CI](https://github.com/gilesknap/maaspower/actions/workflows/ci.yml/badge.svg)](https://github.com/gilesknap/maaspower/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/gilesknap/maaspower/branch/main/graph/badge.svg)](https://codecov.io/gh/gilesknap/maaspower)
[![PyPI](https://img.shields.io/pypi/v/maaspower.svg)](https://pypi.org/project/maaspower)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# maaspower

Power control webhook server for Canonical's MAAS.

The requirements for such webhooks are defined here:

- https://maas.io/docs/snap/3.1/ui/power-management#heading--webhook


Source          | <https://github.com/gilesknap/maaspower>
:---:           | :---:
PyPI            | `pip install maaspower`
Docker          | `docker run ghcr.io/gilesknap/maaspower:latest`
Documentation   | <https://gilesknap.github.io/maaspower>
Releases        | <https://github.com/gilesknap/maaspower/releases>


This project implements MAAS power control for machines that do not already have
a BMC type supported by MAAS. It uses webhooks to control any number of
remote switching devices that can power cycle such machines.

The project uses an extensible architecture so more switching device types
may be added, see `add_api`.

At present it supports two flavours of switching control:

- Command line interface. Anything that is controllable by a command line
  utility that can be installed on the machine running this webhook service.
- SmartThings API: a popular Samsung IoT protocol that is supported by
  thousands of devices
- Web UI controlled devices - uses selenium to connect to the web UI and control
  the device. A basic DSL describes the UI fields to scrape.
- Cisco IOS PoE Switches



```python
from maaspower import __version__

print(f"Hello maaspower {__version__}")
```

Or if it is a commandline tool then you might put some example commands here:

```
python -m maaspower --version
```

<!-- README only content. Anything below this line won't be included in index.md -->

See https://gilesknap.github.io/maaspower for more detailed documentation.
