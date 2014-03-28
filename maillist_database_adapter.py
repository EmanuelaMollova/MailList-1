from maillist import MailList
from maillist_db_factory import MailListDataBaseFactory
import sqlite3


class MailListDataBaseAdapter():
    def __init__(self, db_name, mail_list=None):
        self.db_name = db_name
        self.mail_list = mail_list
        self._connection = self._create_connection(self.db_name)
        self.factory=MailListDataBaseFactory(self._connection)

    def _create_connection(self, db_name):
        return sqlite3.connect(db_name)

    def _get_cursor(self):
        return self._connection.cursor()

    def _commit_connection(self):
        self._connection.commit()

    def _close_connection(self):
        self._connection.close()

    def save(self):
        c=self._get_cursor()
        c.execute("INSERT INTO maillist(name) VALUES(?)",(self.mail_list.get_name(),))
        subscribers = self.mail_list.get_subscribers()
        c=self._get_cursor()
        ids=c.execute("SELECT subscriber_id FROM subscribers").fetchall()
        subscriber_max_id=0
        if ids != []:
            subscriber_max_id=ids[len(ids)-1][0]
        for subs in subscribers:
            c.execute("INSERT INTO subscribers(name, email) VALUES(?,?)",(subs[0],subs[1]))
            c.execute("INSERT INTO maillists_to_subscribers(maillist_id, subscriber_id) VALUES(?,?)",(self.mail_list.get_id(),subscriber_max_id+1))
            subscriber_max_id+=1
        self._commit_connection()
    def load(self,list_id):
        c=self._get_cursor()
        list_name=c.execute("SELECT name FROM maillist WHERE maillist_id=?",str(list_id)).fetchall()
        maillist = self.factory.create(list_name[0][0])
        ids_of_subscribers=c.execute("SELECT subscriber_id FROM maillists_to_subscribers WHERE maillist_id=?",str(list_id)).fetchall()
        for id in ids_of_subscribers:
            subscriber=c.execute("SELECT name, email FROM subscribers WHERE subscriber_id=?",str(id[0])).fetchall()
            maillist.add_subscriber(subscriber[0][0],subscriber[0][1])
        return maillist








        
