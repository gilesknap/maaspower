maaspower
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

Power control webhook server for Canonical's MAAS. See here
https://discourse.maas.io/t/creating-a-web-service-for-the-maas-webhook-power-driver/3756
for details of the requirements.

============== ==============================================================
PyPI           ``pip install maaspower``
Source code    https://github.com/dls-controls/maaspower
Documentation  https://dls-controls.github.io/maaspower
Releases       https://github.com/dls-controls/maaspower/releases
============== ==============================================================

This project adds MAAS power control to servers that do not already have 
a BMC type that MAAS supports. It uses a webhook to control switching 
equipment that can power cycle such servers. 

The project uses an extensible architecture so more switching device types 
may be added, see `How to add support for a new API`.

At present it supports two flavours of switching control:

- Command line interface. Anything that is controllable by a command line 
  utility that can be installed on the machine running this webhook service. 
- SmartThings API: a popular Samsung IoT protocol that is supported by 
  thousands of devices


.. code:: python

    from maaspower.hello import HelloClass

    hello = HelloClass("me")
    print(hello.format_greeting())

Or if it is a commandline tool then you might put some example commands here::

    maaspower person --times=2

.. |code_ci| image:: https://github.com/dls-controls/maaspower/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/maaspower/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/dls-controls/maaspower/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/maaspower/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/dls-controls/maaspower/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dls-controls/maaspower
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

See https://dls-controls.github.io/maaspower for more detailed documentation.
