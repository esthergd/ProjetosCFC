#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código!

from enlace import *
import time
import numpy as np
import time
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5')

        #Criamos um local para salvarmos a cópia da imagem
        imagemCopia = "./imagemCopia.jpg"

        #Carregamos a imagem no txBuffer
        with open('ferroImagem.jpg', 'rb') as imagem:
            txBuffer = imagem.read()
        print(len(txBuffer))

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar
        #aqui você deverá gerar os dados a serem transmitidos.
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o
        #nome de txBuffer. Ela sempre irá armazenar os dados a serem enviados.
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        print("Comunicação aberta")

        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
        print("A transmissão irá começar")
        #Iniciamos a contagem do tempo do processo
        ini = time.time()
        com1.sendData(np.asarray(txBuffer))

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        print(txSize)
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("A recepção vai começar")
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        #print("recebeu {}" .format(rxBuffer))

        #Salvar uma copia da imagem
        print("Salvando dados no arquivo")
        print(" - {}".format(imagemCopia))
        print("-------------------------")
        f = open(imagemCopia, 'wb')
        f.write(rxBuffer)
        f.close

        #Finalizamos a contagem do tempo
        end = time.time() 

        #Imprime o tempo total decorrido
        print ("Tempo total decorrido: {}".format(end - ini))

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()