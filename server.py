from enlace import enlace


def main():
    try:
        com1 = enlace('/dev/ttyACM0')
        com1.enable()
        com1.rx.clearBuffer()
        resultados = []

        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()

        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer == b'\xAA':
                break
            elif rxBuffer == b'\xBB':
                rxBuffer, nRx = com1.getData(2)
                resultados.append(rxBuffer)
            else:
                resultados.append(rxBuffer)
        print(resultados)

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()
