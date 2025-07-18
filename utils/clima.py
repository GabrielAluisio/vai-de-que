import requests
from datetime import datetime, timedelta


'''Recomendo ir com roupas leves, como camiseta e shorts. Está calor!

Recomendo usar roupas confortáveis — o clima está agradável.

Recomendo uma blusa leve ou um casaco fino. Está um pouco frio!

Recomendo usar um casaco ou jaqueta para se proteger. Está frio!

Recomendo um casaco pesado, cachecol e luvas — o frio está intenso!'''







#abe4201233b3a20dca48e1a3498d45d3

def api_forecast(api_key, city):

    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    response_forecast = requests.get(url_forecast)

    return response_forecast.json()
"""
{'06:00:00': {'dt': 1753164000, 'main': {'temp': 16.94, 'feels_like': 16.52, 'temp_min': 16.94, 'temp_max': 16.94, 'pressure': 1017, 'humidity': 70}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 0}, 'wind': {'speed': 1.19, 'deg': 32, 'gust': 1.08},}, 
'12:00:00': {'dt': 1753185600, 'main': {'temp': 18.49, 'feels_like': 17.86, 'temp_min': 18.49, 'temp_max': 18.49, 'pressure': 1019, 'humidity': 56}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 0}, 'wind': {'speed': 1.15, 'deg': 29, 'gust': 1.42},}, 
'18:00:00': {'dt': 1753207200, 'main': {'temp': 27.59, 'feels_like': 26.52, 'temp_min': 27.59, 'temp_max': 27.59, 'pressure': 1015, 'humidity': 22}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 0}, 'wind': {'speed': 1.87, 'deg': 198, 'gust': 3.26},}}"""

def api_weather(api_key, city):

    url_weather = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric"

    response_weather = requests.get(url_weather)

    return response_weather.json() 


def definir_temperatura(city_name):
    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    dadosF = api_forecast(api_key, city_name)
    dadosW = api_weather(api_key, city_name)

    dt = dadosW['dt']
    fuso_horario = dadosW['timezone']

    data_hora = datetime.utcfromtimestamp(dt)
    horario_local = data_hora + timedelta(seconds=fuso_horario)
    hora = horario_local.hour
    
    periodo = []

    if 0 <= hora < 12:
        periodo = ['manha', 'tarde', 'noite' ]

    elif 12 <= hora < 18: 
        periodo = ['tarde', 'noite' ]

    elif 18 <= hora <= 23:
        periodo = ['noite']

    

    print(periodo)
    print(hora)
    print(dadosW)






    #Previsões do tempo das 06, 12, 18

    dados_list = dadosF['list']

    #Pegando os dados da api, filtrando somente para as horas desejadas e adicionando no dicionario previsoes filtradas
    horarios_desejados = ['06:00:00', '12:00:00', '18:00:00']
    previsoes_filtradas = {}

    for itens in dados_list:
        dt_txt = itens['dt_txt']
        hora_list = dt_txt.split()[1]
        if hora_list in horarios_desejados:
            previsoes_filtradas[hora_list] = itens 


    if '06:00:00' in previsoes_filtradas and '12:00:00' in previsoes_filtradas and '18:00:00' in previsoes_filtradas:


        dados_6 = previsoes_filtradas['06:00:00']
        dados_12 = previsoes_filtradas['12:00:00']
        dados_18 = previsoes_filtradas['18:00:00']

        temperatura_6 = dados_6['main']['temp']
        sensacao_6 = dados_6['main']['feels_like']

        temperatura_12 = dados_12['main']['temp']
        sensacao_12 = dados_12['main']['feels_like']

        temperatura_18 = dados_18['main']['temp']
        sensacao_18 = dados_18['main']['feels_like']

        print(f"""6h: {temperatura_6} {sensacao_6}
12h: {temperatura_12} {sensacao_12}
18h: {temperatura_18} {sensacao_18}""")




















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
    