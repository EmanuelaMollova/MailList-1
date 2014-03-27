from maillist import MailList
import sqlite3

class MailListDataBaseAdapter():
	def __init__(self,db_path,mail_list=None):
		self.__db_name=db_path
	def create_table(cursor):
		cursor.execute(''' CREATE TABLE maillist
			(id int, name text)''')
		cursor.execute(''' CREATE TABLE subscribers
			(id int, name text, email text)''')
		cursor.execute(''' CREATE TABLE m_to_s
			(list_id int, subscriber_id int)''')