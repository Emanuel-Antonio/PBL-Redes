import socket

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta do servidor

# Criação do socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Conecta ao servidor
    client_socket.connect((HOST, PORT))
    # Envia uma mensagem para o servidor
    client_socket.sendall(b'Ola, servidor TCP')
    # Recebe a resposta do servidor
    data = client_socket.recv(1024)

print('Resposta do servidor:', data.decode())
