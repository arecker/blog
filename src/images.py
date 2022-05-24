import argparse

from . import lib

parser = argparse.ArgumentParser()
parser.add_argument('--dir-www', required=True)

if __name__ == '__main__':
    lib.configure_logging()
    args = parser.parse_args()
    lib.scan_images(args.dir_www)
