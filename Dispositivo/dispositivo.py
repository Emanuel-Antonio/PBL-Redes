import threading
import socket
import time
import random
import os

# Configurações do cliente
IP = '192.168.1.105'   # Endereço IP do servidor de destino, no caso, broker
TCP_PORT = 65432              # Porta TCP do servidor
UDP_PORT = 65433              # Porta UDP do servidor para resposta
MENSAGE = 'Ligar'
BRILHO = '100'

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect((IP, TCP_PORT))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = "Emanuel"
    print('\nDispositivo Conectado')

    thread1 = threading.Thread(target=receberTcp, args=[client])
    thread2 = threading.Thread(target=enviarMensagem, args=[client, username])
    thread3 = threading.Thread(target=enviarDadoUdp, args=[client_udp])
    thread4 = threading.Thread(target=menu)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

def menu():
    global MENSAGE
    global BRILHO
    while True:
        try:
            print("===========================================\n1 - Ligar\n2 - Desligar\n3 - Mudar Brilho\n4 - Visualizar Dados\n===========================================")
            n = int(input("Digite o Comando: "))
            if MENSAGE == 'Desligar' and n == 3:
                n = 0
                print("Primeiro ligue o dispositivo para alterar seu Brilho!")
            while n < 1 or n > 4:
                n = int(input("Digite um comando válido: "))
                if MENSAGE == 'Desligar' and n == 3:
                    n = 0
                    print("Primeiro ligue o dispositivo para alterar seu Brilho!")
            print("===========================================")
            if(n == 1):
                MENSAGE = "Ligar"
                print("Ligando dispositivo ...")
                b = input('Digite enter para solicitar outro comando!\n===========================================')
                while b != '':
                    b = input('Digite enter para solicitar outro comando!\n===========================================')
            elif(n == 2):
                MENSAGE = "Desligar"
                print("Desligando Dispositivo ...")
                b = input('Digite enter para solicitar outro comando!\n===========================================')
                while b != '':
                    b = input('Digite enter para solicitar outro comando!\n===========================================')
            elif(n == 3):
                b = int(input('Brilho: ')) 
                while b > 100 or b < 0:
                    b = int(input('Digite um valor válido para o Brilho: '))   
                BRILHO = str(b)
                print("Mudança efetuada com sucesso ...")
                b = input('Digite enter para solicitar outro comando!\n===========================================')
                while b != '':
                    b = input('Digite enter para solicitar outro comando!\n===========================================')
            else:
                print("Brilho do dispositivo: {}\nStatus do dispositivo: {}".format(BRILHO, MENSAGE[:-1] + 'do'))
                b = input('Digite enter para solicitar outro comando!\n===========================================')
                while b != '':
                    b = input('Digite enter para solicitar outro comando!\n===========================================')
        except ValueError as e:
            pass
        limpar_terminal()

def receberTcp(client):
    global MENSAGE
    global BRILHO
    while True:
        try:
            msg = client.recv(2048).decode()
            #print(msg+'\n')
            if msg == 'Desligar':
                MENSAGE = msg
            elif msg == 'Ligar':
                MENSAGE = 'Ligar'
            else: 
                BRILHO = msg
                MENSAGE = 'Ligar' 
        except Exception as e:
            print('\nBroker desconectado ...\n')
            print('Pressione <Enter> Para continuar...')
            try:
                client.close()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((IP, TCP_PORT))
            except Exception as e:
                pass

def enviarMensagem(client, username):
    while True:
        try:
            msg = "conectado"
            client.send(f'<{username}> {msg}'.encode())
        except:
            return
          
def enviarDadoUdp(client_udp):
    global BRILHO
    global MENSAGE
    while True:
        try:
            #print(BRILHO)
            if MENSAGE == 'Desligar':
                client_udp.sendto(b"Desligado", (IP, UDP_PORT))
            else:
                #temperatura = gerarTemperaturaFake()
                #temperatura_str = str(temperatura)
                client_udp.sendto(BRILHO.encode(), (IP, UDP_PORT))
            time.sleep(0.5)
        except Exception as e:
            pass
 
def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')  # Limpa o terminal no Windows
    else:
        # Limpa o terminal em sistemas Unix (Linux, macOS, etc.)
        os.system('clear')

if __name__=="__main__":            
    main()