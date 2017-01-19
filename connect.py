import MySQLdb


class Connection:
    def __init__(self, user, password, db, host='localhost'):
        self.user = user
        self.host = host
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db
            )

    def disconnect(self):
        if self._connection:
            self._connection.close()


class Offices:
    def __init__(self, db_connection, named, location):
        self.db_connection = db_connection.connection
        self.named = named
        self.location = location

    def save(self):
        c = self.db_connection.cursor()
        c.execute("insert into office (named, location) values (%s, %s);",
                  (self.named, self.location))
        self.db_connection.commit()
        c.close()

con = Connection('root', '1234', 'first_db')

with con:
    m = Offices(con, 'PR department', 'Moscow, Lenina, 15/1')
    m.save()


class Members:
    def __init__(self, db_connection, name, position):
        self.db_connection = db_connection.connection
        self.name = name
        self.position = position

    def save(self):
        c = self.db_connection.cursor()
        c.execute("insert into members (name, position) values (%s, %s);",
                  (self.name, self.position))
        self.db_connection.commit()
        c.close()

con = Connection('root', '1234', 'first_db')

with con:
    m = Members(con, 'Ivanov', 'lawyer')
    m.save()