from io import TextIOWrapper
from enlace import *
import time
import numpy as np
import time
import random
from math import *

imagePath = 'ferro.jpg'
with open (imagePath, 'rb') as file:
    imageBytes = file.read()


class Pacotes():

    def __init__(self, port) :
        self.com1 = enlace(port)
        self.com1.enable()
        print("Porta Aberta")

        self.eop = b'\x0b\x0a\x0b\x0a'

    def constroiPacotes(self, head, pacotes=b''):

        return (head + pacotes + self.eop)

class Head(): 

    def __init__(self, tamanho, nPacote, total):
        self.listaHead = []

        self.tamanho = tamanho
        self.nPacote = nPacote 
        self.total = total
        self.idPacote = b'\x69'

    def constroiHead(self):
        self.listaHead.append(int(self.tamanho).to_bytes(1, 'big'))
        self.listaHead.append(int(self.nPacote).to_bytes(1, 'big'))
        self.listaHead.append(int(self.total).to_bytes(1, 'big'))
        self.head = b''.join(self.listaHead)

        while len(self.head) != 10:
            self.head += b'\x00'

        return (self.head)
    
class Payload():

    def __init__(self, conteudo):
        self.conteudo = conteudo

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


    def totalPacotes(self):
        self.pacote = len(self.conteudo)/114
        if type (self.pacote) == float:
            self.pacote = ceil(self.pacote)
        return self.pacote



payload = Payload(imageBytes)
listaTamanho = payload.tamanhoPacote()
nPacote = payload.nPacote()
listaPacotes = payload.quebraPacote()
pacotes = Pacotes(port="/dev/ttyACM0")


for i in nPacote:
    classeHead = Head(listaTamanho[i-1], nPacote[i-1], total=payload.totalPacotes())
    head = classeHead.constroiHead()
    pacote = pacotes.constroiPacotes(head, listaPacotes[i-1][0])

    #print(pacote)
    pacotes.com1.sendData(pacote)
    time.sleep(1.5)
    #print(pacotes.com1.rx.buffer)
    
    # rxbuffer1, nrx = pacotes.com1.getData(10)
    # tamanhoPacote = rxbuffer1[0]
    # qualPacote = rxbuffer1[1]
    # totalDePacotes = rxbuffer1[2]
    # rxbuffer2, nrx = pacotes.com1.getData(tamanhoPacote)
    # rxbuffer3, nrx = pacotes.com1.getData(4)
    # print(f'\nHEAD: {rxbuffer1}')
    # print(f'\nPAYLOAD: {rxbuffer2}')
    # print(f'\nEOP: {rxbuffer3}')

totalDePacotes = 255
contagem = 1

for contagem in range(totalDePacotes):

    rxbuffer1, nrx = pacotes.com1.getData(10)
    tamanhoPacote = rxbuffer1[0]
    qualPacote = rxbuffer1[1]
    totalDePacotes = rxbuffer1[2]
    rxbuffer2, nrx = pacotes.com1.getData(tamanhoPacote)
    rxbuffer3, nrx = pacotes.com1.getData(4)
    print(f'\nHEAD: {rxbuffer1}')
    print(f'\nPAYLOAD: {rxbuffer2}')
    print(f'\nEOP: {rxbuffer3}')




#print(payload.quebraPacote())
# # print(len(payload.quebraPacote()[-1][0]))
#print(payload.tamanhoPacote()[0])
# print(payload.nPacote)

# # print(payload.totalPacotes())
#print(Head.constroiHead(payload))
