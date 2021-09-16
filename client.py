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
        self.eop = eop 

    def constroiPacotes(self):
        return (self.head + self.payload + self. eop)

class Head(): 

    def __init__(self):

        self.tamanho = payload.tamanhoPacote()
        self.nPacote = payload.nPacote()
        self.total = payload.totalPacotes()
        #self.tipo = tipo


    def constroiHead(self):
        return (self.tamanho + self.nPacote + self.total)
    
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
        self.fim = [b'\x00', b'\x00',b'\x00', b'\x00']

payload = Payload(imageBytes)
# head = Head()

print(len(payload.quebraPacote()[0][0]))
print(len(payload.quebraPacote()[-1][0]))
print(payload.tamanhoPacote()[-1])
print(len(payload.nPacote()))
#print(Head.constroiHead(payload))