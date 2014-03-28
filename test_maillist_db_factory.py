import unittest
import sqlite3
from maillist_db_factory import MailListDataBaseFactory
from subprocess import call


class MailListDataBaseFactoryTest(unittest.TestCase):
	"""docstring for MailListFactoryTest"""

	def setUp(self):
		self.db_name="testtable"
		self.conn=sqlite3.connect(self.db_name)
		cursor=self.conn.cursor()
		
		cursor.execute(''' CREATE TABLE maillist
			(maillist_id INTEGER PRIMARY KEY, name text)''')
		cursor.execute(''' CREATE TABLE subscribers
			(subscriber_id INTEGER PRIMARY KEY, name text, email text)''')
		cursor.execute(''' CREATE TABLE maillists_to_subscribers
			(maillist_id INTEGER PRIMARY KEY, subscriber_id int)''')

		self.factory = MailListDataBaseFactory(self.conn)
	def test_init_id(self):
		self.assertEqual(1,self.factory.init_id(self.conn))
	def test_next_id(self):
		m1 = self.factory.create("Hack Bulgaria")
		c=self.conn.cursor()
		c.execute("INSERT INTO maillist(name) VALUES(?)",(m1.get_name(),))
		self.assertEqual(1, m1.get_id())
		c=self.conn.cursor()
		m2 = self.factory.create("Uni Sofia")
		c.execute("INSERT INTO maillist(name) VALUES(?)",(m2.get_name(),))
		self.assertEqual(2,m2.get_id())
		factory=MailListDataBaseFactory(self.conn)
		self.assertEqual(3,factory.next_id())

	def tearDown(self):
		call("rm " + self.db_name,shell=True)

if __name__ == '__main__':
	unittest.main()