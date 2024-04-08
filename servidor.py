import socket
from flask import Flask, request, jsonify
import json
import requests


# Configurações do servidor
SERVER_IP = '192.168.1.105'  # Endereço IP do servidor, no caso, broker
TCP_PORT = 65432             # Porta TCP do servidor
UDP_PORT = 65433             # Porta UDP do servidor para resposta

def main():
    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp_socket:
        # Associa o socket à porta TCP
        server_tcp_socket.bind((SERVER_IP, TCP_PORT))
        # Configura o socket para escutar conexões
        server_tcp_socket.listen()

        print("Servidor TCP esperando por conexões...")

        # Aceita uma conexão
        conn_tcp, addr_tcp = server_tcp_socket.accept()
        with conn_tcp:
            print('Conectado por TCP:', addr_tcp)
            # Recebe dados do cliente TCP
            data_tcp = conn_tcp.recv(1024)
            print('Mensagem recebida do cliente TCP:', data_tcp.decode())

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_udp_socket:
        # Associa o socket à porta UDP
        server_udp_socket.bind((SERVER_IP, UDP_PORT))

        print("Servidor UDP esperando por mensagens...")

        # Recebe dados do cliente UDP
        data_udp, addr_udp = server_udp_socket.recvfrom(1024)
        print('Conectado por TCP:', addr_udp)
        print('Mensagem recebida do cliente UDP:', data_udp.decode())

        # Salva a mensagem UDP em um arquivo JSON
        mensagem_udp = data_udp.decode()
        with open('mensagem_udp.json', 'w') as file:
            json.dump({'mensagem_udp': mensagem_udp}, file)
            
        # Carregar os dados do arquivo JSON
        with open('mensagem_udp.json', 'r') as file:
            data = json.load(file)

        # URL da API para enviar os dados
        url = 'http://127.0.0.1:5000/publish'

        # Fazer uma solicitação POST para a API com os dados do arquivo JSON
        response = requests.post(url, json=data) 
        print(response)   "
            
if __name__ == '__main__':
    main()
