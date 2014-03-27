import sqlite3


class MailListDataBaseAdapter():
    def __init__(self, db_name, mail_list=None):
        self.db_name = db_name
        self.mail_list = mail_list
        self._connection = self._create_connection()

    def _create_connection(self, db_name):
        return sqlite3.connect(db_name)

    def _get_cursor(self):
        return self._connection.cursor()

    def _commit_connection(self):
        self._conncetion.commit()

    def _close_connection(self):
        self._conncetion.close()
