from mvc.views.view import View
from mvc.views.menu import Menu
from mvc.models.model import Model
from mvc.models.database import Database
from mvc.controllers.controller import Controller

def main():
    url = "https://dadosabertos.rfb.gov.br/CNPJ/"
    controller = Controller(url)
    controller.request
    controller.export_data('Empresas0')

if __name__ == '__main__':
    main()
