from flask import Flask, request, jsonify
from whatsapp.bot import processar_mensagem  # função que processa e envia mensagem

app = Flask(__name__)

@app.route('/webhook/messages-upsert', methods=['POST'])
def messages_upsert():
    data = request.get_json()
    print("Recebido no webhook messages-upsert:", data)
    
    texto_recebido = data.get('data', {}).get('message', {}).get('conversation', '').strip().lower()
    
    if texto_recebido:
        processar_mensagem(texto_recebido)  # processa qualquer mensagem recebida
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)