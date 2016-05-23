#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import imagehash
import argparse
import collections
from operator import itemgetter

from collections import defaultdict
from PIL import Image, ExifTags


def print_err(content):
    print(content, file=sys.stderr)


def get_file_size(file_name):
    return os.path.getsize(file_name)


def get_image_size(img):
    return "{} x {}".format(*img.size)


def is_image(thefile):
    fname, ext = os.path.splitext(thefile)
    return not fname.startswith('.') and ext.lower() in set(['.jpg', '.jpeg', '.gif', '.png', '.tiff'])

def walk_images(path):
    for root, dirs, files in os.walk(path):
        dirs[:] = filter(lambda d: not d.startswith('.'), dirs)
        for fname in files:
            if is_image(fname):
                path = os.path.join(root, fname)
                with Image.open(path) as img:
                    dup_info = {
                        'hash': str(imagehash.phash(img)),
                        'path': path,
                        'size': get_file_size(path),
                        'image_size': get_image_size(img),
                    }
                    yield dup_info



def main(args):
    dup_count = 0
    total = 0
    if args.existing:
        src_dict = defaultdict(list, json.load(args.existing))
    else:
        src_dict = defaultdict(list)

    try:
        for path in args.dirs:
            for dup_info in walk_images(path):
                total += 1
                print_err('Processing %s.' % dup_info['path'])
                src_dict[dup_info['hash']].append({
                    'path': dup_info['path'],
                    'size': dup_info['size'],
                    'image_size': dup_info['image_size'],
                })
    except KeyboardInterrupt:
        pass
    print_err('\n%d files processed.' % total)
    output = collections.OrderedDict((
        info[0], sorted(info[1], key=itemgetter('size'), reverse=True)
    ) for info in sorted(
        src_dict.items(),
        key=lambda d: len(d[1])))

    for hash_str, dups in output.items():
        count = len(dups)
        if count > 1:
            dup_count += count

    print(json.dumps(output, indent=2), file=args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            'Looking up a directory to see if there are duplicated file.'))
    parser.add_argument('dirs', nargs='+', help='Target directories')
    parser.add_argument(
        '-v', '--verbose', action='store_false', help='More information')
    parser.add_argument(
        '-e', '--existing', type=argparse.FileType('r'),
        default=None, help='Use this as existing hash table.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout, help='output')

    main(parser.parse_args())
