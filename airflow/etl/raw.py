#from pyspark.sql import SparkSession
import pandas as pd
import datetime
import requests 

#api dos personagens 
def api_getdata_personagem(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erro ao acessar a página:", response.status_code)
        return None

# URL
base_url_personagens = "https://rickandmortyapi.com/api/character/"
all_data = []

# Iniciar a iteração pelas páginas de 2 até 42
for page_number in range(2, 43):
    page_url = f"{base_url_personagens}?page={page_number}"
    page_data = api_getdata_personagem(page_url)
    
    if not page_data:
        break
    
    all_data.extend(page_data['results'])


# API das localizações dos locais
def api_getdata_local(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erro ao acessar a página:", response.status_code)
        return None

# URL
base_url_local = "https://rickandmortyapi.com/api/location"
all_data_local = []

# Iniciar a iteração pelas páginas de 2 até 42
for page_number in range(2, 7):
    page_url = f"{base_url_local}?page={page_number}"
    page_data = api_getdata_local(page_url)
    
    if not page_data:
        break
    
    all_data_local.extend(page_data['results'])


df_personagem = pd.DataFrame(all_data)
df_local = pd.DataFrame(all_data_local)