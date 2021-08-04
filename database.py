"""The module is responsible for SQL databases."""
import mysql.connector
import databaseconfig as cfg


class SQLDatabase:
    """This class can be used for SQL operation on databases.
    """

    def __init__(self):
        """Constructor method."""
        self.db_name = ""
        self.all_databases = []

    @staticmethod
    def connect():
        """Connect with database.

        :return: Cursor and connector.
        :rtype: mysql.connector.connection.MySQLConnection, mysql.connector.cursor.MySQLCursor
        """
        conn = mysql.connector.connect(**cfg.mysql_connect)
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def close(cursor, conn):
        """Close connection with database.

        :param cursor: MySQL cursor.
        :type cursor:  mysql.connector.cursor.MySQLCursor
        :param conn: MySQL connector.
        :type conn: mysql.connector.connection.MySQLConnection
        """
        cursor.close()
        conn.close()

    def create_database(self):
        """Create new database.

        :raises mysql.connector.Error: Fail during creation database.
        :raises mysql.connector.errors.DatabaseError: Database already exists.
        :return: An information of success of operation.
        :rtype: bool
        """
        conn, cursor = SQLDatabase.connect()
        success = False
        try:
            cursor.execute(
                "CREATE DATABASE text_reader_{} DEFAULT CHARACTER SET 'utf8'".format(self.db_name))
            success = True
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
        except mysql.connector.errors.DatabaseError as err:
            print("database exists: {}".format(err))
        finally:
            SQLDatabase.close(cursor, conn)

        return success

    def show_database(self):
        """Show all databases.

        :return: All names of databases.
        :rtype: table
        """
        conn, cursor = SQLDatabase.connect()
        cursor.execute("SHOW DATABASES")
        self.all_databases = [db[0] for db in cursor.fetchall()]
        SQLDatabase.close(cursor, conn)
        return self.all_databases

    def change_database(self, cursor):
        """Switch database.

        :param cursor: MySQL cursor.
        :type cursor:  mysql.connector.cursor.MySQLCursor
        :raises mysql.connector.errors.ProgrammingError: Unknown database.
        """
        try:
            cursor.execute("USE {}".format(self.db_name))
        except mysql.connector.errors.ProgrammingError as err:
            print("{}, {} -->  unknown".format(err, self.db_name))
