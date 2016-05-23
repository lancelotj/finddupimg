#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
from finddupimg import print_err
from send2trash import send2trash


def filter_dict(hash_dict):
    for key, group in hash_dict.items():
        if len(group) > 1:
            yield group


def fmt_report(hash_dict, print_out):
    dup_count = 0
    for group in filter_dict(hash_dict):
        dup_count += len(group) - 1
    print_err('Total %s images. %s duplictes' % (len(hash_dict), dup_count))


def fmt_html(hash_dict, print_out):
    print_out('<html><body>\n')
    for group in filter_dict(hash_dict):
        print_out('<hr/>')
        for info in group:
            print_out('<div><a href="%(path)s" target="_blank"><img width="150px" src="file://%(path)s" /></a> Path: %(path)s, Size: %(size)s, Image Size: %(image_size)s</div>' % info)
    print_out('</body></html>')


def fmt_trash(hash_dict, print_out):
    for group in filter_dict(hash_dict):
        for info in group[1:]:
            print_out('Send %s to trash...' % info['path'])
            send2trash(info['path'])


def main(args):
    hash_dict = json.loads(args.input.read())

    def print_out(content):
        print(content, file=args.output)

    {
        'report': fmt_report,
        'html': fmt_html,
        'trash': fmt_trash,
    }[args.format](hash_dict, print_out)


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
        '-f', '--format', choices=('html', 'report', 'trash'), default='report',
        help='format')

    main(parser.parse_args())
