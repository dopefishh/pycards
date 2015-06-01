#!/usr/bin/python

import argparse
import os
import database
import pycards

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='pycards: a python flashcard engine', usage="""
    start a session:
        %(prog)s [opts] entry-name
    import a file:
        %(prog)s -f filename
    list files in the database:
        %(prog)s -ls""")

    parser.add_argument('-c', '--config', default='~/.pycards/config',
                        help='location of the configuration file.')
    parser.add_argument('-d', '--ddir', default='~/.pycards',
                        help='location of the data directory.')
    parser.add_argument('-i', '--interface', choices=['cli', 'web'],
                        default='cli', help='type of interface.')
    parser.add_argument('-s', '--system', choices=['leit', 'random', 'order'],
                        default='random', help='type of flashcard system.')
    parser.add_argument('-o', action='store_true',
                        help='shortcut for --system order')
    parser.add_argument('-l', action='store_true',
                        help='shortcut for --system leitner')
    parser.add_argument('-r', action='store_true',
                        help='shortcut for --system random')

    parser.add_argument('-f', '--load-from',
                        help='load a file into the database.')
    parser.add_argument('-ls', '--list', action='store_true',
                        help='list decks in the database.')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(pycards.__version__))
    parser.add_argument('file', nargs='?', default='',
                        help='deck to play from the database')
    args = vars(parser.parse_args())

    with open(args['config'], 'r') as cin:
        for line in [l.strip() for l in cin]:
            if line and line[0] != '#':
                items = line.split('=')
                if len(items) > 1:
                    args[items[0]] = '='.join(items[1:])
                else:
                    print('Couldn\'t parse "{}"\nSkipping...\n'.format(line))

    args['ddir'] = os.path.abspath(os.path.expanduser(args['ddir']))
    args['config'] = os.path.abspath(os.path.expanduser(args['config']))
    args['file'] = os.path.abspath(os.path.expanduser(args['file']))

    try:
        os.makedirs(args['ddir'])
    except OSError as e:
        if e.errno != 17:
            raise e

    if args['list']:
        pycards.list_decks(**args)
    elif args['load_from']:
        print('loading file...')
    elif args['file']:
        print('playing deck...')
    else:
        parser.print_help()
