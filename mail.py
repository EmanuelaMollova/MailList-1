from commandparser import CommandParser
from maillist_database_adapter import MailListDataBaseAdapter
from maillist_db_factory import MailListDataBaseFactory
from glob import glob
from os.path import basename
import sys
import sqlite3


class MailListProgram():
    """docstring for MailListProgram"""
    def __init__(self):
        self.db_path = "maillist"
        self.conn=sqlite3.connect(self.db_path)
        self.create_table(self.conn.cursor())
        self.factory = MailListDataBaseFactory(self.conn)
        self.cp = CommandParser()
        self.lists = {}
        self._load_initial_state()
        self._init_callbacks()
        self._loop()
    def create_table(self,cursor):
        cursor.execute(''' CREATE TABLE IF NOT EXISTS maillist
            (maillist_id INTEGER PRIMARY KEY, name text)''')
        cursor.execute(''' CREATE TABLE IF NOT EXISTS subscribers
            (subscriber_id INTEGER PRIMARY KEY, name text, email text)''')
        cursor.execute(''' CREATE TABLE IF NOT EXISTS maillists_to_subscribers
            (maillist_id int, subscriber_id int)''')
    def create_list_callback(self, arguments):
        name = " ".join(arguments)

        maillist = self.factory.create(name)
        maillist_adapter = MailListDataBaseAdapter(self.db_path,maillist)
        maillist_adapter.save()
        self.lists[maillist.get_id()] = (maillist, maillist_adapter)

    def add_subscriber_callback(self, arguments):
        list_id = int("".join(arguments))
        if not list_id in self.lists:
            print("Id is incorrect, try again.")
        else:
            name = input("name>")
            email = input("email>")

            self.lists[list_id][0].add_subscriber(name, email)
            #TODO: function which add subscriber into tables

    def show_lists_callback(self, arguments):
        for list_id in self.lists:
            current_list = self.lists[list_id][0]
            print("[{}] {}".format(list_id,
                                   current_list.get_name()))

    def show_list_callback(self, arguments):
        list_id = int("".join(arguments))

        if list_id in self.lists:
            subscribers = self.lists[list_id][0].get_subscribers()
            for s in subscribers:
                print("{} - {}".format(s[0], s[1]))
        else:
            print("List with id <{}> was not found".format(list_id))

    def exit_callback(self, arguments):
        sys.exit(0)

    def _load_initial_state(self):
        c=self.conn;
        ids_of_maillists=c.execute("SELECT maillist_id FROM maillist").fetchall()
        for id in ids_of_maillists:
            adapter=MailListDataBaseAdapter("maillist")
            maillist=adapter.load(id[0])
            self.lists[id[0]]=(maillist,adapter)
    def _init_callbacks(self):
        self.cp.on("create", self.create_list_callback)
        self.cp.on("add", self.add_subscriber_callback)
        self.cp.on("show_lists", self.show_lists_callback)
        self.cp.on("show_list", self.show_list_callback)
        self.cp.on("exit", self.exit_callback)
        # TODO - implement the rest of the callbacks

    def _loop(self):
        while True:
            command = input(">")
            self.cp.take_command(command)


if __name__ == '__main__':
    MailListProgram()
