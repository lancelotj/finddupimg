#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
from finddup import print_err


def main(args):
    hash_dict = json.loads(args.input.read())

    def oprint(content):
        print(content, file=args.output)

    oprint('<html><body>\n')

    dup_count = 0
    for key, group in hash_dict.items():
        count = len(group)
        if count > 1:
            dup_count += count
            oprint('<hr/>')
            for info in group:
                oprint('<div><img width="150px" src="file://%(path)s" /> Path: %(path)s Size: %(size)s</div>' % info)

    oprint('</body></html>')
    print_err('Total %s images. %s duplictes' % (len(hash_dict), dup_count))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=('Looking up a director to see if there are duplicated file'))
    parser.add_argument(
        '-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
        help='input')
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
        help='output')
    parser.add_argument(
        '-f', '--format', choice=('html', 'report'), default='report',
        help='format')

    main(parser.parse_args())
