from datetime import datetime
from crccheck.crc import Crc16

class Log():
    def __init__(self, info, alteration):
        self.typeMsg = info[0]
        self.size = len(info)
        self.alteration = alteration
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        self.all = []

        if self.typeMsg == 3:
            self.pkgNmbr = info[4]
            self.totalPkgs = info[3]
            self.crc = str(info[8:10]).upper()
            self.crc = self.crc[4:6] + self.crc[8:10]
        else:
            self.pkgNmbr = ''
            self.totalPkgs = ''
            self.crc = ''
        
    def crateLog(self):
        if self.typeMsg == 3:
            info = f'\n {self.time} / {self.alteration} / {self.typeMsg} / {self.size} / {self.pkgNmbr} / {self.totalPkgs} / {self.crc}'
        else:
            info = f'\n {self.time} / {self.alteration} / {self.typeMsg} / {self.size}'
        return info

    def writeLog(self, create, fileName):
        self.all.append(create)
        file = open(fileName, 'a')
        for create in self.all:
            file.write(create)
            file.close()

    def crc(self, data):
        crc = Crc16.calc(data)
        return crc
    