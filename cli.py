#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import pycards
import logging
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='which')

    parser.add_argument('-d', '--database', default='~/.pycards/pycards.db',
                        help='Specify a custom database file. If not given ~/.'
                        'pycards/pycards.db is used.')
    parser.add_argument('-l', '--loglevel', default='SILENT',
                        choices=['INFO', 'DEBUG', 'SILENT'], help='Specify a c'
                        'ustom loglevel. If not given SILENT is used.')
    parser.add_argument('-f', '--logfile', default=None, help='Specify a log f'
                        'ile location. If not given stdout is used.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(pycards.__version__))
    parser.set_defaults(which='all')

    list_parser = subparsers.add_parser(
        'list', help='Show one or more decks from the database')
    list_parser.add_argument('deckname', nargs='?', help='name of the deck to '
                             'print. If not given, all decks will be printed.')
    list_parser.add_argument('-e', '--show-entries', action='store_true',
                             help='Flag to print all the individual entries.')
    list_parser.set_defaults(which='list')
    list_parser.required = True

    load_parser = subparsers.add_parser(
        'load', help='Load a deck from a file into a database.')
    load_parser.add_argument('-e', '--encoding',
                             default=sys.getdefaultencoding(),
                             help='Encoding to read the file/stream in.')
    load_parser.add_argument(
        'deckname', help='Name of the deck to load the entries in.')
    load_parser.add_argument('filepath', nargs='?', help='Location to load the'
                             ' entries from. If not given stdin is used.')
    load_parser.set_defaults(which='load')
    load_parser.required = True

    remove_parser = subparsers.add_parser(
        'remove', help='Remove a deck from the database.')
    remove_parser.add_argument('deckname', help='Name of the deck to remove.')
    remove_parser.set_defaults(which='remove')
    remove_parser.required = True

    export_parser = subparsers.add_parser(
        'export', help='Export a deck from the database.')
    export_parser.add_argument('deckname', help='Name of the deck to export.')
    export_parser.add_argument('filepath', nargs='?', help='Location to export'
                               ' to. If not given stdout is used.')
    export_parser.set_defaults(which='export')
    export_parser.required = True

    session_parser = subparsers.add_parser(
        'session', help='Run a session with a deck')
    session_parser.add_argument('deckname', help='name of the deck')
    session_parser.add_argument('-l', '--leitner', action='store_true',
                                help='Use the leitner system.')
    session_parser.add_argument('-r', '--random', action='store_true',
                                help='Randomize the questions.')
    session_parser.add_argument('-i', '--inverse', action='store_true',
                                help='Inverse the question and the answer.')
    session_parser.set_defaults(which='session')
    session_parser.required = True

    pargs = parser.parse_args()
    args = {}
    args.update(vars(pargs))
    args['database'] = os.path.abspath(os.path.expanduser(args['database']))

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
            print('date_added : {}'.format(time.strftime(
                '%x %X', time.localtime(deck['date_added']))))
            print('num_entries: {}'.format(len(deck['entries'])))
            if args['show_entries']:
                print('entries: (a,b,times,times_correct,box)\n{}'.format(
                    '\n'.join(map(str, deck['entries']))))
            print()
    elif args['which'] == 'load':
        if not args['filepath'] or args['filepath'] == '-':
            fin = sys.stdin
        else:
            fin = open(args['filepath'], 'r', encoding=args['encoding'])
        pycards.load_from_file(fin, **args)
        if fin != sys.stdin:
            fin.close()
    elif args['which'] == 'remove':
        print('Decks removed: {}'.format(pycards.remove_deck(**args)))
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
        ses = pycards.session(**args)
        for s in ses:
            answer = input(s + ': ')
            if ses.answer_current(answer):
                print('correct!')
            else:
                print('incorrect, it had to be: "{}"'.format(ses.answer))
    else:
        parser.print_help()
