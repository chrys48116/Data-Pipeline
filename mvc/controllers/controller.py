class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        self.view.show_welcome_message()

        # Aqui, você pode adicionar a lógica do controlador para solicitar as informações do usuário,
        # chamar as funções do modelo e atualizar a visualização.
