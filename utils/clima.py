import requests
from datetime import datetime, timedelta

# Funções para acessar as duas apis

def api_forecast(api_key, city):
    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response_forecast = requests.get(url_forecast)

    return response_forecast.json()

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
    
def msg_madrugada(temp_atual, temp_madrugada):
    if temp_atual > (temp_madrugada + 5):
        if 15 <= temp_madrugada < 20:
            return "Durante a madrugada vai esfriar um pouco. Considere dormir com um cobertor quente."
        elif 10 <= temp_madrugada < 15:
            return "A madrugada será bem fria. Durma com dois cobertores ou um mais grosso."
        else:
            return "A madrugada terá frio intenso! Use casaco pesado, cachecol e se agasalhe bem até para dormir."
    return ''

def mensagem_recomendada(temp_atual, temp_proximo, periodo_atual, periodo_proximo):
    def recomendar_roupa(temp):
        if temp >= 28:
            return "🌞 Recomendo roupas leves, como camiseta e shorts. Está calor!"
        elif 20 <= temp < 28:
            return "😊 Recomendo usar roupas confortáveis — o clima está agradável."
        elif 15 <= temp < 20:
            return "🧥 Recomendo uma blusa leve ou um casaco fino. Está um pouco frio!"
        elif 10 <= temp < 15:
            return "🧣 Recomendo usar um casaco ou jaqueta para se proteger. Está frio!"
        else:
            return "❄️ Recomendo um casaco pesado, cachecol e luvas — o frio está intenso!"

    def recomendar_variacao(temp_atual, temp_proximo_periodo):
        diferenca = temp_proximo_periodo - temp_atual
        if diferenca <= -5 and temp_proximo_periodo < 18:
            return f"🧥 Porém, leve um casaco pois a {periodo_proximo} vai esfriar."
        elif diferenca >= 5 and temp_proximo_periodo > 26:
            return f"🌡️ Porém, a {periodo_proximo} vai esquentar, então escolha roupas que possa tirar."
        else:
            return ''

    roupa_msg = recomendar_roupa(temp_atual)
    variacao_msg = recomendar_variacao(temp_atual, temp_proximo)
    if periodo_atual == 'manhã':
        oi = '☀️ Bom dia'
    elif periodo_atual == 'tarde':
        oi = '🌤️ Boa tarde'
    elif periodo_atual == 'noite':
        oi = '🌙 Boa noite'
        return f'{oi}, pela {periodo_atual} a temperatura está em torno de {temp_atual:.1f}°C. \n\n{roupa_msg} Mas, ao amanhecer, fará {temp_proximo:.1f}°C. {recomendar_roupa(temp_proximo)}'
    return f'{oi}, pela {periodo_atual} a temperatura está em torno de {temp_atual:.1f}°C. \n\n{roupa_msg} {variacao_msg}'

def clima(dados, dados_proximo_periodo, proximo_periodo, vento, umidade, hora):
    condicoes_climaticas = {
        "rain": " - ☔ Está chovendo agora. Leve um guarda-chuva! ☔",
        "drizzle": " - 🌦️ Está chuviscando agora. Leve um guarda-chuva leve! 🌦️",
        "thunderstorm": " - ⛈️ Há tempestades com raios agora. Evite se expor e leve capa de chuva! ⛈️",
        "snow": " - ❄️ Está nevando agora. Se agasalhe bem! ❄️",
        "clouds": " - ☁️ Está nublado agora.",
        "mist": " - 🌫️ Há névoa no ar, atenção ao sair.",
        "fog": " - 🌁 A visibilidade está baixa devido à neblina.",
    }

    clima = dados['weather'][0]['main'].lower()
    clima_proximo = dados_proximo_periodo['weather'][0]['main'].lower()

    mensagem = condicoes_climaticas.get(clima, '')
    aviso_de_vento = aviso_de_umidade = aviso_chuva = sol = ''

    if (clima == 'clear' and 6 < hora < 18) or clima == 'clouds':
        cobertura = dados['clouds']['all']  # % de nuvens
        if cobertura < 30:
            sol = "\n - ☀️ Está sol no momento."
            temperatura_atual = dados['main']['temp']
            if temperatura_atual >= 28:
                sol += " E o sol está quente, use roupas leves e proteja-se do sol."
            else:
                sol += " Mas não está tão quente, aproveite o dia."

    if vento >= 5:
        aviso_de_vento = "\n - 🌬️ O vento está forte, pode parecer mais frio do que a temperatura indica."

    if umidade >= 85:
        aviso_de_umidade = "\n - 💧 A umidade está alta, o clima pode ficar mais abafado."
    elif umidade <= 30:
        aviso_de_umidade = "\n - 💨 A umidade está baixa, o ar está seco — beba bastante água e hidrate a pele."
    elif 30 < umidade < 40:
        aviso_de_umidade = "\n - ⚠️ A umidade está um pouco baixa, atenção à hidratação."

    if clima in ['clear', 'clouds', 'mist', 'fog'] and clima_proximo in ['rain', 'drizzle', 'thunderstorm']:
        aviso_chuva = f"\n - ☂️ Leve um guarda-chuva! Há previsão de chuva no(a) {proximo_periodo}."

    if mensagem or aviso_chuva:
        partes = [mensagem, aviso_chuva, aviso_de_vento, aviso_de_umidade, sol]
        texto_adicional = '\n'.join([p.strip() for p in partes if p.strip()])
        return f"\n📝 Informações adicionais sobre o clima:\n{texto_adicional}"
    else:
        return ''


