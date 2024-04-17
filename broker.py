import socket
import json
import requests
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de mensagens (simulando uma fila de mensagens)
messages = []
lock = threading.Lock()

@app.route('/publicar', methods=['POST'])
def publish_message():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        with lock:
            messages.append(message)
        return jsonify({'status': 'success', 'message': 'Mensagem publicada com sucesso'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Parâmetro "message" ausente'}), 400

@app.route('/consumir', methods=['GET'])
def consume_message():
    with lock:
        if messages:
            message = messages.pop(0)
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Nenhuma mensagem disponível'}), 404

def tcp_server():
    # Configurações do servidor
    SERVER_IP = '0.0.0.0'     # Endereço IP do servidor, no caso, broker
    TCP_PORT = 7777           # Porta TCP do servidor

    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp_socket:
        try:
            # Associa o socket à porta TCP
            server_tcp_socket.bind((SERVER_IP, TCP_PORT))
            # Configura o socket para escutar conexões
            server_tcp_socket.listen()

            print("Servidor TCP esperando por conexões...")

            # Loop infinito para aceitar conexões
            i = 0
            while True:
                # Aceita uma conexão
                conn_tcp, addr_tcp = server_tcp_socket.accept()
                with conn_tcp:
                    print('Conectado por TCP:', addr_tcp)
                    # Recebe dados do cliente TCP
                    data_tcp = conn_tcp.recv(1024)
                    print('Mensagem recebida do cliente TCP:', data_tcp.decode())
                    
                    '''i += 1
                    # Envia uma mensagem de volta para o cliente
                    if i == 15:
                        message_to_send = "desligar"
                        conn_tcp.sendall(message_to_send.encode())
                    if i == 20:
                        message_to_send = "ligar"
                        conn_tcp.sendall(message_to_send.encode())
                    else:
                        message_to_send = "ligar"
                        conn_tcp.sendall(message_to_send.encode())'''
                        
        except Exception as e:
            pass

def udp_server():
    # Configurações do servidor
    SERVER_IP = '0.0.0.0'  # Endereço IP do servidor, no caso, broker
    UDP_PORT = 65433             # Porta UDP do servidor para resposta

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_udp_socket:
        try:
            # Associa o socket à porta UDP
            server_udp_socket.bind((SERVER_IP, UDP_PORT))

            print("Servidor UDP esperando por mensagens...")

            # Loop infinito para receber mensagens
            while True:
                # Recebe dados do cliente UDP
                data_udp, addr_udp = server_udp_socket.recvfrom(1024)
                print('Conectado por UDP:', addr_udp)
                print('Mensagem recebida do cliente UDP:', data_udp.decode())

                # Envia os dados UDP para a API
                enviar_para_api(data_udp)
        except Exception as e:
            pass
        
def enviar_para_api(data_udp):
    url_publish = 'http://127.0.0.1:8081/publicar'
    url_consume = 'http://127.0.0.1:8081/consumir'  # Rota para consumir a API

    try:
        # Preparar os dados para publicar na API
        payload = {'message': data_udp.decode()}  # Supondo que data_udp é uma sequência de bytes
        json_payload = json.dumps(payload)  # Convertendo para JSON
        headers = {'Content-Type': 'application/json'}

        # Publicar na API
        response_publish = requests.post(url_publish, data=json_payload, headers=headers)

        # Verificar se a publicação foi bem-sucedida
        if response_publish.status_code == 201:
            print("Dados UDP enviados com sucesso para a API.")
            print(json_payload)
        else:
            print("Erro ao enviar os dados UDP para a API:", response_publish.status_code)
            return

        # Consumir a API para obter a mensagem recém-publicada
        response_consume = requests.get(url_consume)

        # Verificar se a mensagem foi consumida com sucesso
        if response_consume.status_code == 200:
            consumed_message = response_consume.json()

            print("Mensagem consumida da API:", consumed_message)
        else:
            print("Erro ao consumir a API:", response_consume.status_code)
    except Exception as e:
        print('Erro ao enviar/receber dados para/de API:', e)

def main():

    try:
        # Inicia os servidores TCP e UDP em threads separadas
        tcp_thread = threading.Thread(target=tcp_server)
        udp_thread = threading.Thread(target=udp_server)
        tcp_thread.start()
        udp_thread.start()

        # Inicia a aplicação Flask
        app.run(port=8081, debug=True)

    except Exception as e:
        print('Erro:', e)

if __name__ == '__main__':
    main()