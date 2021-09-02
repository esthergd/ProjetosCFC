from enlace import enlace


def main():
    try:
        com1 = enlace('/dev/ttyACM0')
        com1.enable()
        com1.rx.clearBuffer()
        listResult = []

        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()

        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer == b'\x':
                break
            elif rxBuffer == b'\xBB':
                com1.getData(2)

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()
