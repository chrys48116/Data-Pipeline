from mvc.controllers.controller import Controller

import unittest
from unittest.mock import MagicMock
import requests

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller(url="https://dadosabertos.rfb.gov.br/CNPJ/")
        self.controller.response = MagicMock(spec=requests.Response)
        self.controller.parser = MagicMock()

    def test_request(self):
        mock_link1 = MagicMock()
        mock_link1.get.return_value = "Empresas0.zip"
        mock_link2 = MagicMock()
        mock_link2.get.return_value = "Estabelecimento0.zip"
        self.controller.parser.find_all.return_value = [mock_link1, mock_link2]

        self.controller.processing.data_empresas.return_value = ...
        self.controller.processing.data_estabelecimento.return_value = ...

        self.controller.database.insert.return_value = ...

        self.controller.request()

        self.controller.parser.find_all.assert_called_once()
        self.controller.processing.data_empresas.assert_called_once()
        self.controller.processing.data_estabelecimento.assert_called_once()
        self.controller.database.insert.assert_called()

if __name__ == '__main__':
    unittest.main()
