import sqlite3


class Database:
    """Classe permettant d'interagir avec la base de données."""

    def __init__(self):
        self.connection = None

    def connect(self):
        """Établie une connexion avec la base de données dans le but d'exécuter
        des requêtes

        return:
            La connexion établie. Un objet de type 'Connection' qui exécutera
            les requêtes SQL.
        """

        if self.connection is None:
            self.connection = sqlite3.connect('./database.db')
        return self.connection

    def disconnect(self):
        """Déconnecte la base de données."""

        if self.connection is not None:
            self.connection.close()
            self.connection = None
