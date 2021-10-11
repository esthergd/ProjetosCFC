import os
from io import TextIOWrapper
from enlace import *
import numpy as np
import time
import random
from log.log import *
from math import *
from functions.functions import *
import log.log import *

imgPath = 'ferro.jpg'
with open(imgPath, 'rb') as file:
    imageByte = file.read()

serialName = 'COM5'

def main():
    data = Datagram(port = serialName)
    payload = Payload(imageByte)
    eop = b'\x0b\x0a\x0b\x0a'

    pkgSize = payload.quebraPacote()
    totalPkg = payload.totalPacotes()
    sizePkg = payload.tamanhoPacote()
    pkgNmbr = payload.nPacote()

    try:

        print('A comunicação foi aberta com sucesso')
        print('####################################')
        print(f'Quanto pacotes serão enviados: {pkgNmbr}')

        HANDSHAKE = False
        SEND = False
        type = 1
        count = 0

        if type == 1:

            HANDSHAKE = True

            head = Head(type, totalPkg, 0, 0, 0, 0, 0, 0).creatHead()

            while HANDSHAKE:

                print('Iniciando o HandShake com o Server')
                print('Você está pronto para receber os dados Server??')
                
                timeout = time.time() + 5
                txBuffer1 = head + eop
                data.com1.sendData(txBuffer1)

                logType1 = Log(txBuffer1, 'send')
                type1Msg = logType1.crateLog()
                logType1.writeLog(type1Msg, 'Client1.txt')

                while time.time() < timeout:
                    if data.com1.rx.getIsEmpty != True:
                        rxBuffer, nRx = data.com1.getData(14)
                        type2 = rxBuffer
                        logType2 = Log(type2, 'receive')
                        type2Msg = logType2.crateLog()
                        logType2.writeLog(type2Msg, 'Client1.txt')

                        if rxBuffer[1] == 22:
                            print('TUDO CERTO COM O ID')
                            print('###################')
                            print('Servidor está pronto para comunicação')
                            print('#####################################')
                            print('HandShake realizado com maestria')
                            print('################################')
                            HANDSHAKE = False
                            type = 3
                            break

                if HANDSHAKE:
                    check = input('Servidor inativo. Tentar novamente? [Y/N]') 
                    print("#########################################")
                    if check.upper() == "Y": 
                        print("Rodando servidor novamente")
                        continue
                    elif check.upper() == 'N':
                        print('Encerrando Comunicação')
                        print("----------------------------------------")
                        data.com1.disable()
                else:
                    pass
        if type == 3:
            count = 1
            while count <= pkgNmbr:
                sending = True
                head = Head(type, totalPkg, pkgNmbr[count-1], sizePkg[count-1], 0, 0, 0, 0).creatHead()

                print(f'O Head do pacote a ser enviado é {head}')
                print('#########################################')+
                pkg = Datagram.constroiPacotes(head, pkgSize[count-1][0])

                print(f'Pacoe a ser enviado {count}: {pkg}')
                time.sleep(1)
                data.com1.sendData(pkg)

                logType3 = Log(head, 'send')
                type3Msg = logType3.crateLog()
                logType3.writeLog(type3Msg, 'Client1.txt')

                timer1 = time.time()
                timer2 = time.time()

                print('O pacote foi enviado')
                print('####################')
                print('No Aguardo da resposta do Server')
                
                while not sending:
                    rxBuffer, nRx = data.com1.getData(10)

                    rsp3 = rxBuffer
                    typeRsp = rxBuffer[0]

                    log3Rsp = Log(rsp3, 'receive')
                    rspMsg3 = log3Rsp.crateLog()
                    log3Rsp.writeLog(rspMsg3, 'Client1.txt')

                    if typeRsp == 4:
                        count += 1
                        sending = True

                        print(f"Type of message: {typeRsp}")
                        print(f"Pkg {count} recieved with success!")

                    elif typeRsp == 6:
                        count = rxBuffer[6]
                        print(f"Type of message: {typeRsp}")
                        print(f"Pkg {count} not found!")

                        headType6 = Head(typeRsp, totalPkg, pkgNmbr[count-1], sizePkg[count-1], 0, rxBuffer[6], 0, 0).creatHead()
                        pkg6 = data.constroiPacotes(headType6, sizePkg[count-1][0])

                        print(f'Sending pkg {count} again!')
                        time.sleep(1)
                        data.com1.sendData(pkg6)

                        logType6 = Log(headType6, 'send')
                        type6Msg = logType6.crateLog()
                        logType6.writeLog(type6Msg, 'Client1.txt')
                        
                        timer1 = time.time()''
                        timer2 = time.time()

                    elif time.time() - timer1 > 5:
                        print(f'5 seconds have passed, sending pkg {count} again')

                        data.com1.sendData(pkg)
                        log3Rsp = Log(head, 'receive')
                        rspMsg3 = log3Rsp.crateLog()
                        log3Rsp.writeLog(rspMsg3, 'Client1.txt')
                    
                    if time.time() - timer2 > 20:
                        print(f'20 Seconds have passed, ending communication with server')

                        type = 5
                        headType5 = Head(type, totalPkg, pkgNmbr[count-1], sizePkg[count-1], 0, rxBuffer[6], 0, 0).creatHead()
                        pkg5 = data.constroiPacotes(headType5, sizePkg[count-1][0])
                        time.sleep(1)
                        data.com1.sendData(pkg5)

                        logType5 = Log(head, 'send')
                        type5Msg = logType5.crateLog()
                        logType5.writeLog(type5Msg, 'Client1.txt')

                        data.com1.disable()

            print('Todos os pacotes foram enviados com sucesso')
            print('###########################################')


    except Exception as exception:
        print(exception)
        data.com1.disable()

if __name__ == '__main__':
    main()
        
