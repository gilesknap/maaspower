maaspower
=========

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

Power control webhook server for Canonical's MAAS. The requirements for 
such webhooks are defined here:

- https://maas.io/docs/snap/3.1/ui/power-management#heading--webhook

============== ==============================================================
PyPI           ``pip install maaspower``
Source code    https://github.com/gilesknap/maaspower
Documentation  https://gilesknap.github.io/maaspower
Releases       https://github.com/gilesknap/maaspower/releases
============== ==============================================================

This project implements MAAS power control to machines that do not already have 
a BMC type supported by MAAS. It uses webhooks to control any number of
remote switching devices that can power cycle such machines. 

The project uses an extensible architecture so more switching device types 
may be added, see `add_api`.

At present it supports two flavours of switching control:

- Command line interface. Anything that is controllable by a command line 
  utility that can be installed on the machine running this webhook service. 
- SmartThings API: a popular Samsung IoT protocol that is supported by 
  thousands of devices


.. |code_ci| image:: https://github.com/gilesknap/maaspower/workflows/Code%20CI/badge.svg?branch=main
    :target: https://github.com/gilesknap/maaspower/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/gilesknap/maaspower/workflows/Docs%20CI/badge.svg?branch=main
    :target: https://github.com/gilesknap/maaspower/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/gilesknap/maaspower/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/gilesknap/maaspower
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/maaspower.svg
    :target: https://pypi.org/project/maaspower
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://gilesknap.github.io/maaspower for more detailed documentation.
