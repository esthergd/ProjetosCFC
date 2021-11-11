import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from suaBibSignal import *
from funcoes_LPF import *

#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

def normalize(signal):
    signal[:,0] = signal[:,0]/abs(signal[:,0]).max()
    signal[:,1] = signal[:,1]/abs(signal[:,1]).max()
    return signal

def main():

    signal = signalMeu()

    data, samplerate = sf.read('teste.wav')

    audioNormalized = normalize(data)
    duration = len(audioNormalized)/samplerate

    t = np.linspace(0.0, duration, len(audioNormalized))

    #Graf 1 - Sinal de audio original por tempo
    plt.figure(figsize = (15, 10))
    plt.plot(t, audioNormalized)
    plt.title('Sinal de áudio original normalizado por tempo')
    plt.show()
    
    fcut = 4000

    audioFiltered = LPF(audioNormalized[:,0], fcut, samplerate)

    #Graf 2 - Sinal de audio filtrado por tempo 
    plt.figure(figsize = (15, 10))
    plt.plot(t, audioFiltered)
    plt.title('Sinal de áudio filtrado por tempo. ')
    plt.show() 

    signal.plotFFT(audioFiltered, samplerate, 'Sinal Filtrado')

    #Graf 3 - Sinal de audio filtrado por frequencia

    port = 14000

    time, amp = signal.generateSin(port, 1, 5, samplerate)

    time = time[0:214503]
    amp = amp[0:214503]

    mod = amp * audioFiltered
    dmod = mod * amp

    #Graf 4 - sinal de audio modulado por dominio tempo
    plt.figure(figsize = (15, 10))
    plt.plot(t, mod)
    plt.title('Sinal de áudio modulado por tempo ')
    plt.show() 

    signal.plotFFT(mod, samplerate, 'Sinal Modulado')

    #Graf 5 - Sinal modulado por frequencia

    signal.plotFFT(dmod, samplerate,'Sinal Demodulado')

    #Graf 6 - Sinal demodulado por frequencia

    audioFiltered2 = LPF(dmod, fcut, samplerate)

    signal.plotFFT(audioFiltered2, samplerate, 'Sinal Demodulado e Filtrado')

    sd.play(audioFiltered2, samplerate)
    sd.wait()

    sys.exit()

if __name__ == "__main__":
    main()
    