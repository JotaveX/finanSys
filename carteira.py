import connectDataBase
import datetime
import financia
import autoFinance

class carteira:
    def __init__(self, financas, autoFinance, nome, saldo=0):
        self.financas = financas
        self.autoFinance = autoFinance
        self.nome = nome
        self.saldo = saldo
        self.calculateSaldo()

    def createCarteira(self):
        connectDataBase.ConnectDataBase('carteira').insertData(self.__dict__)
        return self

    def insertFinancas(self, value, motivo):
        financas = financia.financia(value, motivo)
        self.financas.append(financas)
        self.saldo += value
        print(self.__dict__)
        # connectDataBase.ConnectDataBase('carteira').updateById(self._id, self.__dict__)

    def insertAutoFinance(self, value, motivo):
        financas = financia.financia(value, motivo)
        autoFinance1 = autoFinance.autoFinance(financas, datetime.datetime.now())
        self.autoFinance.append(autoFinance1._id)
        connectDataBase.ConnectDataBase('carteira').updateData({'nome': self.nome}, {'$set': {'autoFinance': self.autoFinance}}) 

    def calculateSaldo(self):
        for i in self.financas:
            i = connectDataBase.ConnectDataBase('financia').findId({'_id': i})
            self.saldo += i['value']
        
    def getCarteira(self):
        return connectDataBase.ConnectDataBase('carteira').showData()
