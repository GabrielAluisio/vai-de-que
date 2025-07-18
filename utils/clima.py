import requests
from datetime import datetime, timedelta

'''Recomendo ir com roupas leves, como camiseta e shorts. Está calor!

Recomendo usar roupas confortáveis — o clima está agradável.

Recomendo uma blusa leve ou um casaco fino. Está um pouco frio!

Recomendo usar um casaco ou jaqueta para se proteger. Está frio!

Recomendo um casaco pesado, cachecol e luvas — o frio está intenso!'''







#abe4201233b3a20dca48e1a3498d45d3

def acessar_api(api_key, city):


    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)

    return response.json()








def definir_hora(city_name):
    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    dados = acessar_api(api_key, city_name)

    dados_list = dados['list']

    horarios_desejados = ['06:00:00', '12:00:00', '18:00:00']
    previsoes_filtradas = {}

    for itens in dados_list:
        dt_txt = itens['dt_txt']
        hora = dt_txt.split()[1]
        if hora in horarios_desejados:
            previsoes_filtradas[hora] = itens 

    print(previsoes_filtradas)


















def obter_previsao(city_name):

    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    dados = acessar_api(api_key, city_name)

    if dados['cod'] == 401:
        print('Problema durante a requisição\n'
            f"Mensagem: {dados['message']}")
        
    elif dados['cod'] != 404:
        clima = dados['weather'][0]['main']
        temperatura = dados['main']['temp']
        sensacao = dados['main']['feels_like']
        vento = dados['wind']['speed']
        umidade = dados['main']['humidity']

        def sugestao():

            def pontuar_vento(velocidade):
                if velocidade <= 2:
                    return 0
                elif velocidade <= 5: 
                    return 1
                elif velocidade <= 10:
                    return 2
                else:
                    return 3

            def pontuar_umidade(valor, temperatura):
                if temperatura >= 25:
                    if valor <= 60:
                        return 0
                    elif valor <= 80:
                        return 1
                    else:
                        return 2
                else:
                    if valor <= 30:
                        return 0
                    elif valor <= 60:
                        return 1
                    elif valor <= 80:
                        return 2
                    else:
                        return 3
            
                

            pontos = 0 
            pontos += pontuacao_clima.get(clima, 2)
            pontos += pontuar_vento(vento)
            pontos += pontuar_umidade(umidade, temperatura)
            pontos += pontuar_temperatura(temperatura) 
            pontos += pontuar_sensacao(sensacao, umidade)
            
            print(pontos)
            
            print(pontuacao_clima.get(clima, 2),
                pontuar_vento(vento), 
                pontuar_umidade(umidade, temperatura), 
                pontuar_temperatura(temperatura), 
                pontuar_sensacao(sensacao, umidade))

            def sugestao_roupa(pontos):
                if pontos <= 4:
                    return "Pode ir de roupa leve: camiseta e shorts"
                elif pontos <= 8:
                    return "Recomendo uma blusa fina"
                elif pontos <= 13:
                    return "Use casaco ou jaqueta"
                elif pontos <= 17:
                    return "Melhor ir de roupa bem quente, tipo casaco pesado e cachecol"
                else: 
                    return "Muito frio! Cachecol, luvas e gorro são recomendados"
                
            print(sugestao_roupa(pontos))


        sugestao()
        print(dados)
    else:
        print('Cidade não encontrada!')
    