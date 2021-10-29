import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
import time
from suaBibSignal import *
import peakutils

#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
dictFreq = {'1':[1209, 697], '2':[1336, 697], '3':[1477, 697], '4':[1209, 770], '5':[1336, 770], '6':[1477, 770],
    '7':[1209, 852], '8':[1336, 852], '9':[1477, 852], '0':[1336, 941], 'A':[1633, 697], 'B':[1633, 770], 'C':[1633, 852], 'D':[1633, 941]}

def pressedNmbr(freqs):
    if int(freqs[0]) == 697:
        if int(freqs[1]) ==1209:
            return '1'
        elif int(freqs[1]) ==1336:
            return '2'
        elif int(freqs[1]) ==1477:
            return '3'
    elif int(freqs[0]) ==770:
        if int(freqs[1]) ==1209:
            return '4'
        elif int(freqs[1]) ==1336:
            return '5'
        elif int(freqs[1]) == 1477:
            return '6'
    elif int(freqs[0]) ==852:
        if int(freqs[1]) ==1209:
            return '7'
        elif int(freqs[1]) ==1336:
            return '8'
        elif int(freqs[1]) ==1477:
            return '9'
    elif int(freqs[0]) == 941:
        return '0'
    else:
        print ("Error")
        

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    signal = signalMeu()
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = 1
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa

    print('A Captação irá começar em 3 segundo')
    time.sleep(1)

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera

    print('A gravação foi iniciada')
   
    #faca um print informando que a gravacao foi inicializada
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    duration = 4
    numAmostras = duration * fs
   
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    for dado in audio:
        dados.append(dado[0])

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(-duration/2, duration/2, duration*fs)

    # plot do gravico  áudio vs tempo!
    plt.plot(tempo, audio)
    plt.grid()
    plt.title('Audio no tempo')
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.xlim(0, 1000)
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
    freqs = []
    index = peakutils.indexes(np.abs(yf), thres=0.8, min_dist=20)
    print("index de picos {}" .format(index))
    for freq in xf[index]:
        freqs.append(freq)
        print("freq de pico sao {}" .format(freq))

    #printe os picos encontrados! 
    tecla = pressedNmbr(freqs)

    print(f"A tecla apertada foi {tecla}")
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
