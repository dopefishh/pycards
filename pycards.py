import os
import sqlite3
import time
import logging

__version__ = '0.1'

def setup_logger(logfile, loglevel, **k):
    """Setup the logger

    arguments:
    logfile : file to log to, None for stdout
    loglevel: level to log in
    """
    if logfile:
        logging.basicConfig(filename=logfile, level=loglevel)
    logging.basicConfig(level=loglevel)
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


def list_decks(database, show_entries, **k):
    """List the decks optionally with their entries

    arguments:
    database     - filepath for the sqlite database file
    show_entries - flag to enable listing the individial entries
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
        decks.append({'name': name, 'date_added': date, 'entries': []})
        q = 'SELECT * FROM {}'.format(get_word_db(name))
        logging.info('getting entries information')
        logging.debug('with query: {}'.format(q))
        for entry in c.execute(q):
            decks[-1]['entries'].append(entry)
    sq.close()
    return decks


def load_from_file(database, filepath, deckname, **k):
    """Import a deck from a file

    arguments:
    database - filepath for the sqlite database file
    filepath - filepath for the deck file
    deckname - name of the deck to load in in
    """
    logging.info('load from file...')
    sq, c = get_db(database)
    dbname = get_word_db(deckname)
    _id = 0
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
    with open(filepath, 'r') as f:
        logging.info('opened {}'.format(f))
        for line in f:
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
