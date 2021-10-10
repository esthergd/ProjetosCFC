import os
from io import TextIOWrapper
from enlace import *
import numpy as np
import time
import random
from log.log import *
from math import *
from functions.functions import *

imgPath = 'ferro.jpg'
with open(imgPath, 'rb') as file:
    imageByte = file.read()

serialName = 'COM5'

def main():
    data = Datagram(port = serialName)
    payload = Payload(imageByte)
    eop = b'\x0b\x0a\x0b\x0a'

    pkgSize = Payload.quebraPacote() #PKG_LIST
    totalPkg = Payload.totalPacotes() #TOTAL_PACKAGES
    sizePkg = Payload.tamanhoPacote() #SIZE_LIST
    pkgNmbr = Payload.nPacote() #PKG_NBR

    testError = True

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

                while time.time() < timeout:

                    if data.com1.rx.getIsEmpty != True:
                        head = data.com1.getData(10)
                        type = head[0]
                        if type == 2:
                            rxBuffer, nRx = data.com1.getData(14)

                            if txBuffer1 == rxBuffer:
                                print('O servidor está pronto para a comunicação')
                                print('#########################################')
                                print('O Handshake realizado com maestria')

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
            SEND = True
            count = 1

            while SEND:
                while count <= pkgNmbr:
                    sending = True
                    while sending:
                        head = Head(type, totalPkg, pkgNmbr[count-1], pkgSize[count-1], 0, 0, 0, 0).creatHead()

                        print(f'O Head do pacoote a ser enviado é {head}')
                        print('#########################################')
                        pkg = Datagram.constroiPacotes(head, pkgSize[count-1][0])

                        print(f'Pacoe a ser enviado {count}: {pkg}')
                        data.com1.sendData(pkg)

                        time.sleep(0.1)

                        time1 = time.time()

                        print('O pacote foi enviado')
                        print('####################')
                        print('No Aguardo da resposta do Server')
                        
                        head, nRx = data.com1.getData(10)
                        type = head[0]

                        if type == 4:
                            count +=1
                        else:
                            if time1 > 20:
                                type = 5
                                head = Head(type, 0, 0, 0, 0, 0, 0, 0).creatHead()
                                data.com1.sendData(head)
                                time.sleep(0.1)
                                print('Erro de TimeOut, encerrando a comunicação')
                                data.com1.rx.clearBuffer()
                                data.com1.disable()
                                pass
                            elif type == 5: 
                                print('Erro de TimeOut, encerrando a comunicação')
                                time.sleep(0.1)
                                data.com1.disable()
                                pass
                            else:
                                #Recebe msg
                                # data.com1.getdata()
                                if type == 6:
                                    #corrige o count
                                    #envia msg do type 3
                                    #reset timer 1 e 2
                                    pass
                                else:
                                    #volta tudo
                                    pass

                        rxBuffer, nRx = pkg.com1.getData(14)
                        keep = rxBuffer[3]
                        repeat = rxBuffer[4]

                        if keep == 1 and repeat == 0:
                            sending = False
                            print('Pacote recebebido, pronto para enviar o próxmo')
                            print('##############################################')
            
            print('Todos os pacotes foram enviados com sucesso')
            print('###########################################')


    except Exception as exception:
        print(exception)
        data.com1.disable()

if __name__ == '__main__':
    main()
        
