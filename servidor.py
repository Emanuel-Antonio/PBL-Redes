import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta para escutar conexões

# Criação do socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Liga o socket ao endereço e porta especificados
    server_socket.bind((HOST, PORT))
    # Coloca o socket em modo de escuta
    server_socket.listen()
    print('Servidor TCP esperando por conexões...')
    # Aceita conexões de clientes
    conn, addr = server_socket.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            # Recebe dados do cliente
            data = conn.recv(1024)
            if not data:
                break
            print('Mensagem recebida do cliente:', data.decode())
            # Envia mensagem de volta para o cliente
            conn.sendall(data)
