import requests
from datetime import datetime, timedelta


'''Recomendo ir com roupas leves, como camiseta e shorts. Está calor!

Recomendo usar roupas confortáveis — o clima está agradável.

Recomendo uma blusa leve ou um casaco fino. Está um pouco frio!

Recomendo usar um casaco ou jaqueta para se proteger. Está frio!

Recomendo um casaco pesado, cachecol e luvas — o frio está intenso!'''







# Funções para acessar as duas apis

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



def definir_temperatura(temperatura, sensacao):
    dif = abs(temperatura - sensacao)
    if dif > 7: 
        if sensacao < temperatura:
            return sensacao
        else:
            return temperatura
    else:
        media = (temperatura + sensacao) / 2
        return round(media, 2)

def mensagem_recomendada(temp_atual, temp_proximo, periodo_atual, periodo_proximo):
    def recomendar_roupa(temp):

        if temp >= 28:
            return "Recomendo roupas leves, como camiseta e shorts. Está calor!"
        elif 20 <= temp < 28:
            return "Recomendo usar roupas confortáveis — o clima está agradável."
        elif 15 <= temp < 20:
            return "Recomendo uma blusa leve ou um casaco fino. Está um pouco frio!"
        elif 10 <= temp < 15:
            return "Recomendo usar um casaco ou jaqueta para se proteger. Está frio!"
        else:
            return "Recomendo um casaco pesado, cachecol e luvas — o frio está intenso!"


    def recomendar_variacao(temp_atual, temp_proximo_periodo):
        diferenca = temp_proximo_periodo - temp_atual

        if diferenca <= -5 and temp_proximo_periodo < 18:
            return f"Porém, leve um casaco pois a {periodo_proximo} vai esfriar um pouco."

        elif diferenca >= 5 and temp_proximo_periodo > 26:
            return f"Porém, a {periodo_proximo} vai esquentar, então escolha roupas que possa tirar."

        else:
            return ''

    roupa_msg = recomendar_roupa(temp_atual)
    variacao_msg = recomendar_variacao(temp_atual, temp_proximo)
    if periodo_atual == 'manhã':
        oi = 'Bom dia'

    elif periodo_atual == 'tarde':
        oi = 'Boa tarde'

    elif periodo_atual == 'noite':
        oi = 'Boa noite'
        return f'{oi}, pela {periodo_atual} a temperatura está em torno de {temp_atual:.1f} graus. {recomendar_roupa(temp_atual)}'

    return f'{oi}, pela {periodo_atual} a temperatura está em torno de {temp_atual:.1f} graus. {roupa_msg} {variacao_msg}'

# Função principal

def definir_clima(city_name):
    api_key = "abe4201233b3a20dca48e1a3498d45d3"

    # Requisições para as duas APIs
    dadosF = api_forecast(api_key, city_name)
    dadosW = api_weather(api_key, city_name)



     # Dados de hora e fuso horário
    dt = dadosW['dt']
    fuso_horario = dadosW['timezone']
    data_hora = datetime.utcfromtimestamp(dt)
    horario_local = data_hora + timedelta(seconds=fuso_horario)
    hora = horario_local.hour



    # Dados climaticos 
    temperatura_atual = dadosW['main']['temp']
    sensacao_atual = dadosW['main']['feels_like']
    vento = dadosW['wind']['speed']
    umidade = dadosW['main']['humidity']


    # Previsões para 06h, 12h e 18h

    dados_list = dadosF['list']
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
        

        # Condições de horário
        
        temp_6 = definir_temperatura(temperatura_6, sensacao_6)
        temp_12 = definir_temperatura(temperatura_12, sensacao_12)
        temp_18 = definir_temperatura(temperatura_18, sensacao_18)
        temp_atual = definir_temperatura(temperatura_atual, sensacao_atual)

        
        if 0 <= hora < 6:
            # F F F 
            print(mensagem_recomendada(temp_6, temp_12, 'manhã', 'tarde'))
        elif 6 <= hora < 12:
            # W F F
            print(mensagem_recomendada(temp_atual, temp_12, 'manhã', 'tarde'))
        elif 12 <= hora < 18:
            # W F
            print(mensagem_recomendada(temp_atual, temp_18, 'tarde', 'noite'))
        elif 18 <= hora <= 23:
            # W
            print(mensagem_recomendada(temp_atual, temp_6, 'noite', 'manhã'))
        else:
            print('erro')







    