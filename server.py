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

    pacotes = Pacotes("/dev/ttyACM1")

    try:
        num_packages = 255
        contagem = 1       

        #Handshake
        print("Receiving Handshake")
        handshake, nRx = pacotes.com1.getData(14)
        time.sleep(0.1)
        pacotes.com1.sendData(handshake)

        while contagem < num_packages:

            print("Receiving Head data")
            head, headsize = pacotes.com1.getData(10)
            id_payload = head[1] .to_bytes(1, 'big')
            size_payload = head[0]
            num_packages = head[2]

            print(f"Id do pacote: {id_payload}")
            print(f"Quantidade de pacotes: {num_packages}")
            payload, payloadSize = pacotes.com1.getData(size_payload)

            EOP, nEOP = pacotes.com1.getData(4)
            if EOP == eop:
                print("Deu tudo certo!")
                head = constroiHead(b'\x01', b'\x00')
                sendNext = pacotes.constroiPacotes(head)
                pacotes.com1.sendData(sendNext)
                resultados.append(payload)
                contagem = int.from_bytes(id_payload, "big")

            else:
                print("Algo deu errado")
                pacotes.com1.rx.clearBuffer()
                head = constroiHead(b'\x00', b'\x01')
                sendAgain = pacotes.constroiPacotes(head)
                pacotes.com1.sendData(sendAgain)
        
        
        print("Pronto!")    

        all_results = b''

        for i in resultados:
            all_results += i

        f = open("teste.txt", 'wb')
        f.write(all_results)
        f.close

        pacotes.com1.disable()
            

    except Exception as erro:
        print("ops! :-\\")
        print(traceback.format_exc())
        print(erro)
        pacotes.com1.disable()

if __name__ == "__main__":
    main()
