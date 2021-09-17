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

    def __init__(self, Head, Payload, eop) :

        self.head = Head
        self.payload = Payload
        self.eop = b'\x00\x00\x00\x00'

    def constroiPacotes(self):
        return (self.head + self.payload + self. eop)

class Head(): 

    def __init__(self, tamanho, nPacote, total):
        self.listaHead = []

        self.tamanho = tamanho
        self.nPacote = nPacote 
        self.total = total
        #self.tipo = tipo

    def constroiHead(self):
        self.listaHead.append(int(self.tamanho).to_bytes(1, 'big'))
        self.listaHead.append(int(self.nPacote).to_bytes(1, 'big'))
        self.listaHead.append(int(self.total).to_bytes(1, 'big'))
        self.head = b''.join(self.listaHead)

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

class EOP():

    def __init__(self):
        self.fim = 

payload = Payload(imageBytes)
listaTamanho = payload.tamanhoPacote()
nPacote = payload.nPacote()

for i in nPacote:
    head = Head(listaTamanho[i-1], nPacote[i-1], total=payload.totalPacotes())
    byteHead = head.constroiHead()
    
    print(byteHead)

# print(len(payload.quebraPacote()[0][0]))
# print(len(payload.quebraPacote()[-1][0]))
# print(payload.tamanhoPacote()[-1])

# # print(payload.totalPacotes())
# # #print(Head.constroiHead(payload))