# Função principal

def definir_clima(city_name):
    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    

    # Requisições para as duas APIs
    dadosF = api_forecast(api_key, city_name)
    dadosW = api_weather(api_key, city_name)

    # Tratamento de erro
    if dadosW.get("cod") != 200:
        print(f"Erro ao buscar clima para {city_name}: {dadosW.get('message', 'Erro desconhecido')}")
        return

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


    # Previsões para 03h,06h, 12h e 18h

    dados_list = dadosF['list']
    horarios_desejados = ['03:00:00', '06:00:00', '12:00:00', '18:00:00']
    previsoes_filtradas = {}

    for itens in dados_list:
        dt_txt = itens['dt_txt']
        hora_list = dt_txt.split()[1]
        if hora_list in horarios_desejados:
            previsoes_filtradas[hora_list] = itens 

    # Temperatura e sensação das 03h, 06h, 12h e 18h

    if '03:00:00' in previsoes_filtradas and '06:00:00' in previsoes_filtradas and '12:00:00' in previsoes_filtradas and '18:00:00' in previsoes_filtradas:

        dados_3 = previsoes_filtradas['03:00:00']
        dados_6 = previsoes_filtradas['06:00:00']
        dados_12 = previsoes_filtradas['12:00:00']
        dados_18 = previsoes_filtradas['18:00:00']
        
        temperatura_3 = dados_3['main']['temp']
        sensacao_3 = dados_3['main']['feels_like']

        temperatura_6 = dados_6['main']['temp']
        sensacao_6 = dados_6['main']['feels_like']

        temperatura_12 = dados_12['main']['temp']
        sensacao_12 = dados_12['main']['feels_like']

        temperatura_18 = dados_18['main']['temp']
        sensacao_18 = dados_18['main']['feels_like']
        

        # Condições de horário
        
        temp_3 = definir_temperatura(temperatura_3, sensacao_3)
        temp_6 = definir_temperatura(temperatura_6, sensacao_6)
        temp_12 = definir_temperatura(temperatura_12, sensacao_12)
        temp_18 = definir_temperatura(temperatura_18, sensacao_18)
        temp_atual = definir_temperatura(temperatura_atual, sensacao_atual)
    


        if 0 <= hora < 3:
            # W F 
            msg1 = mensagem_recomendada(temp_atual, temp_6, 'noite', 'manhã')
            msg2 = clima(dadosW, dados_6, 'manhã', vento, umidade, hora)

            resposta_final = f'{msg1}\n{msg2}'
        elif 3 <= hora < 12:
            # W F 
            msg1 = mensagem_recomendada(temp_atual, temp_12, 'manhã', 'tarde')
            msg2 = clima(dadosW, dados_12, 'tarde', vento, umidade, hora)

            resposta_final = f'{msg1}\n{msg2}'
        elif 12 <= hora < 18:
            # W F
            msg1 = mensagem_recomendada(temp_atual, temp_18, 'tarde', 'noite')
            msg2 = clima(dadosW, dados_18, 'noite', vento, umidade, hora)

            resposta_final = f'{msg1}\n{msg2}'
        elif 18 <= hora <= 23:
            # W F
            msg1 = mensagem_recomendada(temp_atual, temp_6, 'noite', 'manhã')
            msg2 = msg_madrugada(temp_atual, temp_3)
            msg3 = clima(dadosW, dados_6, 'manhã', vento, umidade, hora)

            resposta_final = f'{msg1}\n{msg2}\n{msg3}'
        else:
            return 'erro'

    return resposta_final