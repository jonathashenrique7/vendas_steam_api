import requests
import pandas as pd

# Endpoint da SteamSpy API para obter os dados de um jogo específico
endpoint = 'https://steamspy.com/api.php'

# Lista de appids dos jogos que você está interessado em obter os dados de vendas
appids = [730, 570, 440]  # Exemplos de appids (CS:GO, Dota 2, TF2)

# Lista para armazenar os dados de vendas de cada jogo
sales_data = []

# Itera sobre os appids e faz uma solicitação para a API para cada jogo
for appid in appids:
    params = {'request': 'appdetails', 'appid': appid}
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extrai os dados relevantes (vendas) do JSON recebido
        name = data.get('name', 'Unknown')
        owners = data.get('owners', -1)
        sales_data.append({'Name': name, 'Owners': owners})
    else:
        print(f"Failed to fetch data for appid {appid}")

# Converte os dados em um DataFrame pandas
df = pd.DataFrame(sales_data)

# Salvando o DataFrame em um arquivo CSV
df.to_csv('steam_sales_data.csv', index=False)

print("Dados de vendas extraídos e salvos em 'steam_sales_data.csv'.")
