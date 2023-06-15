class Menu:
    
    MODALIDADES = [
        {'nome': 'Mega-Sena', 'N': 60, 'P': 6, 'cor': '#209869', 'dias': (4, 7)},
        {'nome': 'Lotofacil', 'N': 25, 'P': 15, 'cor': '#930089', 'dias': (2, 3, 4, 5, 6, 7)},
        {'nome': 'Quina', 'N': 80, 'P': 5, 'cor': '#260085', 'dias': (2, 3, 4, 5, 6, 7)},
        {'nome': 'Lotomania', 'N': 100, 'P': 20, 'cor': '#f78100', 'dias': (2, 4, 6)},
        {'nome': 'Dupla-Sena', 'N': 50, 'P': 12, 'cor': '#a61324', 'dias': (3, 5, 7)},
        {'nome': 'Federal', 'N': 60, 'P': 6, 'cor': '#103099', 'dias': (4, 7)},
        {'nome': 'Timemania', 'N': 80, 'P': 10, 'cor': '#00ff48', 'dias': (3, 5, 7)},
        {'nome': 'Loteca', 'N': 60, 'P': 6, 'cor': '#fb1f00', 'dias': (2)},
        {'nome': 'Dia_de_Sorte', 'N': 60, 'P': 6, 'cor': '#cb852b', 'dias': (3, 5, 7)},
        {'nome': 'Super-Sete', 'N': 60, 'P': 6, 'cor': '#a8cf45', 'dias': (2, 4, 6)},
        {'nome': 'Milionaria', 'N': 60, 'P': 6, 'cor': '#2E3078', 'dias': (7)},
    ]

    def exibir_menu(self):
        print("Escolha a modalidade:")
        for i, modalidade in enumerate(self.MODALIDADES):
            print(f"{i+1} - {modalidade['nome']}")
        print('0 - Sair')

        opcao = input("\nDigite o número da modalidade desejada: ")

        try:
            opcao = int(opcao)
        except ValueError:
            print("Opção inválida. Digite apenas o número da modalidade desejada.")
            return

        if opcao < 0 or opcao > len(self.MODALIDADES):
            print("Opção inválida. Digite o número da modalidade desejada.")
            return
        
        if opcao == 0:
            print('Saindo...')
            return None

        modalidade = self.MODALIDADES[opcao-1]
        print(f"Modalidade escolhida: {modalidade['nome']}")
        return modalidade