import unittest
import sqlite3
from subprocess import call
from maillist_database_adapter import MailListDataBaseAdapter
from maillist_db_factory import MailListDataBaseFactory

class MailistDataBaseAdapterTest(unittest.TestCase):
	def setUp(self):
		self.db_name="testtable"
		self.conn=sqlite3.connect(self.db_name)
		cursor=self.conn.cursor()
		cursor.execute(''' CREATE TABLE IF NOT EXISTS maillist
			(maillist_id INTEGER PRIMARY KEY, name text)''')
		cursor.execute(''' CREATE TABLE IF NOT EXISTS subscribers
			(subscriber_id INTEGER PRIMARY KEY, name text, email text)''')
		cursor.execute(''' CREATE TABLE IF NOT EXISTS maillists_to_subscribers
			(maillist_id int, subscriber_id int)''')
		self.factory=MailListDataBaseFactory(self.conn)
	def test_save(self):
		m1 = self.factory.create("Hack Bulgaria")
		m1.add_subscriber("Rado","Rado@gmail.com")
		m1.add_subscriber("Imperatora","Tsveta@gmail.com")
		db_adapter=MailListDataBaseAdapter("testtable",m1)
		db_adapter.save()
		c=self.conn
		data=c.execute("SELECT maillist_id, name FROM maillist").fetchall()
		self.assertEqual(data[0],(1,"Hack Bulgaria"))
		m2 = self.factory.create("Uni Sofia")
		m2.add_subscriber("Lucho","Lucho@gmail.com")
		db_adapter2=MailListDataBaseAdapter("testtable",m2)
		db_adapter2.save()
		c=self.conn
		data=c.execute("SELECT maillist_id, name FROM maillist").fetchall()
		self.assertEqual(data[1],(2,"Uni Sofia"))
		c=self.conn
		data=c.execute("SELECT name, email FROM subscribers").fetchall()
		expected = [("Rado","Rado@gmail.com"),("Imperatora","Tsveta@gmail.com"),("Lucho","Lucho@gmail.com")]
		self.assertEqual(sorted(expected),sorted(data))
		# sorted, because dictionary inserts elements on random
		c=self.conn
		data=c.execute("SELECT maillist_id, subscriber_id FROM maillists_to_subscribers").fetchall()
		expected=[(1,1),(1,2),(2,3)]
		self.assertEqual(expected,data)
	def test_load(self):
		m1 = self.factory.create("Hack Bulgaria")
		m1.add_subscriber("Rado","Rado@gmail.com")
		m1.add_subscriber("Imperatora","Tsveta@gmail.com")
		db_adapter1=MailListDataBaseAdapter("testtable",m1)
		db_adapter1.save()
		m2 = MailListDataBaseAdapter("testtable")
		m2 = m2.load(1)
		self.assertEqual("Hack Bulgaria",m2.get_name())
		self.assertEqual(sorted([("Rado","Rado@gmail.com"),("Imperatora","Tsveta@gmail.com")]),sorted(m2.get_subscribers()))
	def tearDown(self):
		call("rm " + self.db_name,shell=True)
if __name__ == '__main__':
	unittest.main()

