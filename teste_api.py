from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de mensagens (simulando uma fila de mensagens)
messages = []


@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        messages.append(message)
        return jsonify({'status': 'success', 'message': 'Mensagem publicada com sucesso'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Parâmetro "message" ausente'}), 400


@app.route('/consume', methods=['GET'])
def consume_message():
    if messages:
        message = messages.pop(0)
        return jsonify({'status': 'success', 'message': message}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Nenhuma mensagem disponível'}), 404


if __name__ == '__main__':
    app.run(debug=True)
