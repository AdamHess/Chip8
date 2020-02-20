import sys
from os.path import exists
from chip import Chip


def main():
    filename = sys.argv[1]
    if not exists(filename):
        raise Exception("file not found")
    c = Chip(read_file_byte(filename))
    c.dump_ram()


def read_file_byte(filename):
    with open(filename, 'rb') as file:
        return file.read()


if __name__ == "__main__":
    main()
