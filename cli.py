#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time
import stat
import os
import pycards
import logging


def parse_args():
    pars = argparse.ArgumentParser()
    subparsers = pars.add_subparsers(dest='which')

    # Global options
    pars.add_argument(
        '-d', '--database', default='~/.pycards/pycards.db',
        help='Specify a custom database file. '
        'If not given ~/.pycards/pycards.db is used.')
    pars.add_argument(
        '-l', '--loglevel', default='SILENT',
        choices=['INFO', 'DEBUG', 'SILENT'],
        help='Specify a custom loglevel. '
        'If not given SILENT is used.')
    pars.add_argument(
        '-f', '--logfile', default=None,
        help='Specify a log file location. '
        'If not given stdout is used.')
    pars.add_argument(
        '--version', action='version',
        version='%(prog)s ' + pycards.__version__)

    # List subparser
    list_parser = subparsers.add_parser(
        'list', help='Show one or more decks from the database')
    list_parser.add_argument(
        'deckname', nargs='*',
        help='Name of the deck to print. '
        'If not given, all decks will be printed.')
    list_parser.add_argument(
        '-e', '--show-entries', action='store_true',
        help='Flag to print all the individual entries.')

    # Load subparser
    load_parser = subparsers.add_parser(
        'load', help='Load a deck from a file into a database.')
    load_parser.add_argument(
        'deckname',
        help='Name of the deck to load the entries in.')
    load_parser.add_argument(
        'filepath', nargs='?', default='-',
        type=argparse.FileType('r'),
        help='Location to load the entries from. '
        'If not given stdin is used.')

    # Remove subparser
    remove_parser = subparsers.add_parser(
        'remove', help='Remove decks from the database.')
    remove_parser.add_argument(
        'deckname', nargs='+',
        help='Name of the deck to remove.')

    # Export subparser
    export_parser = subparsers.add_parser(
        'export', help='Export a deck from the database.')
    export_parser.add_argument(
        '-f', '--filepath', nargs='?', default='-',
        type=argparse.FileType('w'),
        help='Location to export to. '
        'If not given stdout is used.')
    export_parser.add_argument(
        'deckname', nargs='+',
        help='Name of the deck to export.')

    # Session subparser
    session_parser = subparsers.add_parser(
        'session', help='Run a session with a deck')
    session_parser.add_argument(
        'deckname', help='name of the deck')
    session_parser.add_argument(
        '-l', '--leitner', action='store_true',
        help='Use the leitner system.')
    session_parser.add_argument(
        '-r', '--random', action='store_true',
        help='Randomize the questions.')
    session_parser.add_argument(
        '-i', '--inverse', action='store_true',
        help='Inverse the question and the answer.')

    pargs = pars.parse_args()
    if pargs.which is None:
        pars.print_usage()
        exit(1)
    return pargs


def pfclose(fp):
    """Close a file object, but only if it's a real file

    Arguments:
    fp - file object
    """
    logging.debug('closing: {}'.format(fp))
    if stat.S_ISREG(os.fstat(fp.fileno()).st_mode):
        logging.debug('{} is regular file, closing...'.format(fp))
        fp.close()

if __name__ == '__main__':
    args = parse_args()
    db = os.path.abspath(os.path.expanduser(args.database))

    pycards.setup_logger(args.logfile, args.loglevel)
    if args.which == 'list':
        print('\t'.join(['name', 'date added', 'entries']))
        for deck in pycards.list_decks(db, args.deckname):
            print('\t'.join([
                deck['name'],
                time.strftime('%x %X', time.localtime(deck['date_added'])),
                str(len(deck['entries']))]))
            if args.show_entries:
                maxa = max(10, max((len(a[0]) for a in deck['entries'])))
                maxb = max(10, max((len(a[1]) for a in deck['entries'])))
                formats = '{{:{}}} {{:{}}} {{:5}} {{:7}}'.format(
                    maxa, maxb)
                print(formats.format('Question', 'Answer', 'Times', 'Correct'))
                for a, b, times, correct, _ in deck['entries']:
                    print(formats.format(a, b, times, correct))

    elif args.which == 'load':
        pycards.load_from_file(args.filepath, db, args.deckname)
        pfclose(args.filepath)
    elif args.which == 'remove':
        for deck in args.deckname:
            print('decks removed for {}: {}'.format(
                deck, pycards.remove_deck(db, deck)))
    elif args.which == 'export':
        for deckname in args.deckname:
            for line in pycards.export_deck(db, deckname):
                args.filepath.write(line)
        pfclose(args.filepath)
    elif args.which == 'session':
        ses = pycards.session(
            db, args.deckname, args.inverse, args.random, args.leitner)
        try:
            for s in ses:
                answer = input(s + ':\n')
                if ses.answer_current(answer):
                    print('correct!')
                else:
                    print('incorrect, it had to be: "{}"'.format(ses.answer))
            stats = ses.write_stats()
        except KeyboardInterrupt:
            stats = ses.write_stats(False)
        print('\nFinished\n\nGrade: {}'.format(stats))
