from io import TextIOWrapper
from os import name
from enlace import *
import time
import numpy as np
import time
import random
from math import *

imagePath = 'texto.txt'
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

        self.tamanhoPkg = tamanho
        self.nPacote = nPacote 
        self.totalPkgs = total

    def constroiHead(self):
        self.listaHead.append(int(self.tamanhoPkg).to_bytes(1, 'big'))
        self.listaHead.append(int(self.nPacote).to_bytes(1, 'big'))
        self.listaHead.append(int(self.totalPkgs).to_bytes(1, 'big'))
        self.head = b''.join(self.listaHead)

        while len(self.head) != 10:
            self.head += b'\x00'

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

def main():
    pacotes = Pacotes(port="/dev/ttyACM0")
    payload = Payload(imageBytes)

    listaTamanho = payload.tamanhoPacote()
    nPacote = payload.nPacote()
    listaPacotes = payload.quebraPacote()

    testarErro = True

    try:

        handshake = True
        while handshake:
                
            txBuffer = b'\x01'*14
            pacotes.com1.sendData(txBuffer)
            rxBuffer, nRx = pacotes.com1.getData(14)

            if rxBuffer == txBuffer:
                print("HandShake concluído")
                handshake = False

            for i in nPacote:
                enviando = True
                while enviando:

                    classeHead = Head(listaTamanho[i-1], nPacote[i-1], total=payload.totalPacotes())
                    head = classeHead.constroiHead()
                    pacote = pacotes.constroiPacotes(head, listaPacotes[i-1][0])

                    if testarErro and i==2:
                        classeHead = Head(83, nPacote[i-1], total=payload.totalPacotes())
                        head = classeHead.constroiHead()
                        pacote = pacotes.constroiPacotes(head, listaPacotes[i-2][0])
                        testarErro = False
                        print("Envio Errado")


                    time.sleep(0.1)
                    pacotes.com1.sendData(pacote)
                    print("Pacote enviado {0}".format(i))

                    print("Esperando Resposta")
                    rxBuffer, nRx = pacotes.com1.getData(14)
                    continuar = rxBuffer[3]
                    repetir = rxBuffer[4]

                    if continuar == 1 and repetir == 0:
                        enviando = False
                        print("Recebi para continuar")
                
                
            print("Enviei Tudo")
            pacotes.com1.disable()
    except Exception as exception:
        print(exception)
        pacotes.com1.disable()

if __name__ == "__main__":
    main()