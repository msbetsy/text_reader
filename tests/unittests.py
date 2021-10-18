"""The module is responsible for unittest."""
import unittest
from text_reader.files import FilesManager
from text_reader.database import SQLDatabase


class UnitTestFilesManager(unittest.TestCase):
    """This class can be used for testing files module.
    """
    text_to_test = "me me, our, our, our, our, our, myself\nmy my my, my we, we we our\nhouse house house house "\
            "house house house\navec, dans, dans, dans, dans, dans, dans\nelle je, je, je, je, je\nmais mais mardi " \
            "mardi, mardi"

    def setUp(self):
        self.file_m = FilesManager()

    def test_load_file(self, output=text_to_test):
        """Test loading file."""
        self.assertEqual(self.file_m.load_file("text_file_to_tests.txt"), output)

    def test_top_5_words_en(self, text=text_to_test):
        """Show top 5 words, english language."""
        words_list_en = ['house', 'dans', 'je', 'mardi', 'mais']
        self.file_m.text = text
        self.assertEqual(self.file_m.find_top_5_words('english'), words_list_en)

    def test_top_5_words_fr(self, text=text_to_test):
        """Show top 5 words, french language."""
        words_list_fr = ['house', 'our', 'my', 'mardi', 'we']
        self.file_m.text = text
        self.assertEqual(self.file_m.find_top_5_words('french'), words_list_fr)

    def tearDown(self):
        self.file_m = None


class UnitTestSQLDatabase(unittest.TestCase):
    """This class can be used for testing database module.
    """

    def setUp(self):
        self.sql = SQLDatabase()

    def test_create_db(self):
        """Test db creation."""
        self.sql.db_name = "sql_test"
        self.assertTrue(self.sql.create_database(), "Database exists.")

    def test_create_existing_db(self):
        """Test creation a db with name already exists."""
        self.sql.db_name = "sql_test"
        self.assertFalse(self.sql.create_database())

    def test_show_db(self):
        """Test if text_reader_sql_test is on the list of dbs."""
        self.assertIn("text_reader_sql_test", self.sql.show_database(), "Database doesn't exist.")

    def test_create_table(self):
        """Test creation of table."""
        self.sql.db_name = "text_reader_sql_test"
        self.assertTrue(self.sql.create_table('test_table'), "Can't create table.")

    def test_show_tables(self):
        """Test if test_table is on the list of table names."""
        self.assertIn("test_table", self.sql.show_tables('text_reader_sql_test'), "Table doesn't exist.")

    def test_insert_item(self):
        """Test inserting a record into the db."""
        self.sql.db_name = "text_reader_sql_test"
        self.sql.table_name = "test_table"
        self.assertTrue(self.sql.insert_item('path', 'one', 'two', 'three', 'four', 'five'), "Can't insert item to db.")

    def tearDown(self):
        self.sql = None
