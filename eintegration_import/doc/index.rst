Import Documentation
=========================

This module allows to upload regular Odoo data files directly into a running Odoo instance.

First, get an Odoo session Cookie using /login.

Use a POST request to <Your Odoo URL>/import with application/www-url-encoded form.
There are two parameters required:
- module:    is an arbitrary string used as the module name when generating External IDs
- data_file: is a file to import (Currently, only XML files are supported)

The script bin/import_files shows how to use curl to implement a simple upload client.