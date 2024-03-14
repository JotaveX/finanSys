import datetime
import connectDataBase
import carteira

class autoFinance:
    def __init__(self, finance, autoDate):
        print(finance.__dict__)
        self.finance = finance._id
        self.autoDate = autoDate
        connectDataBase.ConnectDataBase('autoFinancia').insertData(self.__dict__)

    def getFiancaAggregated(autoFinance):
        financa = connectDataBase.ConnectDataBase('financia').findId({'_id': autoFinance['finance']}) 
        return financa            
    
    def depositAutoFinance(carteira):
        for i in carteira['autoFinance']:
            i = connectDataBase.ConnectDataBase('autoFinancia').findId({'_id': i})
            if i['autoDate'] == datetime.datetime.now().day:
                finance = autoFinance.getFiancaAggregated(i)
                carteira['financas'].append(finance['_id'])
                carteira['saldo'] += finance['value']
                connectDataBase.ConnectDataBase('carteira').updateData({'nome': carteira['nome']}, {'$set': {'financas': carteira['financas'], 'saldo': carteira['saldo']}})
                
                
