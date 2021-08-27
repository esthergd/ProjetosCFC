

from enlace import *
import time
import numpy as np
import time
import random

def main():
    try:
        com1 = enlace('/dev/ttyACM0')

        com1.enable()

        n = random.randint(10,30)
        commands = [b'00FF', b'00',b'0F',b'F0',b'FF00',b'FF']
        list_commands = list()
        for i in range (n):
            list_commands.append(random.choice(commands))
            commands_array = np.asarray(list_commands)
            return commands_array

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()