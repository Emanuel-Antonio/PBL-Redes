import socket, json, requests, threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de mensagens (simulando uma fila de mensagens)
messages = []
lock = threading.Lock()

@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        with lock:
            messages.append(message)
        return jsonify({'status': 'success', 'message': 'Mensagem publicada com sucesso'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Parâmetro "message" ausente'}), 400

@app.route('/consume', methods=['GET'])
def consume_message():
    with lock:
        if messages:
            message = messages.pop(0)
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Nenhuma mensagem disponível'}), 404

def tcp_server():
    # Configurações do servidor
    SERVER_IP = '192.168.1.105'  # Endereço IP do servidor, no caso, broker
    TCP_PORT = 65432             # Porta TCP do servidor

    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp_socket:
        # Associa o socket à porta TCP
        server_tcp_socket.bind((SERVER_IP, TCP_PORT))
        # Configura o socket para escutar conexões
        server_tcp_socket.listen()

        print("Servidor TCP esperando por conexões...")

        # Loop infinito para aceitar conexões
        while True:
            # Aceita uma conexão
            conn_tcp, addr_tcp = server_tcp_socket.accept()
            with conn_tcp:
                print('Conectado por TCP:', addr_tcp)
                # Recebe dados do cliente TCP
                data_tcp = conn_tcp.recv(1024)
                print('Mensagem recebida do cliente TCP:', data_tcp.decode())

def udp_server():
    # Configurações do servidor
    SERVER_IP = '192.168.1.105'  # Endereço IP do servidor, no caso, broker
    UDP_PORT = 65433             # Porta UDP do servidor para resposta

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_udp_socket:
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

def enviar_para_api(data_udp):
    url_publish = 'http://127.0.0.1:5000/publish'
    url_consume = 'http://127.0.0.1:5000/consume'  # Rota para consumir a API

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

def main():
    
    # Inicia os servidores TCP e UDP em threads separadas
    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread = threading.Thread(target=udp_server)
    tcp_thread.start()
    udp_thread.start()
    
    # Inicia a aplicação Flask
    app.run(debug=True)
    
if __name__ == '__main__':
    main()
    