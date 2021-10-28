#importe as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
from suaBibSignal import *

def getFreq(dic, key):

    freqx = dic[f'{key}'][0]
    freqy = dic[f'{key}'][1]

    return freqx, freqy


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    dictFreq = {'1':[1209, 697], '2':[1336, 697], '3':[1477, 697], '4':[1209, 770], '5':[1336, 770], '6':[1477, 770],
    '7':[1209, 852], '8':[1336, 852], '9':[1477, 852], '0':[1336, 941]}
    #declare um objeto da classe da sua biblioteca de apoio (cedida)  
    signal = signalMeu()
    fs = 44100 #declare uma variavel com a frequencia de amostragem, sendo 44100
    amplitude = 1.5
    time = 2

    t = np.linspace(-time/2, time/2, time*fs)
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    duration = 2   
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    number = input('Digite uma tecla de 0 a 9: ')

    f1, f2 = getFreq(dictFreq, number)

    x1, s1 = signal.generateSin(f1, amplitude, time, fs)
    x2, s2 = signal.generateSin(f2, amplitude, time, fs)

    tone = s1 + s2


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(number))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides

    y = s1 + s2
    #printe o grafico no tempo do sinal a ser reproduzido
    plt.plot(t, y, '.-')
    plt.xlim(0, 0.01)
    X, Y = signal.calcFFT(y, fs)
    plt.figure()
    plt.stem(X,np.abs(Y))
    plt.xlim(0, 2000)

    # reproduz o som
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
