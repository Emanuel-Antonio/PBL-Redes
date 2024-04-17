import threading
import socket
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

clients = []
dispositivosConectados = []
# Lista de mensagens (simulando uma fila de mensagens)
messages = []
lock = threading.Lock()

# Lista de usuários
dispositivos = []

# Rota para listar todos os usuários
@app.route('/dispositivos', methods=['GET'])
def get_usuarios():
    return jsonify(dispositivos)

# Rota para obter um usuário por ID
@app.route('/dispositivos/<int:dispositivo_id>', methods=['GET'])
def get_usuario(dispositivo_id):
    dispositivo = next((dispositivo for dispositivo in dispositivos if dispositivo['id'] == dispositivo_id), None)
    if dispositivo:
        return jsonify(dispositivo)
    return jsonify({'message': 'Sensor não encontrado'}), 404

# Rota para criar um novo usuário
@app.route('/dispositivos', methods=['POST'])
def criar_usuario():
    novo_dispositivo = request.json
    novo_dispositivo['id'] = len(dispositivos) + 1
    dispositivos.append(novo_dispositivo)
    return jsonify(novo_dispositivo), 201

# Rota para atualizar um usuário existente
@app.route('/dispositivo/<int:dispositivo_id>', methods=['PUT'])
def atualizar_usuario(dispositivo_id):
    dispositivo = next((dispositivo for dispositivo in dispositivos if dispositivo['id'] == dispositivo_id), None)
    if not dispositivo:
        return jsonify({'message': 'Sensor não encontrado'}), 404
    dados_atualizados = request.json
    dispositivo.update(dados_atualizados)
    return jsonify(dispositivo)

# Rota para excluir um usuário
@app.route('/dispositivo/<int:dispositivo_id>', methods=['DELETE'])
def excluir_usuario(dispositivo_id):
    global dispositivos
    dispositivos = [dispositivo for dispositivo in dispositivos if dispositivo['id'] != dispositivo_id]
    return jsonify({'message': 'Dispositivo excluído com sucesso'})

def enviar_para_api(data_udp):
    url_publish = 'http://127.0.0.1:8081/dispositivos'

    try:
        # Preparar os dados para publicar na API
        payload = {'temperatura': data_udp.decode()}  # Supondo que data_udp é uma sequência de bytes
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
    except Exception as e:
        print('Erro ao enviar/receber dados para/de API:', e)

def atualizar_dado_api(dado_udp, id):
    url_update = 'http://127.0.0.1:8081/dispositivo/{}'.format(id)

    try:
        # Preparar os dados para atualizar na API
        payload = {'temperatura': dado_udp.decode()}
        json_payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}

        # Enviar requisição PUT para atualizar o dado na API
        response_update = requests.put(url_update, data=json_payload, headers=headers)

        # Verificar se a atualização foi bem-sucedida
        if response_update.status_code == 200:
            print("Dado atualizado com sucesso na API.")
            print(json_payload)
        else:
            print("Erro ao atualizar o dado na API:", response_update.status_code)
            return
    except Exception as e:
        print('Erro ao enviar/receber dados para/de API:', e)
        
def remover_dispositivo(dado_id):
    url_delete = 'http://127.0.0.1:8081/dispositivo/{}'.format(dado_id)

    try:
        # Enviar requisição DELETE para remover o dado da API
        response_delete = requests.delete(url_delete)

        # Verificar se a remoção foi bem-sucedida
        if response_delete.status_code == 200:
            print("Dado removido com sucesso da API.")
        else:
            print("Erro ao remover o dado da API:", response_delete.status_code)
            return
    except Exception as e:
        print('Erro ao enviar/receber dados para/de API:', e)


def verificaRequisição():
    url_consume = 'http://127.0.0.1:8081/consumir'  # Rota para consumir a API

    try:
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
        tcp_thread = threading.Thread(target=tcp_udp_server)
        tcp_thread.start()

        # Inicia a aplicação Flask
        app.run(port=8081, debug=True)

    except Exception as e:
        print('Erro:', e)
        
def tcp_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server.bind(('0.0.0.0', 65432))
        server_udp.bind(("0.0.0.0", 65433))
        server.listen()
    except:
        return print("Servidor Funcionando")
    while True:
        client, addr = server.accept()
        clients.append(client)
        
        thread = threading.Thread(target=selecaoMensagem, args=[client])
        thread2 = threading.Thread(target=receberTcp, args=[client])
        thread3 = threading.Thread(target=receberUdp, args=[server_udp])
        thread.start()
        thread2.start()
        thread3.start()
                
def receberUdp(server_udp):
    global dispositivosConectados
    while True:
        # Recebe dados do cliente UDP
        data_udp, addr_udp = server_udp.recvfrom(1024)
        print('Conectado por UDP:', addr_udp)
        print('Mensagem recebida do cliente UDP:', data_udp.decode())
        if(data_udp.decode() != "Desligar"):
            if(addr_udp not in dispositivosConectados):
                dispositivosConectados.append(addr_udp)
                enviar_para_api(data_udp)
            else:
                atualizar_dado_api(data_udp, dispositivosConectados.index(addr_udp) + 1)
        else:
            remover_dispositivo(dispositivosConectados.index(addr_udp) + 1)
            dispositivosConectados.remove(addr_udp)
            
def receberTcp(client):
    data_tcp = client.recv(1024)
    print('Mensagem recebida do cliente TCP:', data_tcp.decode())
                    
def selecaoMensagem(client):
    while True:
        try:
            num = int(input('\ncliente 1\ncliente 2\n'))
            msg = b'Desligar'
            transmitir(msg, num)
        except:
            removerCliente(client)
            break

def transmitir(msg, num):
    try:
        clients[num - 1].send(msg)
    except:
        removerCliente(clients[num -1])


def removerCliente(client):
    clients.remove(client)

if __name__ == "__main__":
    main()
