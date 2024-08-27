"""
This script demonstrates a simple CLI application using Click.

How to run this file:
- To run the script normally without any options, use:
  $ python cli.py

- To enable debug mode, use the --debug option:
  $ python cli.py --debug

- To display help information about the command and its options, use:
  $ python cli.py --help

What to expect from the output:
- If no options are provided, the output will indicate that debug mode is not enabled.
- If the --debug option is provided, the script will indicate that debug mode is enabled.
- If the --help option is provided, you will see the following output:

Usage:  [OPTIONS]

  Simple program that greets NAME for a total of COUNT times.

Options:
  --debug     Enters debug mode
  -h, --help  Show this message and exit.
"""
import click


@click.command()
@click.option('--debug', is_flag=True, help='Enters debug mode')
@click.help_option('--help', '-h')
def main(debug):
    """Simple program that greets NAME for a total of COUNT times."""
    if debug:
        click.echo("Debug mode is enabled")
    else:
        click.echo("Debug mode is not enabled")


if __name__ == '__main__':
    main()

