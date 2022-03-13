.. _yaml_schema:

YAML schema
===========

Maaspower provides a schema for its configuration file. If you use a schema 
aware YAML editor then this will use hints and auto completion to help
create the config.

You can generate a schema file with the command::

    masspower schema <schema file name>

You can instruct schema aware editors to use a schema file with the following
modeline at the start of the YAML file::

    # yaml-language-server: $schema=https://my.url.to/the/schema

Note that local schema files are supported with relative or absolute file names
(at least in vscode).

A popular choice for YAML aware editing is vscode.

Below is a useful discussion on yaml/json schema including how to enable
schema validated editing of yaml files in vscode.

https://dev.to/brpaz/how-to-create-your-own-auto-completion-for-json-and-yaml-files-on-vs-code-with-the-help-of-json-schema-k1i
