from pathlib import Path
from setuptools import setup, find_packages

# Read the contents of the requirements file:
requirements = Path('requirements.txt').read_text().strip().split('\n')

setup(
    name='tmproject',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    url='',
    license='',
    author='Marc Casanova',
    author_email='mcasanto14@alumnes.ub.edu',
    description='Projecte de pràctiques de l\'assignatura Tecnologies Multimèdia',
    entry_points={
        'console_scripts': [
            'tmproject = tmproject.cli:main',
        ],
    }
)
