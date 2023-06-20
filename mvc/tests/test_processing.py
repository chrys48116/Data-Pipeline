from mvc.controllers.processing import Processing

import unittest
from unittest.mock import MagicMock

class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.processing = Processing()

    def test_data_empresas(self):
        name = "Empresas0.zip"
        data = ...

        result = self.processing.data_empresas(name, data)

        self.assertEqual(result, ...)

    def test_data_estabelecimento(self):
        name = "Estabelecimento0.zip"
        data = ...

        result = self.processing.data_estabelecimento(name, data)

        self.assertEqual(result, ...)


if __name__ == '__main__':
    unittest.main()