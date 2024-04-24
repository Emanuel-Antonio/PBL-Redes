import threading
import socket
import time
import random
import os

# Configurações do cliente
SERVER_IP = '192.168.1.105'   # Endereço IP do servidor de destino, no caso, broker
TCP_PORT = 65432              # Porta TCP do servidor
UDP_PORT = 65433              # Porta UDP do servidor para resposta
MENSAGE = 'Ligar'
BRILHO = '100'

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect((SERVER_IP, TCP_PORT))
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
    
def enviarDadoUdp(client_udp):
    global BRILHO
    global MENSAGE
    while True:
        try:
            #print(BRILHO)
            if MENSAGE == 'Desligar':
                client_udp.sendto(b"Desligar", (SERVER_IP, UDP_PORT))
            else:
                #temperatura = gerarTemperaturaFake()
                #temperatura_str = str(temperatura)
                client_udp.sendto(BRILHO.encode(), (SERVER_IP, UDP_PORT))
            time.sleep(5)
        except Exception as e:
            print(e)
        
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
            print('\nNão foi possível permanecer conectado no servidor!\n', e)
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def enviarMensagem(client, username):
    while True:
        try:
            msg = "conectado"
            client.send(f'<{username}> {msg}'.encode())
        except:
            return
        
def gerarTemperaturaFake():
    # Gerar uma temperatura fictícia entre -20°C e 40°C
    return round(random.uniform(-20, 40), 2)

def menu():
    global MENSAGE
    global BRILHO
    while True:
        print("digite\n1 - Ligar\n2 - Desligar\n3 - Mudar Brilho\n4 - Visualizar Dados")
        n = int(input())
        if(n == 1):
            MENSAGE = "Ligar"
        elif(n == 2):
            MENSAGE = "Desligar"
        elif(n == 3):
            b = int(input('Brilho: '))   
            BRILHO = str(b)
        else:
            print("Brilho do dispositivo: {}\nStatus do dispositivo: {}".format(BRILHO, MENSAGE))
            b = input('Digite enter para solicitar outro comando!')
        print("Voce decidiu", MENSAGE, "o dispositivo")
        limpar_terminal()
 
def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')  # Limpa o terminal no Windows
    else:
        # Limpa o terminal em sistemas Unix (Linux, macOS, etc.)
        os.system('clear')

if __name__=="__main__":            
    main()