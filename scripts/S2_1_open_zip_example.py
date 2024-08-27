"""
This script demonstrates how to open a file from a zip file using Python. First, we need to define the path of the zip
file using the `Path` class from the `pathlib` library. Then, we can use the `ZipFile` class from the `zipfile` library
to open the zip file. Finally, we can use the `open` method from the `ZipFile` class to open a file from the zip file.
"""
# Import dependencies from standard library:
from pathlib import Path
from zipfile import ZipFile

# Execute only if run as a script:
if __name__ == '__main__':
    # Define the path of the zip file:
    zip_path = Path('data/raw/hola.zip')

    # Open a zip file using a context manager and the `ZipFile` class, then open a file from the zip file using the
    # `open` method from the `ZipFile` class:
    with ZipFile(zip_path, 'r') as zip_file:

        # ZipFile objects allow to open files within the zip file using the `open` method, this opens the files inside
        # as a stream. This is useful to read the content of the file without extracting it in a temporal folder:
        with zip_file.open('mon.txt') as file:
            # Now the object `file` is a stream object, we can read the content of the file using the `read` method:
            print(file.read().decode('utf-8'))

            # As it is a stream we can move to a specific position using the `seek` method:
            file.seek(0)

            # And read it again:
            content = file.read().decode('utf-8')

            # Finally, we can print only part of the content:
            print(content.split(' ')[0])

