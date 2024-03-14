import datetime
import connectDataBase

class financia:
    def __init__(self, value, motivo):
        self.value = value
        self.motivo = motivo
        self.date = datetime.datetime.now()
        connectDataBase.ConnectDataBase('financia').insertData(self.__dict__)
    

