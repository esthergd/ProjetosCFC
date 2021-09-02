

from enlace import *
import time
import numpy as np
import time
import random


def create_commands():
    commands = [b"\x00",b"\x00"b"\xFF",b"\x0F",b"\xF0",b"\xFF",b"\xFF"b"\x00"]
    n = random.randint(10,30)
    flagged_commands = []
    for i in range(n):
        command = random.choice(commands)
        if len(command) == 2:
            flagged_commands.append(b'\xBB')
        flagged_commands.append(command)
    flagged_commands.append(b'\xAA')
    flagged_commands_bytes = b''.join(flagged_commands)
    print(flagged_commands_bytes)
    return flagged_commands_bytes

def main():
    try:
        com1 = enlace('/dev/ttyACM0')

        com1.enable()

        com1.sendData(b'\xcc')

        txBuffer = create_commands() 

        com1.sendData(np.asarray(txBuffer))

        com1.disable()


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()





if __name__ == "__main__":
    main()
