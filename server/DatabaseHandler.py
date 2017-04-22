import sqlite3

class DatabaseHandler:

    def __init__(self, dbName):
        self._dbName = dbName

    def