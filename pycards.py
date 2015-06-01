import os
import database

__version__ = '0.1'

def list_decks(ddir, **kwargs):
    db = database.Database(os.path.join(ddir, 'pycards.db'))
    decks = db.list_decks()
    return decks
