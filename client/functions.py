from enlace import *
from math import *

class Datagram():
    def __init__(self, port) :
        self.com1 = enlace(port)
        self.com1.enable()
        print("Porta Aberta")
        self.eop = b'\xFF\xAA\xFF\xAA'

    def constroiPacotes(self, head, pacotes=b''):
        return (head + pacotes + self.eop)

class Head():
    def __init__(self, type, total, pkgNmbr, payloadSize, pkgRequest, lastPkg, crc8, crc9):
        self.msgType = type
        self.serverId = 44
        self.sensorId = 22
        self.totalPkgs = total
        self.pkgNmbr = pkgNmbr
        if self.msgType == 1 or self.msgType == 2:
            self.size = 0
        else:
            self.size = payloadSize
        self.pkgRequest = pkgRequest
        self.lastPkg = lastPkg
        self.crc8 = crc8
        self.crc9 = crc9
        self.listHead = []

    def creatHead(self):
        self.listHead.append(int(self.msgType).to_bytes(1, 'big'))
        self.listHead.append(int(self.sensorId).to_bytes(1, 'big'))
        self.listHead.append(int(self.serverId).to_bytes(1, 'big'))
        self.listHead.append(int(self.totalPkgs).to_bytes(1, 'big'))
        self.listHead.append(int(self.pkgNmbr).to_bytes(1, 'big'))
        self.listHead.append(int(self.size).to_bytes(1, 'big'))
        self.listHead.append(int(self.pkgRequest).to_bytes(1, 'big'))
        self.listHead.append(int(self.lastPkg).to_bytes(1, 'big'))
        self.listHead.append(int(self.crc8).to_bytes(1, 'big'))
        self.listHead.append(int(self.crc9).to_bytes(1, 'big'))
        self.head = b''.join(self.listHead)

        return (self.head)

class Payload():
    def __init__(self, conteudo):
        self.conteudo = conteudo

    def totalPacotes(self):
        self.pacote = len(self.conteudo)/114
        if type (self.pacote) == float:
            self.pacote = ceil(self.pacote)
        return self.pacote

    def quebraPacote(self):
        self.lista_pacotes = [] 

        for length in range(self.totalPacotes()):
            self.lista_pacotes.append([self.conteudo[length*114:(length+1)*114]])

        return self.lista_pacotes

    def tamanhoPacote(self):
        self.tamanho=[]

        for length in range(len(self.quebraPacote())):
            self.tamanho.append(len(Payload.quebraPacote(self)[length][0]))
        
        return self.tamanho
    
    def nPacote(self):
        self.nPacote = []

        for length in range(len(self.tamanhoPacote())):
            self.nPacote.append(length + 1)
        return self.nPacote
