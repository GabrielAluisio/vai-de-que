import requests
from utils.clima import definir_clima  # sua função que gera texto clima

def enviar_mensagem_whatsapp(texto):
    url = "http://127.0.0.1:8080/message/sendText/vou-de-que"  # URL da API do WhatsApp (local ou externa)
    headers = {
        "Content-Type": "application/json",
        "apikey": "16645164840"  # sua chave da API
    }
    payload = {
        "number": "5511932222897",
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


import requests
from utils.clima import definir_clima  # sua função que gera texto clima

cidade_atual = 'sao paulo'  # padrão inicial

def enviar_mensagem_whatsapp(texto):
    url = "http://127.0.0.1:8080/message/sendText/vai-de-que"  # sua URL API WhatsApp
    headers = {
        "Content-Type": "application/json",
        "apikey": "16645164840"  # sua chave da API
    }
    payload = {
        "number": "5511932222897",
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

def processar_mensagem(texto):
    global cidade_atual
    texto = texto.strip().lower()
    
    if texto.startswith('mudar cidade para '):
        nova_cidade = texto[len('mudar cidade para '):].strip()
        if nova_cidade:
            cidade_atual = nova_cidade
            enviar_mensagem_whatsapp(f"Cidade alterada para {cidade_atual.title()}!")
        else:
            enviar_mensagem_whatsapp("Você precisa informar o nome da cidade após 'mudar cidade para'.")
    
    elif texto == 'vou de que':
        resposta = definir_clima(cidade_atual)
        enviar_mensagem_whatsapp(resposta)
    
    else:
        enviar_mensagem_whatsapp("Por favor, digite 'mudar cidade para ...' ou 'vou de que'.")

