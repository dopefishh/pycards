# -*- coding: utf-8 -*-

import sqlite3
import time
import logging
import random

__version__ = '0.1'


def setup_logger(logfile, loglevel, **k):
    """Setup the logger

    arguments:
    logfile : file to log to, None for stdout
    loglevel: level to log in
    """
    f = '%(levelno)s\t%(lineno)d\t%(asctime)s\t%(message)s'
    if logfile:
        logging.basicConfig(format=f, filename=logfile, level=loglevel)
    else:
        logging.basicConfig(format=f, level=loglevel)
    logging.debug('Logger initialized')


def get_db(database):
    """Helper function to start the database and initialize if necessary

    arguments:
    database - filepath for the sqlite databasae file

    returns: (sqlite-object, sqlite-cursor)
    """
    sq = sqlite3.connect(database)
    logging.debug('Connected with database at {}'.format(database))
    c = sq.cursor()
    q = 'CREATE TABLE IF NOT EXISTS decks (date TEXT, name TEXT UNIQUE)'
    logging.info('Creating decks table')
    logging.debug('With query: {}'.format(q))
    c.execute(q)
    return sq, sq.cursor()


def get_word_db(name):
    return '"words_{}"'.format(name)


def list_decks(database, deckname, **k):
    """List the decks optionally with their entries

    arguments:
    database     - filepath for the sqlite database file
    deckname     - name of the deck to list, if None all decks are shown

    returns: [deck]
        where deck = {name, date_added, entries}
        where entries = [(id, a, b, times, times_correct, box)]
    """
    logging.info('list decks...')
    sq, c = get_db(database)
    decks = []
    q = 'SELECT * FROM decks'
    logging.info('getting deck information')
    logging.debug('with query: {}'.format(q))
    for date, name in c.execute(q):
        if not deckname or deckname == name:
            decks.append({'name': name, 'date_added': date, 'entries': []})
            q = 'SELECT * FROM {}'.format(get_word_db(name))
            logging.info('getting entries information')
            logging.debug('with query: {}'.format(q))
            for entry in c.execute(q):
                decks[-1]['entries'].append(entry)
    sq.close()
    return decks


def load_from_file(lines, database, deckname, **k):
    """Import a deck from a file

    arguments:
    lines    - generator for lines of input
    database - filepath for the sqlite database file
    deckname - name of the deck to load in in
    """
    logging.info('load from file...')
    sq, c = get_db(database)
    dbname = get_word_db(deckname)
    q = 'CREATE TABLE IF NOT EXISTS {} (id INTEGER UNIQUE, a TEXT, b TEXT,'\
        'times INTEGER, times_correct INTEGER, box INTEGER)'.format(dbname)
    logging.info('creating deck table')
    logging.debug('with query: {}'.format(q))
    c.execute(q)
    q = 'INSERT OR IGNORE INTO decks values("{}", "{}")'.format(
        time.time(), deckname)
    logging.info('inserting info in deck table')
    logging.debug('with query: {}'.format(q))
    c.execute(q)

    startid = 0
    for line in lines:
        line = line.strip()
        if line and line[0] != '#':
            a, b = line.split('\t')
            startid += 1
            q = 'INSERT OR IGNORE INTO {} values({},"{}","{}",0,0,0)'.\
                format(dbname, startid, a, b)
            logging.debug('inserting entry\nwith query: {}'.format(q))
            c.execute(q)
    sq.commit()
    sq.close()


def remove_deck(database, deckname, **k):
    """Remove a deck from the database

    arguments:
    database - filepath for the sqlite database file
    deckname - name of the deck to load in in
    """
    logging.info('remove deck...')
    sq, c = get_db(database)
    q = 'DROP TABLE IF EXISTS {}'.format(get_word_db(deckname))
    logging.info('removing table {}'.format(deckname))
    logging.debug('with query: {}'.format(q))
    c.execute(q)
    q = 'DELETE FROM decks WHERE decks.name = "{}"'.format(deckname)
    logging.info('remove intry from decks table')
    logging.debug('with query: {}'.format(q))
    c.execute(q)
    sq.commit()
    sq.close()


def export_deck(database, deckname, **k):
    """Export a deck from the database

    arguments:
    database - filepath for the sqlite database file
    deckname - name of the deck to load in in

    yields: lines
    """
    logging.info('exporting deck...')
    sq, c = get_db(database)
    logging.info('getting deck information')
    decks = list_decks(database, **k)
    deck = [d for d in decks if d['name'] == deckname]
    if not deck:
        logging.warning('deck not found')
    else:
        for entry in deck[0]['entries']:
            if entry:
                s = '{}\t{}\n'.format(entry[1], entry[2])
                logging.debug('yielding: {}'.format(s))
                yield s

class Session:
    def __init__(self, system, inverse, entries, name, **k):
        self.name = name
        self.entries = entries
        self.inverse = inverse
        self.system = system
        self.current = None
        if self.system == 'random':
            logging.info('Shuffled entries for random mode')
            random.shuffle(self.entries)

    def __iter__(self):
        return self

    def __next__(self):
        if self.entries:
            if self.system == 'leitner':
                self.current = self.entries.pop(0)[1:3]
            else:
                self.current = self.entries.pop(0)[1:3]
            return self.current[self.get_question_index()]
        else:
            raise StopIteration

    def get_question_index(self):
        return 1 if self.inverse else 0

    def get_answer_index(self):
        return 0 if self.inverse else 1

    def answer_current(self, answer):
        if self.current == None:
            logging.warning('Nothing to be answered, nothing has been asked')
        correctanswer = self.current[self.get_answer_index()]
        logging.info('comparing {} with {}'.format(answer, correctanswer))
        correct = answer == correctanswer
        self.current = None
        return correct


def session(database, deckname, system, inverse, **k):
    logging.info('starting session')
    deck = list_decks(database, deckname)
    if not deck:
        logging.warning('deck not found')
    else:
        return Session(system, inverse, **deck[0])
