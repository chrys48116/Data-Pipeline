from mvc.views.view import View
from mvc.views.menu import Menu
from mvc.models.model import Model
from mvc.models.database import Database
from mvc.controllers.controller import Controller

def main():
    menu = Menu()
    modalidade = menu.exibir_menu()
    print(f'{modalidade["nome"]}')
    pass

if __name__ == '__main__':
    main()
