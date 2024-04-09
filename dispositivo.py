import socket
import random

# Configurações do cliente
SERVER_IP = '192.168.1.105'   # Endereço IP do servidor de destino, no caso, broker
TCP_PORT = 65432              # Porta TCP do servidor
UDP_PORT = 65433              # Porta UDP do servidor para resposta
    
def generate_fake_temperature():
    # Gerar uma temperatura fictícia entre -20°C e 40°C
    return round(random.uniform(-20, 40), 2)

def main():
    
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

            # Criação do socket UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp_socket: 
                # Converte o número para string antes de enviar   
                temperatura = generate_fake_temperature()
                print(temperatura)
                # # Envia a temperatura para o servidor UDP 
                temperatura_str = str(temperatura)
                # # Envia uma mensagem para o servidor UDP
                client_udp_socket.sendto(temperatura_str.encode(), (SERVER_IP, UDP_PORT))

    except Exception as e:
        print('Erro:', e)
        
if __name__ == '__main__':
    main()
