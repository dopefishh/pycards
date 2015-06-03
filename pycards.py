import os
import sqlite3


__version__ = '0.1'


def list_decks(ddir, **kwargs):
    db = Database(os.path.join(ddir, 'pycards.db'))
    return db.list_decks()


def load_from_file(ddir, load_from, ifile, **args):
    db = Database(os.path.join(ddir, 'pycards.db'))
    dbname = db.setup_deck(load_from)
    startid = 0
    with open(ifile, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line[0] != '#':
                a, b = line.split('\t')
                startid += 1
                db.add_word(dbname, startid, a, b)
    return (True, '')


class Database:
    """
    Database object

    Decks table:
    id  | date_added | file_path | name

    words_NAME
    a | b | times | times_correct | box
    stats_NAME
    null
    """
    def __init__(self, filepath):
        self.sq = sqlite3.connect(filepath)
        c = self.sq.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS decks(
           id INTEGER,
           name TEXT UNIQUE)""")
        self.sq.commit()

    def setup_deck(self, name):
        """Sets up the tables. Returns a boolean succes code with an optional
        error message.
        """
        c = self.sq.cursor()
        dbname = 'words_{}'.format(name)
        _id = 0
        c.execute("""CREATE TABLE IF NOT EXISTS "{}" (
            id INTEGER UNIQUE,
            a TEXT,
            b TEXT,
            times INTEGER,
            times_correct INTEGER,
            box INTEGER)""".format(dbname))
        c.execute('INSERT OR IGNORE INTO decks values(0, "{}")'.format(name))
        self.sq.commit()
        return dbname

    def add_word(self, name, _id, a, b):
        c = self.sq.cursor()
        c.execute('INSERT OR IGNORE INTO {} values({},"{}","{}",0,0,0)'.format(
            name, _id, a, b))
        self.sq.commit()

    def list_decks(self):
        c = self.sq.cursor()
        return c.execute('SELECT * FROM decks')

    def close(self):
        self.sq.close()
