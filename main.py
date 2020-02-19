import binascii
import sys
from os.path import exists


def main():
    filename = sys.argv[1]
    if not exists(filename):
        raise Exception("file not found")
    for b in read_file_byte(filename):
        print(binascii.hexlify(b), end='')


def read_file_byte(filename):
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while True:
            byte = file.read(1)
            if byte:
                yield byte
            else:
                break


if __name__ == "__main__":
    main()
