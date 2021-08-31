

from enlace import *
import time
import numpy as np
import time
import random

def main():
    try:
        com1 = enlace('/dev/ttyACM0')
        com1.enable()
        command1 = b'\x00'
        command2 = [b'\x00',b'\xFF']
        command3 = b'\x0F'
        command4 = b'\xF0'
        command5 = b'\xFF'
        command6 = [b'\xFF',b'\x00']

        n = random.randint(10,30)
        commands = [command1,command2,command3,command4,command5,command6]
        list_commands = []
        for i in range(n):
            list_commands += random.choice(commands)
            return list_commands

        com1.sendData(list_commands)
        print(list_commands)

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()