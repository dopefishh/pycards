import dbm

class Database:
    def __init__(self, filepath):
        self.dbmob = dbm.open(filepath, 'c')

    def list_decks(self):
        print(dir(self.dbmob))
        print(self.dbmob.keys())

    def close(self):
        self.dbmob.close()
