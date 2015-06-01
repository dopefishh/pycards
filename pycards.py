import os
import sqlite3


__version__ = '0.1'


def list_decks(ddir, **kwargs):
    db = Database(os.path.join(ddir, 'pycards.db'))
    return db.list_decks()


def load_from_file(ddir, load_from, ifile, **args):
    db = Database(os.path.join(ddir, 'pycards.db'))
    return db.setup_deck(load_from)


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
        try:
            c.execute("""CREATE TABLE decks(
                id INTEGER,
                file_path TEXT,
                name TEXT)""")
        except sqlite3.OperationalError as e:
            if e.args != ('table decks already exists',):
                raise e
        self.sq.commit()

    def setup_deck(self, name):
        """Sets up the tables. Returns a boolean succes code with an optional
        error message.
        """
        c = self.sq.cursor()
        try:
            c.execute("""CREATE TABLE "words_{}" (
                id INTEGER,
                a TEXT,
                b TEXT,
                times INTEGER,
                times_correct INTEGER,
                box INTEGER)""".format(name))
        except sqlite3.OperationalError as e:
            if ('table "{}" already exists'.format(name),) != e.args:
                return (False, 'Deck with that name already exists')
            else:
                raise e
        self.sq.commit()
        return (True, '')

    def add_words(self, name, _id, a, b):
        c = self.sq.cursor()
        c.execute('INSERT INTO "words_{}" (?,?,?,0,0,0)'.format(name),
                  (name, _id, a, b))

    def list_decks(self):
        c = self.sq.cursor()
        return c.execute('SELECT * FROM decks')

    def close(self):
        self.sq.close()
