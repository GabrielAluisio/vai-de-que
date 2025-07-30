import requests
from utils.clima import definir_clima

cidade_atual = 'sao paulo' 
meu_numero = '5511932222897@s.whatsapp.net'


def processar_mensagem(texto, remote_jid, from_me):
    global cidade_atual

    if (not from_me) or (from_me and remote_jid == meu_numero):

        texto = texto.strip().lower()
        
        if texto.startswith('mudar cidade para '):
            nova_cidade = texto[len('mudar cidade para '):].strip()
            if nova_cidade:
                cidade_atual = nova_cidade
                enviar_mensagem_whatsapp(remote_jid, f"Cidade alterada para {cidade_atual.title()}!")
            else:
                enviar_mensagem_whatsapp(remote_jid, "Você precisa informar o nome da cidade após 'mudar cidade para'.")
        
        elif texto == 'vou de que' or texto == 'vou de que?':
            resposta = definir_clima(cidade_atual)
            enviar_mensagem_whatsapp(remote_jid, resposta)
        
        elif texto == 'comandos' or texto == 'comando' or texto == 'oi, bot' or texto == 'oi bot':
            enviar_mensagem_whatsapp(remote_jid,
    "Oi! 👋 Eu sou seu assistente de clima.\n"
    "Você pode me pedir a previsão do tempo dizendo 'vou de que?'.\n"
    "Também posso mudar a cidade para você, basta digitar: 'mudar cidade para [nome da cidade]'."
)



def enviar_mensagem_whatsapp(numero, texto):
    url = "https://vou-de-que.onrender.com/message/sendText/vou-de-que"  # URL API WhatsApp
    headers = {
        "Content-Type": "application/json",
        "apikey": "16645164840"  # chave da API
    }
    payload = {
        "number": numero.replace('@s.whatsapp.net',''),
        "options": {
            "delay": 1000,
            "presence": "composing"
        },
        "textMessage": {
            "text": texto
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Status:", response.status_code)
    print("Resposta:", response.text)


