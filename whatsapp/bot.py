import requests
from utils.clima import definir_clima


def iniciar_bot():

    print("Conectando ao WhatsApp...")

    texto = definir_clima('tokyo')

    url = "http://127.0.0.1:8080/message/sendText/vou-de-que" 
    headers = {
        "Content-Type": "application/json",
        "apikey": "16645164840"  
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


