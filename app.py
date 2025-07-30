from flask import Flask, request, jsonify
from whatsapp.bot import processar_mensagem  # função que processa e envia mensagem

app = Flask(__name__)

@app.route('/webhook/messages-upsert', methods=['POST'])
def messages_upsert():
    data = request.get_json()
    mensagem = data.get('data')
    key = mensagem.get('key')
    remote_jid = key.get('remoteJid')
    from_me = key.get('fromMe')
    texto = mensagem.get('message', {}).get('conversation', '').strip().lower()

    
    processar_mensagem(texto, remote_jid, from_me)

    print("Recebido no webhook messages-upsert:", data)
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)