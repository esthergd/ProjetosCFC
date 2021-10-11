from _typeshed import IdentityFunction
from enlace import *
import time
import numpy as np
from functions.functions import *

serialName = "COM5"

imgPath = 'ferro.jpg'
with open(imgPath, 'rb') as file:
    imageByte = file.read()

def createHead(keep, repeat):
    listHead = []
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(int(0).to_bytes(1, 'big'))
    listHead.append(keep)
    listHead.append(repeat)
    head = b''.join(listHead)

    return head

def main():
    main = True
    results = []
    id = b''
    eop = b'\x0b\x0a\x0b\x0a'
    data = Datagram(port = serialName)
    payload = Payload(imageByte)

    pkgSize = payload.quebraPacote() #PKG_LIST
    totalPkg = payload.totalPacotes() #TOTAL_PACKAGES
    sizePkg = payload.tamanhoPacote() #SIZE_LIST
    pkgNmbr = payload.nPacote() #PKG_NBR

    try:
        packages = 255
        count = 1
        idle = True

        while idle:
            print('Servidor aberto e ocioso para a comunicação')
            print('###########################################')

            rxBuffer, nRx = data.com1.getData(14)

            if rxBuffer[2] == b'\xcc':
                idle = False
                break
            else:
                print('Id do servidor está errado')
                time.sleep(1)
                continue

        time.sleep(1)

        type = 2

        if type == 2:
            head = Head(type, totalPkg, 0, 0, 0, 0, 0, 0).creatHead()
            data.com1.sendData(head)
        
        while count <= packages:
            timer1 = time.time()
            timer2 = time.time()

            print('O Head foi recebido')
            print('###################')
            head, nRx = data.com1.getData(10)

            typeMsg = head[0]
            pkgsTotal = head[3]
            nmbrPkg = head[4].to_bytes(1, 'big')
            pkgSize = head[5]
            
            print(f'Qual o tipo do Pacote: {typeMsg}')
            print('#################################')
            print(f'Qual é o pacote recebido: {nmbrPkg}')
            print('####################################')
            print(f'Quantidade de pacotes para serem lidos: {pkgsTotal}')
            print('####################################################')
            payload, nRx = data.com1.getData(pkgSize)
            eop, nRx = data.com1.getData(4)

            i = 1

            while i <= packages:
                if nmbrPkg == i and eop == b'\x0b\x0a\x0b\x0a':
                    i += 1
                    
            




    except Exception as exception:
        print(exception)
        data.com1.disable()

