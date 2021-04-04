#!/usr/bin/env python3

import argparse
import os.path
import sys

import svgwrite
import toml

from parameters import *
from draw import draw_svg


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('files', metavar='definition-file', nargs='+',
                        help='TOML file(s) containing grid definitions.  Later files override earlier files.')
    args = parser.parse_args()

    for dfile in args.files:
        if not os.path.exists(dfile):
            print('"{}" does not exist.'.format(dfile), file=sys.stderr)
            exit(1)
    
    return args

def dict_merge(dest, source):
    """Merges source into dest and returns dest."""
    for k, v in source.items():
        if k in dest and isinstance(dest[k], dict) and isinstance(v, dict):
            dict_merge(dest[k], v)
        else:
            dest[k] = v
    return dest

def parse_definitions(files):
    result = {}
    for dfile in files:
        result = dict_merge(result, toml.load(dfile))
    return result


if __name__ == '__main__':
    args = parse_args()
    definitions = parse_definitions(args.files)
    parameters = Parameters(definitions)
    draw_svg(args.output, parameters)
