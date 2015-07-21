# -*- coding: utf-8 -*-

import sqlite3
import time
import logging

__version__ = '0.3'

LEITNER_BOXES = 5


def setup_logger(logfile, loglevel, **k):
    """Setup the logger

    arguments:
    logfile  - file to log to, None for stdout
    loglevel - level to log in
    """
    f = '%(levelno)s\t%(lineno)d\t%(asctime)s\t%(message)s'
    if logfile is None:
        logging.basicConfig(format=f, level=loglevel)
    else:
        logging.basicConfig(format=f, filename=logfile, level=loglevel)
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
    q = 'CREATE TABLE IF NOT EXISTS decks '\
        '(date TEXT, name TEXT UNIQUE, times INTEGER)'
    logging.info('Creating decks table')
    logging.debug('With query: {}'.format(q))
    c.execute(q)
    return sq, sq.cursor()


def close_db(database):
    database.commit()
    database.close()


def get_word_db(name):
    return '"words_{}"'.format(name)


def list_decks(database, deckname, **k):
    """List the decks optionally with their entries

    arguments:
    database - filepath for the sqlite database file
    deckname - name of the deck to list, if None all decks are shown

    returns: [deck]
        where deck = {name, date_added, entries}
        where entries = [(a, b, times, times_correct, box)]
    """
    logging.info('list decks... with name: {}'.format(deckname))
    sq, c = get_db(database)
    decks = []
    q = 'SELECT rowid, name, date FROM decks'
    logging.info('getting deck information')
    logging.debug('with query: {}'.format(q))
    datenames = list(c.execute(q))
    for id_, name, date in datenames:
        if not deckname or deckname == name:
            decks.append({'name': name, 'date_added': float(date),
                          'entries': []})
            q = 'SELECT * FROM {}'.format(get_word_db(id_))
            logging.info('getting entries information')
            logging.debug('with query: {}'.format(q))
            for entry in c.execute(q):
                decks[-1]['entries'].append(entry)
    close_db(sq)
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
    q = 'INSERT OR IGNORE INTO decks (date, name, times) values(?,?,0)'
    logging.info('inserting info in deck table')
    logging.debug('with query: {}'.format(q))
    c.execute(q, (time.time(), deckname))

    dbname = get_word_db(c.lastrowid)
    q = 'CREATE TABLE IF NOT EXISTS {} (a TEXT, b TEXT,'\
        'times INTEGER, times_correct INTEGER, box INTEGER)'.format(dbname)
    logging.info('creating deck table')
    logging.debug('with query: {}'.format(q))
    c.execute(q)

    logging.info('inserting from {}'.format(lines))
    for line in lines:
        line = line.strip()
        if line and line[0] != '#':
            a, b = line.split('\t')
            q = ('INSERT OR IGNORE INTO {} (a, b, times, times_correct, box) '
                 'values(?,?,0,0,1)').format(dbname)
            logging.debug('inserting entry\nwith query: {}'.format(q))
            c.execute(q, (a, b))
    sq.commit()
    sq.close()


def remove_deck(database, deckname, **k):
    """Remove a deck from the database

    arguments:
    database - filepath for the sqlite database file
    deckname - name of the deck to load in in

    returns: number of decks removed
    """
    logging.info('remove deck...')
    sq, c = get_db(database)
    q = 'SELECT rowid FROM decks WHERE name = ?'
    logging.info('finding matching tables')
    logging.info('with query: {}'.format(q))

    num = 0
    for (id_,) in list(c.execute(q, (deckname,))):
        q = 'DROP TABLE {}'.format(get_word_db(id_))
        logging.info('removing deck table: {}'.format(id_))
        logging.debug('with query: {}'.format(q))
        c.execute(q)
        q = 'DELETE FROM decks WHERE rowid={}'.format(id_)
        logging.info('removing deck entry: {}'.format(id_))
        logging.debug('with query: {}'.format(q))
        c.execute(q)
        num += 1
    sq.commit()
    sq.close()
    return num


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
    decks = list_decks(database, deckname, **k)
    deck = [d for d in decks if d['name'] == deckname]
    if not deck:
        logging.warning('deck not found')
    else:
        for entry in deck[0]['entries']:
            if entry:
                s = '{}\t{}\n'.format(entry[0], entry[1])
                logging.debug('yielding: {}'.format(s))
                yield s


class Session:
    def __init__(self, database, inverse, random, leitner, deckname):
        self.sq, self.c = get_db(database)
        self.entries = []
        self.cur = None

        q = 'SELECT rowid, times FROM decks WHERE name = ?'
        logging.info('finding deck with name: {}'.format(deckname))
        logging.debug('with query: {}'.format(q))
        deck = list(self.c.execute(q, (deckname,)))
        logging.info('found: {}'.format(deck))
        times = 0
        if not deck:
            logging.warning('No deck with that name')
            return
        else:
            rowid, times = deck[0]

        self.deckdb = get_word_db(rowid)
        q = 'SELECT rowid, {}, times, times_correct, box FROM {}'.format(
            'b, a' if inverse else 'a, b', self.deckdb)
        if leitner:
            q += ' WHERE box = 0'
            for i in range(1, 5):
                if times % i == 0:
                    q += ' OR box = {}'.format(i)
        if random:
            logging.info('randomize questions...')
            q += ' ORDER BY Random()'
        logging.debug('with query: {}'.format(q))
        self.entries += list(self.c.execute(q))
        logging.debug('entries testing: {}'.format(self.entries))
        logging.info('incrementing times column')
        q = 'UPDATE decks SET times=? WHERE rowid=?'
        logging.debug('with query: {}'.format(q))
        self.c.execute(q, (times+1, rowid))

    def __iter__(self):
        return self

    def __next__(self):
        if self.entries:
            self.cur = self.entries.pop(0)
            return self.cur[1]
        else:
            logging.info('no entries left, closing database')
            close_db(self.sq)
            raise StopIteration

    def answer_current(self, answer):
        if self.cur is None:
            logging.warning('Nothing to be answered, nothing has been asked')
        self.answer = self.cur[2]
        logging.info('comparing "{}" with "{}"'.format(answer, self.answer))
        print(self.cur)

        correct = answer == self.answer
        if correct:
            p = (self.cur[3]+1, self.cur[4]+1,
                 min(self.cur[5]+1, LEITNER_BOXES), self.cur[0])
        else:
            p = (self.cur[3]+1, self.cur[4],
                 max(self.cur[5]-1, 0), self.cur[0])

        logging.info('updating word')
        q = 'UPDATE {} SET times=?, times_correct=?, box=? WHERE rowid=?'.\
            format(self.deckdb)
        logging.debug('with query: {}'.format(q))
        self.c.execute(q, p)
        self.cur = None
        return correct


def session(database, deckname, inverse, random, leitner, **k):
    """Start a session

    arguments:
    database - filepath for the sqlite database file
    deckname - name of the deck to list, if None all decks are shown
    inverse  - flag for inversing question and answer
    random   - flag for randomizing questions
    leitner  - flag for using leitner system.

    returns: Session object
    """
    logging.info('starting session')
    return Session(database, inverse, random, leitner, deckname)
