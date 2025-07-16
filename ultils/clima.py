import requests

#abe4201233b3a20dca48e1a3498d45d3

def acessar_api(api_key, city):


    url = "https://api.openweathermap.org/data/2.5/weather?"
    url_completa = f"{url}&appid={api_key}&q={city}"
    
    reponse = requests.get(url_completa)

    return reponse.json()

def obter_previsão(city_name):

    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    dados = acessar_api(api_key, city_name)

    print(dados)