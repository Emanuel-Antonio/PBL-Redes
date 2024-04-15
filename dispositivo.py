import socket
import random
import time
import threading


# Configurações do cliente
SERVER_IP = '192.168.1.105'   # Endereço IP do servidor de destino, no caso, broker
TCP_PORT = 65432              # Porta TCP do servidor
UDP_PORT = 65433              # Porta UDP do servidor para resposta
MENSAGE = ''

    
def generate_fake_temperature():
    # Gerar uma temperatura fictícia entre -20°C e 40°C
    return round(random.uniform(-20, 40), 2)

def menu():
    global MENSAGE
    while True:
        print("(1) Ligar\n (2) Desligar\n")
        n = int(input())
        if(n == 1):
            MENSAGE = "ligar"
        else:
            MENSAGE = "desligar"

def main():
    menu_thread = threading.Thread(target=menu)
    menu_thread.start()
    global MENSAGE
    while True:
        try:
            
            # Criação do socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp_socket:
                # Conecta ao servidor TCP
                client_tcp_socket.connect((SERVER_IP, TCP_PORT))
                # Envia uma mensagem para o servidor TCP
                client_tcp_socket.sendall(b'Ola, servidor TCP')
                # Recebe a resposta do servidor TCP
                tcp_response = client_tcp_socket.recv(1024)
                print('Resposta do servidor (TCP):', tcp_response.decode())
                if(tcp_response.decode() == "desligar" or tcp_response.decode() == "ligar"):
                    MENSAGE = tcp_response.decode()
            if MENSAGE == "desligar":
                pass
            else:    
                # Criação do socket UDP
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp_socket: 
                    # Converte o número para string antes de enviar   
                    temperatura = generate_fake_temperature()
                    print(temperatura)
                    # # Envia a temperatura para o servidor UDP 
                    temperatura_str = str(temperatura)
                    # # Envia uma mensagem para o servidor UDP
                    client_udp_socket.sendto(temperatura_str.encode(), (SERVER_IP, UDP_PORT))
                    
            time.sleep(1)

        except Exception as e:
            print('Erro: Broker desconectado')
            pass
        
if __name__ == '__main__':
    main()
