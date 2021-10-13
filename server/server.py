from enlace import *
import time
from functions.functions import *
from log.log import*

serialName = "COM5"

imgPath = 'ferro.jpg'
with open(imgPath, 'rb') as file:
    imageByte = file.read()

def main():
    eop = b'\x0b\x0a\x0b\x0a'
    data = Datagram(serialName)
    payload = Payload(imageByte)

    pkgSize = payload.quebraPacote()
    totalPkg = payload.totalPacotes()
    sizePkg = payload.tamanhoPacote()
    pkgNmbr = payload.nPacote()

    try:
        packages = 255
        count = 1
        idle = True

        while idle:
            print('Server open and ready to comunicate')
            print('###########################################')

            rxBuffer, nRx = data.com1.getData(14)

            type1 = rxBuffer
            logType1 = Log(type1, 'recieve')
            type1Msg = logType1.crateLog()
            logType1.writeLog(type1Msg, 'Server1.txt')

            if rxBuffer[2] == 44:
                print('Server ID correct')
                idle = False
                break
            else:
                print('Server ID is wrong!')
                time.sleep(1)
                continue

        time.sleep(1)

        headType2 = Head(2, totalPkg, 0, 0, 0, 0, 0, 0).creatHead()
        pkg2 = headType2 + eop
        data.com1.sendData(pkg2)

        logtype2 = Log(pkg2, 'send')
        msgType2 = logtype2.crateLog()
        logtype2.writeLog(msgType2, 'Server1.txt')

        while count <= packages:

            timer1 = time.time()
            timer2 = time.time()

            head, nRx = data.com1.getData(10)

            head3 = head

            logHead3 = Log(head3, 'receive')
            msgType3 = logHead3.crateLog()
            logHead3.writeLog(msgType3, 'Server1.txt')

            typeMsg = head[0]

            if typeMsg == 3:
                
                totalPkgs = head[3]
                pkgNmbr = head[4]
                pkgSize = head[5]
                crc = head[8:10]
                print('Type of packege: ''{}'.format(typeMsg))
                print('Size of the packege: ''{}'.format(pkgSize))
                print('Amount of packeges: ''{}'.format(totalPkgs))
                print('CRC: ''{}'.format(crc))

                pkg, 
            




    except Exception as exception:
        print(exception)
        data.com1.disable()

