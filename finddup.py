#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from collections import defaultdict
from hashlib import md5
from argparse import ArgumentParser


def get_md5(dup):
    with open(dup) as f:
        m = md5()
        #f.seek(-1000, os.SEEK_END)
        m.update(f.read())
        return m.digest()


if __name__ == '__main__':
    parser = ArgumentParser(description=('Looking up a director to see if there are duplicated file'))
    parser.add_argument('dirs', nargs='+', help='Target directories')
    parser.add_argument('-v', '--verbose', action='count', help='More information')

    args = parser.parse_args()
    src_dict = defaultdict(list)
    for path in args.dirs:
        for root, dirs, files in os.walk(path):
            for f in files:
                fext = os.path.splitext(f)[1].lower()
                if fext in set(('.jpg', '.jpeg', '.nef', '.mov', '.png', '.gif')):
                    fname = os.path.join(root, f)
                    size = os.path.getsize(fname)
                    src_dict[size].append(fname)
    if args.verbose:
        sys.stderr.write('%d files processed\n' % len(src_dict))

    hashes = defaultdict(list)
    for size, dups in src_dict.iteritems():
        if len(dups) > 1:
            if args.verbose:
                print '\t'.join(dups)
            for dup in dups:
                hashes[get_md5(dup)].append(dup)

    count = 0
    for code, dups in hashes.iteritems():
        if len(dups) > 1:
            count += 1
            print '\t'.join('"%s"' % dup for dup in sorted(dups))

    if args.verbose:
        sys.stderr.write('%d duplicated files found.\n' % count)
