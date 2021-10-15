from enlace import *
import time
from functions import *
from log import*
import traceback
import sys

serialName = "COM6"

imgPath = 'texto.txt'
with open(imgPath, 'rb') as file:
    imageByte = file.read()

def main():
    eop = b'\xFF\xAA\xFF\xAA'
    data = Datagram(serialName)
    payload = Payload(imageByte)
    results = []

    pkgSize = payload.quebraPacote()
    totalPkg = payload.totalPacotes()
    pkgNmbr = payload.nPacote()

    try:
        totalPkgs = 255
        count = 1
        idle = True

        while idle:
            print('Server opened and ready to comunicate')
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

        startTime = time.time()

        while count <= totalPkgs:

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
                print(f'Type of package: {typeMsg}')
                print(f'Size of the package: {pkgSize}')
                print(f'Amount of packages: {totalPkgs}')
                print(f'NmbrPkg {pkgNmbr}')
                print(f'CRC: {crc}')

                pkg, nRx = data.com1.getData(pkgSize)

                eop, nRx = data.com1.getData(4)

                if eop == b'\xFF\xAA\xFF\xAA' and pkgNmbr == count:
                    lastPkg = pkgNmbr

                    head4 = Head(4, 0, 0, 0, 0, lastPkg, 0, 0).creatHead()
                    pkg4 = head4 + eop
                    data.com1.sendData(pkg4)

                    logMsg4 = Log(pkg4, 'send')
                    msgType4 = logMsg4.crateLog()
                    logMsg4.writeLog(msgType4, 'Server1.txt')

                    results.append(pkg)

                    count += 1
                    startTime = time.time()
                else:
                    previousPkg = count - 1
                    head6 = Head(6, 0, 0, 0, previousPkg, 0, 0, 0,).creatHead()
                    pkg6 = head6 + eop
                    data.com1.sendData(pkg6)

                    logMsg6 = Log(pkg6, 'send')
                    msgType6 = logMsg6.crateLog()
                    logMsg6.writeLog(msgType6, 'Server1.txt')
            
            else:
                time.sleep(1)
                if time.time() - startTime > 20:
                    idle = True

                    head5 = Head(5, 0, 0, 0, 0, 0, 0, 0).creatHead()
                    pkg5 = head5 + eop
                    data.com1.sendData(pkg5)

                    logMsg5 = Log(pkg5, 'send')
                    msgType5 = logMsg5.crateLog()
                    logMsg5.writeLog(msgType5, 'Server1.txt')

                    data.com1.disable()
                    sys.exit()
                else:
                    if rxBuffer == "SENDAGAIN":

                        head4 = Head(4, 0, pkgNmbr[count-1], 0, 0, lastPkg, 0, 0).creatHead()
                        pkg4 = head4 + eop
                        data.com1.sendData(pkg4)

                        logMsg4 = Log(pkg4, 'send')
                        msgType4 = logMsg4.crateLog()
                        logMsg4.writeLog(msgType4, 'Server1.txt')

                        startTime = time.time()

        allResults = b''
        for i in results:
            allResults += i
        
        f = open("copy1.txt", "wb")
        f.write(allResults)
        f.close

        time.sleep(1)
        data.com1.disable()
        sys.exit()

    except Exception as exception:
        print(traceback.format_exc())
        print(exception)
        data.com1.disable()

if __name__ == "__main__":
    main()