from datetime import datetime

class Log:
    def __init__(self, side, typeCase):
        self.side = side
        self.fileLog = open('files/logs/{}{}.txt'.format(side,typeCase), 'a')

    def logCrate(self, typeSend, type, size, pkgSend, totalPkgs, crc = b'' ):
        '''
        date -> MOMENTO DO ENVIO
        typeSend -> ENVIOU/RECEBEU
        type -> 1,2,3 etc.
        size -> TAMANHO INTEIRO
        pkgSend -> TYPE 3 (INTEIRO)
        totalPkgs -> TYPE 3 (INTEIRO)
        '''
        date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
        crc=hex(int.from_bytes(crc, byteorder='big'))
        message = '{} / {} / {} / {}'.format(date,typeSend,type,size)
        if type == 3:
            message = message + ' / {} / {} / {}'.format(pkgSend,totalPkgs, crc) 
        else:
            message
        self.fileLog.write(message+'\n')
    
    def closeLog(self):
        self.fileLog.close()