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

    def __init__(self, tamanho, nPacote, totalPacotes, tipo):

        self.tamanho = tamanho
        self.nPacote = nPacote
        self.total = totalPacotes
        self.tipo = tipo


    def constroiHead(self):
        return (self.tamanho + self.nPacote + self.total + self.tipo)
    
class Payload():

    def __init__(self, conteudo):
        self.conteudo = conteudo

    def quebraPacote(self):
        lista_pacotes = []

        for length in range(self.totalPacotes()):
            lista_pacotes.append([self.conteudo[length*114:(length+1)*114]])

        return lista_pacotes

    def totalPacotes(self):
        pacote = len(self.conteudo)/114
        if type (pacote) == float:
            pacote = ceil(pacote)
        return pacote

class EOP():

    def __init__(self):
        self.fim = [b'\x00', b'\x00',b'\x00', b'\x00']


# payload = Payload(imageBytes)
# head = Head()

# print(len(payload.quebraPacote()[0][0]))
# print(len(payload.quebraPacote()[-1][0]))