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
        self.table_name = ""
        self.all_tables = []

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

    def create_table(self, table_name):
        """Create table in database.

        :param table_name: Name of the new table.
        :type table_name: str
        :raises mysql.connector.errors.ProgrammingError: Can't create database.
        :return: Information of success of operation.
        :rtype: bool
        """
        self.table_name = table_name
        conn, cursor = SQLDatabase.connect()
        self.change_database(cursor)
        sucess = False
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (\
                        Text_ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                        Text_Path varchar(250) NOT NULL,\
                        Word_First varchar(250) NOT NULL, \
                        Word_Second varchar(250),\
                        Word_Third varchar(250),\
                        Word_Fourth varchar(250),\
                        Word_Fifth varchar(250));\
                        ".format(self.table_name))
            sucess = True
        except mysql.connector.errors.ProgrammingError as err:
            print("Failed creating table: {}".format(err))
        finally:
            SQLDatabase.close(cursor, conn)

        return sucess

    def show_tables(self, name_db):
        """Show all table names in chosen database.

        :param name_db: Name of the database.
        :type name_db: str
        :raises mysql.connector.errors.ProgrammingError: Unknown database.
        :return: Names of the tables.
        :rtype: list
        """
        conn, cursor = SQLDatabase.connect()
        try:
            cursor.execute("SHOW TABLES FROM {}".format(name_db))
            self.all_tables = [table[0] for table in cursor.fetchall()]
        except mysql.connector.errors.ProgrammingError as err:
            print("{} : {} --> unknown".format(err, name_db))
        finally:
            SQLDatabase.close(cursor, conn)

        return self.all_tables

    def insert_item(self, text_path, word_first, word_second, word_third, word_fourth, word_fifth):
        """Insert new record in SQL table.

        :param text_path: The path to the text file.
        :type text_path: str
        :param word_first: The most popular word in text.
        :type word_first: str
        :param word_second: The second most popular word in text.
        :type word_second: str
        :param word_third: The third most popular word in text.
        :type word_third: str
        :param word_fourth: The fourth most popular word in text.
        :type word_fourth: str
        :param word_fifth: The fifth most popular word in text.
        :type word_fifth: str
        :raises mysql.connector.errors.ProgrammingError: Can't insert item.
        :return: Information of success of operation.
        :rtype: bool
        """
        conn, cursor = SQLDatabase.connect()
        self.change_database(cursor)
        success = False
        try:
            cursor.execute("INSERT INTO {table} (Text_Path, Word_First, Word_Second, Word_Third,\
                                   Word_Fourth, Word_Fifth) VALUES ('{path}','{first}', '{second}',\
                                    '{third}', '{fourth}', '{fifth}')\
                                    ".format(table=self.table_name, path=text_path, first=word_first,
                                             second=word_second,
                                             third=word_third, fourth=word_fourth, fifth=word_fifth))
            conn.commit()
            success = True
        except mysql.connector.errors.ProgrammingError as err:
            print("{} can't insert item".format(err))
        finally:
            SQLDatabase.close(cursor, conn)

        return success
