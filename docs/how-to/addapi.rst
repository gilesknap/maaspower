.. _add_api:

How to add support for a new API
================================

Here we discuss how to extend this package to support new devices with
APIs that are not currently covered.

Steps
-----

There are only a few steps required.

- add a new python file to the devices folder. Copying shell_cmd.py would be
  an excellent start. The new class in the new file will be a subclass of
  ``MaasConfig``

- Implement your own versions of turn_on, turn_off, query_state.

- if you need any addition configuration information in the config file 
  then add some more dataclass properties (e.g. see ``device_id`` in smart_thing.py)

- make sure that the new class is reference in __main__ by adding it to
  ``required_to_find_subclasses`` list.

- regenerate a schema for helping define the configuration file

  - ``maaspower schema <path to new schema file>``

