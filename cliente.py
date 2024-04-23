import requests
import threading
import time
import os
import json
import datetime

def verificaDados():
    url_consume = 'http://127.0.0.1:8081/dispositivos'  # Rota para consumir a API

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
        
def pegar_horario_atual_json():
    agora = datetime.datetime.now()
    hora = agora.hour
    minutos = agora.minute
    segundos = agora.second
    
    # Criando um dicionário com os valores
    horario_dict = {
        "hora": hora,
        "minutos": minutos,
        "segundos": segundos
    }
    
    return horario_dict

def enviarRequisicao(num, comando):
    url_publish = 'http://127.0.0.1:8081/requisicoes'

    try:
        # Preparar os dados para publicar na API
        payload = {'temperatura': comando, 'id': num}  # Supondo que data_udp é uma sequência de bytes
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
    
def menu():
    while True:
        num = int(input('escreva o número do cliente que deseja mandar um comando: '))
        comando = int(input("digite\n1 - Ligar\n 2 - Desligar"))
        if comando == 1:
            comando = 'Ligar'
        else:
            comando = 'Desligar'
        enviarRequisicao(num, comando)
    
def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')  # Limpa o terminal no Windows
    else:
        # Limpa o terminal em sistemas Unix (Linux, macOS, etc.)
        os.system('clear')

def main():
    while True:
        menu_thread = threading.Thread(target=menu)
        menu_thread.start()
        time.sleep(10)
        verificaDados()
    
if __name__=="__main__":
    main()