from mvc.models.database import Database

import unittest
from unittest.mock import MagicMock

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()

    def tearDown(self):
        pass

    def test_insert(self):
        zip_name = "Empresas.zip"
        data = ...

        self.database.insert(zip_name, data)


    def test_query(self):
        table_name = "Empresas"

        result = self.database.query(table_name)

        self.assertEqual(result, ...)


if __name__ == '__main__':
    unittest.main()
