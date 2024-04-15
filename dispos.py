import threading
import socket
import time
import random


def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.connect(('192.168.1.105', 65432))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = '192.168.1.105'
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])
    thread3 = threading.Thread(target=sendMessagesUdp, args=[client_udp])
    thread4 = threading.Thread(target=menu)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

def menu():
    global MENSAGE
    while True:
        print("(1) Ligar\n (2) Desligar\n")
        n = int(input())
        if(n == 1):
            MENSAGE = "ligar"
        else:
            MENSAGE = "desligar"
            
def sendMessagesUdp(client_udp):
    while True:
        # # Envia uma mensagem para o servidor UDP
        client_udp.sendto(b"20", ('192.168.1.105', 65433))
        time.sleep(1)
        
def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, username):
    while True:
        try:
            msg = "boa noite"
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()