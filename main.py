import schedule
import financia
import carteira
import autoFinance
import connectDataBase
import datetime
import os

class main:
    def __init__(self):
        if not list(connectDataBase.ConnectDataBase('carteira').showData()):
            self.createCarteira()

        schedule.every().day.at("00:00").do(self.job)
        self.createMenu()

    def job(self):
        autoFinance.autoFinance.depositAutoFinance(list(connectDataBase.ConnectDataBase('carteira').showData())[0])

    def createCarteira(self):
        # Run the scheduled jobs
        schedule.run_pending()
        print("Bem vindo ao Financys! Vamos começar criando uma carteira para você.")
        print("Sua carteira é onde você irá inserir suas finanças e finanças automáticas.")
        print("Vamos começar criando uma carteira para você.")
        nome = input("Digite o nome da carteira: ")
        carteira1 = carteira.carteira([], [], nome).createCarteira()
        self.clear_console()
        print(f'Carteira {carteira1.nome} criada com sucesso!')
        self.createMenu()

    def createMenu(self):
        self.clear_console()
        c1 = connectDataBase.ConnectDataBase('carteira').showData()[0] 
        print("Bem vindo ao Financys! O que deseja fazer?")
        print("Sua carteira é onde você irá inserir suas finanças e finanças automáticas.")
        print(f"Sua carteira atual é: {c1['nome']}")
        print(f"Saldo atual: {c1['saldo']}")
        print("Digite o número da opção desejada:")
        print("1 - Inserir finanças")
        print("2 - Inserir finanças automáticas")
        print("3 - Editar nome da carteira")
        print("4 - Mostrar Finanças")
        print("5 - Sair")
        option = input("Digite a opção desejada: ")
        self.clear_console()
        if option == "1":
            self.insertFinancas(c1)
        elif option == "2":
            self.insertAutoFinance(c1)
        elif option == "3":
            self.editNameCarteira(c1)
        elif option == "4":
            self.showCarteira(c1)
        elif option == "5":
            print("Até mais!")
            exit()
        else:
            print("Opção inválida")
            self.createMenu()

    def insertFinancas(self, c1):
        print(f"Inserindo finanças na carteira {c1['nome']}")
        print("Digite se a finança é de entrada ou saída")
        print("1 - Entrada")
        print("2 - Saída")
        option = input("Digite a opção desejada: ")
        if option == "1":
            valor = float(input("Digite o valor: "))
            motivo = input("Digite o motivo: ")
            financas = financia.financia(valor, motivo)
            c1['financas'].append(financas._id)
            c1['saldo'] += valor
            connectDataBase.ConnectDataBase('carteira').updateData({'nome': c1['nome']}, {'$set': {'financas': c1['financas'], 'saldo': c1['saldo']}})
            print(f'Finança inserida com sucesso na carteira {c1["nome"]}!')
            self.createMenu()
        elif option == "2":
            valor = float(input("Digite o valor: "))
            motivo = input("Digite o motivo: ")
            financas = financia.financia(-valor, motivo)
            c1['financas'].append(financas._id)
            c1['saldo'] -= valor
            connectDataBase.ConnectDataBase('carteira').updateData({'nome': c1['nome']}, {'$set': {'financas': c1['financas'], 'saldo': c1['saldo']}})
            print(f'Finança inserida com sucesso na carteira {c1["nome"]}!')
            self.createMenu()
        else:
            print("Opção inválida")
            self.insertFinancas(c1)

    def insertAutoFinance(self, c1):
        print(f"Inserindo finanças automáticas na carteira {c1['nome']}")
        print("Digite o dia do mês que deseja inserir a finança")
        print("Todo dia do mes nesse dia será inserido a finança")
        print("Digite se a finança é de entrada ou saída")
        print("1 - Entrada")
        print("2 - Saída")
        option = input("Digite a opção desejada: ")
        if option == "1":
            valor = float(input("Digite o valor: "))
            motivo = input("Digite o motivo: ")
            dia = int(input("Digite o dia do mês que deseja inserir a finança: "))
            autoFinance1 = autoFinance.autoFinance(financia.financia(valor, motivo), dia)
            c1['autoFinance'].append(autoFinance1._id)
            connectDataBase.ConnectDataBase('carteira').updateData({'nome': c1['nome']}, {'$set': {'autoFinance': c1['autoFinance']}})
            print(f'Finança automática inserida com sucesso na carteira {c1["nome"]}!')
            self.createMenu()
        elif option == "2":
            valor = float(input("Digite o valor: "))
            motivo = input("Digite o motivo: ")
            dia = int(input("Digite o dia do mês que deseja inserir a finança: "))
            autoFinance1 = autoFinance.autoFinance(financia.financia(-valor, motivo), dia)
            c1['autoFinance'].append(autoFinance1._id)
            connectDataBase.ConnectDataBase('carteira').updateData({'nome': c1['nome']}, {'$set': {'autoFinance': c1['autoFinance']}})
            print(f'Finança automática inserida com sucesso na carteira {c1["nome"]}!')
            self.createMenu()
        else:
            print("Opção inválida")
            self.insertAutoFinance(c1)

    def showCarteira(self, c1):
        print(f"Finanças da carteira {c1['nome']}:")
        for i in c1['financas']:
            i = connectDataBase.ConnectDataBase('financia').findId({'_id': i})
            if i['value'] > 0:
                print(f"[ENTRADA] - Valor: {i['value']} - Motivo: {i['motivo']}")
            else:
                print(f"[SAÍDA] - Valor: {i['value']} - Motivo: {i['motivo']}")
        print(f"Finanças automáticas da carteira {c1['nome']}:")
        for i in c1['autoFinance']:
            i = connectDataBase.ConnectDataBase('autoFinancia').findId({'_id': i})
            finance = autoFinance.autoFinance.getFiancaAggregated(i)
            if finance['value'] > 0:
                print(f"[ENTRADA] - Valor: {finance['value']} - Motivo: {finance['motivo']} - Dia: {i['autoDate']}")
            else:
                print(f"[SAÍDA] - Valor: {finance['value']} - Motivo: {finance['motivo']} - Dia: {i['autoDate']}")
        input("Pressione enter para voltar ao menu")
        self.createMenu()

    def editNameCarteira(self, c1):
        newName = input("Digite o novo nome da carteira: ")
        connectDataBase.ConnectDataBase('carteira').updateData({'nome': c1['nome']}, {'$set': {'nome': newName}})
        print(f'Nome da carteira alterado com sucesso para {newName}!')
        self.createMenu()

    def clear_console(self):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)

main()
