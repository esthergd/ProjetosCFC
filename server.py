import enlace


def main():
    try:
        com1 = enlace('/dev/ttyACM0')
        com1.enable()

        print("Comunicação aberta")

        print("A transmissão irá começar")