from enlace import enlace
import time
import traceback


class Pacotes():

    def __init__(self, port):
        self.com1 = enlace(port)
        self.com1.enable()
        print("Porta Aberta")
        self.eop = b'\x0b\x0a\x0b\x0a'

    def constroiPacotes(self, head, pacotes=b''):

        return (head + pacotes + self.eop)

def resend():
    pass

def constroiHead(continuar, repetir):
    listaHead = []
    listaHead.append(int(0).to_bytes(1, 'big'))
    listaHead.append(int(0).to_bytes(1, 'big'))
    listaHead.append(int(0).to_bytes(1, 'big'))
    listaHead.append(continuar)
    listaHead.append(repetir)
    head = b''.join(listaHead)

    while len(head) != 10:
        head += b'\x00'

    return (head)

def main():
    main = True
    resultados = []
    eop = b'\x0b\x0a\x0b\x0a'
    id_previous = b''

    pacotes = Pacotes("COM6")

    while main:

        try:
            totalDePacotes = 255
            contagem = 1            

            while contagem <= totalDePacotes:

                rxbuffer1, nrx = pacotes.com1.getData(10)
                tamanhoPacote = rxbuffer1[0]
                qualPacote = rxbuffer1[1]
                totalDePacotes = rxbuffer1[2]
                rxbuffer2, nrx = pacotes.com1.getData(tamanhoPacote)
                rxbuffer3, nrx = pacotes.com1.getData(4)
                print(f'\nHEAD: {rxbuffer1}')
                print(f'\nID DO PACOTE: {qualPacote}')
                print(f'\nPAYLOAD: {rxbuffer2}')
                print(f'\nEOP: {rxbuffer3}')

                contagem = qualPacote
    
            #Handshake
            # print("Receiving Handshake")
            # handshake, nRx = pacotes.com1.getData(14)
            # pacotes.com1.sendData(handshake)

            #Inicia Transmissão

            #Head
            print("Receiving Head data")
            head, headsize = pacotes.com1.getData(10)
            id_payload = head[0] .to_bytes(1, 'big')
            size_payload = head[1]
            num_packages = head[2:4]

            print(f"Id do pacote: {id_payload}")
            print(f"Quantidade de pacotes: {num_packages}")
            payload, payloadSize = pacotes.com1.getData(size_payload)
            

            EOP, nEOP = pacotes.com1.getData(4)
            if EOP == eop:
                print("Deu tudo certo!")
                head = constroiHead(b'\x01', b'\x00')
                sendNext = Pacotes.constroiPacotes(head)
                pacotes.com1.sendData(sendNext)
                resultados.append(payload)
                
            else:
                print("Algo deu errado")
                head = constroiHead(b'\x00', b'\x01')
                sendAgain = Pacotes.constroiPacotes(head)
                pacotes.com1.sendData(sendAgain)


        except Exception as erro:
            print("ops! :-\\")
            print(traceback.format_exc())
            print(erro)
            pacotes.com1.disable()

if __name__ == "__main__":
    main()
