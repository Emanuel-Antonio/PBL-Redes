import socket

# Configurações do cliente
SERVER_IP = '192.168.1.105'   #Endereço IP do servidor de destino no caso broker
PORT = 65432                  # Porta do servidor

try:
    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Conecta ao servidor
        client_socket.connect((SERVER_IP, PORT))
        # Envia uma mensagem para o servidor
        client_socket.sendall(b'Ola, servidor TCP')
        # Recebe a resposta do servidor
        data = client_socket.recv(1024)

    print('Resposta do servidor:', data.decode())
except Exception as e:
    print('Erro:', e)
