#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import pycards
import logging
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('-c', '--config', default='~/.pycards/config',
                        help='custom config file')
    parser.add_argument('-d', '--database', default='~/.pycards/pycards.db',
                        help='custom database file')
    parser.add_argument('-l', '--loglevel', default='SILENT',
                        choices=['INFO', 'DEBUG', 'SILENT'],
                        help='set loglevel to INFO DEBUG or SILENT')
    parser.add_argument('-f', '--logfile', default=None,
                        help='log file location')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(pycards.__version__))
    parser.set_defaults(which='all')

    list_parser = subparsers.add_parser('list', help='show decks or deck')
    list_parser.add_argument('deckname', nargs='?',
                             help='name of the deck to show')
    list_parser.add_argument('-e', '--show-entries', action='store_true',
                             help='also print all entries')
    list_parser.set_defaults(which='list')

    load_parser = subparsers.add_parser('load', help='load a file as deck')
    load_parser.add_argument('deckname', help='name for the deck')
    load_parser.add_argument('filepath', nargs='?', help='file to load from')
    load_parser.set_defaults(which='load')

    remove_parser = subparsers.add_parser('remove', help='remove a deck')
    remove_parser.add_argument('deckname', help='name of the deck')
    remove_parser.set_defaults(which='remove')

    export_parser = subparsers.add_parser('export', help='export a deck')
    export_parser.add_argument('deckname', help='name of the deck')
    export_parser.add_argument('filepath', nargs='?', help='file to export to')
    export_parser.set_defaults(which='export')

    session_parser = subparsers.add_parser('session', help='practise session')
    session_parser.add_argument('deckname', help='name of the deck')
    session_parser.add_argument('-s', '--system', default='order',
                                choices=['order', 'random', 'leitner'],
                                help='set questioning system')
    session_parser.add_argument('-i', '--inverse', action='store_true',
                                help='inverse the question and the answer')
    session_parser.set_defaults(which='session')

    pargs = parser.parse_args()
    args = {}
    with open(pargs.config, 'r') as cin:
        for line in [l.strip() for l in cin]:
            if line and line[0] != '#':
                items = line.split('=')
                if len(items) > 1:
                    args[items[0].strip()] = '='.join(items[1:]).strip()
                else:
                    print('Couldn\'t parse "{}"\nSkipping...\n'.format(line))
    args.update(vars(pargs))
    args['database'] = os.path.abspath(os.path.expanduser(args['database']))
    args['config'] = os.path.abspath(os.path.expanduser(args['config']))

    try:
        os.makedirs(os.path.dirname(args['database']))
    except OSError as e:
        if e.errno != 17:
            raise e

    args['loglevel'] = logging.INFO if args['loglevel'] == 'INFO' else\
        logging.DEBUG if args['loglevel'] == 'DEBUG' else logging.WARNING

    pycards.setup_logger(**args)

    if args['which'] == 'list':
        for deck in pycards.list_decks(**args):
            print('name       : {}'.format(deck['name']))
            print('date_added : {}'.format(deck['date_added']))
            print('num_entries: {}'.format(len(deck['entries'])))
            if args['show_entries']:
                print('entries: (id,a,b,times,times_correct,box)\n{}'.format(
                    '\n'.join(map(str, deck['entries']))))
            print()
    elif args['which'] == 'load':
        if not args['filepath'] or args['filepath'] == '-':
            fin = sys.stdin
        else:
            fin = open(args['filepath'], 'r')
        pycards.load_from_file(fin, **args)
        if fin != sys.stdin:
            fin.close()
    elif args['which'] == 'remove':
        pycards.remove_deck(**args)
    elif args['which'] == 'export':
        if not args['filepath'] or args['filepath'] == '-':
            fout = sys.stdout
        else:
            fout = open(args['filepath'], 'w')
        for line in pycards.export_deck(**args):
            fout.write(line)
        if fout != sys.stdout:
            fout.close()
    elif args['which'] == 'session':
        session = pycards.session(**args)
        for s in session:
            answer = input(s + ': ')
            print(session.answer_current(answer))
    else:
        parser.print_help()
