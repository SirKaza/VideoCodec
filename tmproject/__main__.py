"""
The __main__.py file is a component of a Python module that is executed when the module is run using the
command `python -m module_name`. This file is used to define the entry point of the module, and it is
responsible for executing the main functionality of the module.
"""
# Imports should go at the top of the file, before any other code:
from . import cli

# An if statement should be used to check if the module is being run as the main program:
if __name__ == '__main__':
    cli.main()

