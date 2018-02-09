"""Usage:
  novaConfParser_V2.py [--input <path-to-input-file>] [--par <par>]

Options:
  -h --help       Show this help screen.

Examples:
  python3 novaConfParser_V2.py --input /nova/nova.conf --par my_ip

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')
    print(arguments)
