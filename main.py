import requests
import pandas as pd
import time
import logging

# Configuração de logging
logging.basicConfig(filename='steam_api_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Endpoint da SteamSpy API para obter os dados de um jogo específico
endpoint = 'https://steamspy.com/api.php'

# Lista de appids dos jogos que você está interessado em obter os dados de vendas
appids = [
    730, 570, 440, 578080, 271590, 359550, 252490, 620, 1091500, 381210,
    8930, 550, 240, 4000, 304930, 236390, 221100, 245070, 362890, 10,
    480, 1500, 70, 22380, 72850, 1151640, 200510, 49520, 105600, 281990,
    252950, 400, 346110, 550650, 329110, 494840, 438100, 212070, 644930,
    410320, 431960, 433340, 425580, 218620, 227300, 582010, 489830, 359320,
    240720, 251570, 304930, 218620, 322330, 427520
]

# Remove duplicatas da lista de appids
appids = list(set(appids))

# Lista para armazenar os dados de vendas de cada jogo
dados_vendas = []

# Itera sobre os appids e faz uma solicitação para a API para cada jogo
for appid in appids:
    for attempt in range(3):  # Tenta até 3 vezes
        params = {'request': 'appdetails', 'appid': appid}
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                # Verificar se a estrutura do JSON é a esperada
                nome = data.get('name', 'Desconhecido')
                preco = data.get('price', 'Desconhecido')
                if isinstance(preco, int):
                    preco = f"R${preco / 100:.2f}"  # Converte centavos em reais
                classificacao = data.get('score_rank', 'Desconhecido')
                nota_usuarios = data.get('userscore', 'Desconhecido')
                proprietarios = data.get('owners', 'Desconhecido')
                
                dados_vendas.append({
                    'Nome': nome,
                    'Preço': preco,
                    'Classificação': classificacao,
                    'Nota dos Usuários': nota_usuarios,
                    'Proprietários': proprietarios
                })
                logging.info(f"Dados obtidos com sucesso para appid {appid}")
                break  # Sai do loop de tentativas se a requisição foi bem-sucedida
            except ValueError:
                logging.error(f"Resposta JSON inválida para appid {appid}")
                continue  # Tenta novamente se houver um erro ao processar o JSON
        else:
            logging.warning(f"Falha ao obter dados para appid {appid}, código de status {response.status_code}")
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente
    else:
        logging.error(f"Falha ao obter dados para appid {appid} após 3 tentativas")

# Converte os dados em um DataFrame pandas
df = pd.DataFrame(dados_vendas)

# Salvando o DataFrame em um arquivo CSV
df.to_csv('dados_vendas_steam.csv', index=False)

print("Dados de vendas extraídos e salvos em 'dados_vendas_steam.csv'.")
