#!/usr/bin/python

import argparse
import os
import pycards
import logging

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
    load_parser.add_argument('filepath', help='file to load from. - for stdin')
    load_parser.add_argument('deckname', help='name for the deck')
    load_parser.set_defaults(which='load')

    session_parser = subparsers.add_parser('session', help='practise session')
    session_parser.add_argument('deckname', help='name of the deck')
    session_parser.set_defaults(which='session')

    remove_parser = subparsers.add_parser('remove', help='remove a deck')
    remove_parser.add_argument('deckname', help='name of the deck')
    remove_parser.set_defaults(which='remove')

    args = vars(parser.parse_args())
    args['database'] = os.path.abspath(os.path.expanduser(args['database']))
    args['config'] = os.path.abspath(os.path.expanduser(args['config']))

    with open(args['config'], 'r') as cin:
        for line in [l.strip() for l in cin]:
            if line and line[0] != '#':
                items = line.split('=')
                if len(items) > 1:
                    args[items[0]] = '='.join(items[1:])
                else:
                    print('Couldn\'t parse "{}"\nSkipping...\n'.format(line))

    try:
        os.makedirs(os.path.dirname(args['database']))
    except OSError as e:
        if e.errno != 17:
            raise e

    if args['loglevel'] == 'INFO':
        args['loglevel'] = logging.INFO
    elif args['loglevel'] == 'DEBUG':
        args['loglevel'] = logging.DEBUG
    elif args['loglevel'] == 'SILENT':
        args['loglevel'] = logging.WARNING

    pycards.setup_logger(**args)

    if args['which'] == 'list':
        for deck in pycards.list_decks(**args):
            print('name      : {}'.format(deck['name']))
            print('date_added: {}'.format(deck['date_added']))
            if args['show_entries']:
                print('entries: (id,a,b,times,times_correct,box)\n{}'.format(
                    '\n'.join(map(str, deck['entries']))))
            print()
    elif args['which'] == 'load':
        pycards.load_from_file(**args)
    elif args['which'] == 'remove':
        print('remove' + str(args))
    elif args['which'] == 'session':
        print('session' + str(args))
    else:
        parser.print_help()
