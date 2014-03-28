from maillist import MailList


class MailListDataBaseFactory():
    """docstring for MailListFactory"""
    def __init__(self,conn):
        self.conn=conn
        self.__current_id = self.init_id(self.conn)
    def init_id(self,conn):
        c=conn.cursor()
        ids=c.execute("SELECT maillist_id FROM maillist").fetchall()
        if ids == []:
            return 1
        else:
            return ids[len(ids)-1][0] + 1 # ids is a list of tuples

    def next_id(self):
        result = self.__current_id
        self.__current_id += 1

        return result

    def create(self, list_name):
        m = MailList(self.next_id(), list_name)
        return m
