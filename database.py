"""The module is responsible for SQL databases."""
import mysql.connector
import databaseconfig as cfg


class SQLDatabase:
    """This class can be used for SQL operation on databases.
    """

    def __init__(self):
        """Constructor method."""
        self.db_name = ""

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

        :param cursor: A character to be converted to sine wave or silence array.
        :type cursor: str
        :param conn: .
        :type conn:
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
