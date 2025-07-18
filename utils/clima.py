import requests
from datetime import datetime, timedelta

#abe4201233b3a20dca48e1a3498d45d3

def acessar_api(api_key, city):


    url = "https://api.openweathermap.org/data/2.5/weather?"
    url_completa = f"{url}appid={api_key}&q={city}&units=metric"
    
    response = requests.get(url_completa)

    return response.json()

def definir_hora(city_name):
    api_key = "abe4201233b3a20dca48e1a3498d45d3"
    dados = acessar_api(api_key, city_name)

    dt = dados['dt']
    fuso_horario = dados['timezone']

    data_hora = datetime.utcfromtimestamp(dt)
    horario_local = data_hora + timedelta(seconds=fuso_horario)
    hora = horario_local.hour
    
    periodo = []

    if 0 <= hora < 12:
        periodo = ['manha', 'tarde', 'noite' ]

    elif 12 <= hora < 18: 
        periodo = ['tarde', 'noite' ]

    elif 18 <= hora < 23:
        periodo = ['noite']

    

    print(periodo)
    print(hora)
    print(dados)


















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

            pontuacao_clima  = {
                "Clear": 0,
                "Clouds": 1,
                "Haze": 1,
                "Smoke": 1,
                "Drizzle": 2,    
                "Rain": 3,          
                "Mist": 2,
                "Fog": 3,
                "Thunderstorm": 4
            }

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
            
            def pontuar_temperatura(temperatura):
                if temperatura >= 27:
                    return 0
                elif temperatura >= 22:
                    return 1
                elif temperatura >= 15:
                    return 2
                elif temperatura >= 10:
                    return 3
                elif temperatura >= 5:
                    return 5
                elif temperatura >= 0:
                    return 7
                else:
                    return 9
            
            def pontuar_sensacao(sensacao, umidade):
                if sensacao >= 27:
                    return 0
                elif sensacao >= 22:
                    return 1
                elif sensacao >= 15:
                    return 2
                elif sensacao >= 10:
                    return 3
                elif sensacao >= 5:
                    return 5 if umidade <= 80 else 6
                elif sensacao >= 0:
                    return 7 if umidade <= 80 else 8
                else:
                    return 9
                

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
    