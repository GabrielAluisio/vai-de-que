import requests

#abe4201233b3a20dca48e1a3498d45d3

def acessar_api(api_key, city):


    url = "https://api.openweathermap.org/data/2.5/weather?"
    url_completa = f"{url}appid={api_key}&q={city}&units=metric"
    
    response = requests.get(url_completa)

    return response.json()

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
        
        print(f'O clima em {city_name}: {clima}')
        print(f'Temperatura: {temperatura}°C')
        print(f'Sensação: {sensacao}°C')
        print(f'Velocidade do vento: {vento}m/s')

    else:
        print('Cidade não encontrada!')
    