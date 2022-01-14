from sqlite3 import connect
from config import config

from secrets import token_hex


class DataBase:

    def __init__(self):
        self.connexion = None
        self.create()

    def create(self):

        new = False
        try: open(config["DATABASE"]).close()
        except IOError: new = True

        self.connexion = connect(config["DATABASE"])
        cursor = self.connexion.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS api_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, permission TEXT, key TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, nick TEXT, password TEXT, permission TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS qcms (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS questions (id TEXT PRIMARY KEY, name TEXT, possibilities TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS possibilities (id TEXT PRIMARY KEY, valid INTEGER, text TEXT)")

        if new:
            print('New database created ! Superkey is going to be created...')
            superkey = token_hex(config["TOKEN_SECURITY"]["superkey"])
            cursor.execute("INSERT INTO api_keys (permission, key) VALUES (?, ?)", ('super', superkey))
            print(f'Superkey created ! Please save it : {superkey}')

        self.connexion.commit()

    def __enter__(self):
        return self.connexion.cursor()

    def __exit__(self, _1, _2, _3):
        self.connexion.commit()
