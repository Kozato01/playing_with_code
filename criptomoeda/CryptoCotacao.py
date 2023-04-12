# Import Libs
import requests
import csv
import time
import os
from datetime import datetime
from pyspark.sql.functions import from_unixtime, unix_timestamp, date_format, from_utc_timestamp, lit
from pyspark.sql.functions import expr, explode, col, regexp_replace
from pyspark.sql import SparkSession

"""
Este é um código em Python que utiliza a biblioteca Spark/PySpark para extrair dados de uma criptomoeda escolhida pelo usuário. 
O objetivo é salvar os dados em um arquivo CSV, mas o código também foi atualizado para permitir que os dados sejam salvos em um banco de dados 
como MySQL ou MongoDB.
O usuário pode definir a criptomoeda desejada e o intervalo de tempo em que a extração de dados deve ocorrer, 
permitindo que o código seja customizado de acordo com as necessidades individuais.

Para personalizar o código, é possível alterar os seguintes parâmetros:

O nome da criptomoeda a ser extraída, definido na variável 'EntradaCrypto'.
O intervalo de tempo da extração de dados, definido no final do codigo em "time.sleep()" (30 segundos por padrão).
"""


# Define a criptomoeda a ser monitorada
EntradaCrypto = ["BTC"]

# API da Brapi
# Faz a requisição na API para verificar quais criptomoedas estão disponíveis para consulta
camp = requests.request(
    "GET", "https://brapi.dev/api/v2/crypto/available").json()
# Extrai a lista de criptomoedas disponíveis da API
camposlist = camp.pop('coins', None)

while True:
    # Loop principal que fica verificando a criptomoeda definida em EntradaCrypto

    for parametro in EntradaCrypto:
        parametro = parametro.upper()
        print(f"""\nA criptomoeda escolhida foi: {parametro}\n""")
        # Verifica se a criptomoeda definida está disponível na API

        if parametro in camposlist:
            # Monta a URL de consulta com a criptomoeda definida, OBS: Você pode trocar a moeda de BRL pra outra.
            url = f"https://brapi.dev/api/v2/crypto?coin={parametro}&currency=BRL"
            response = requests.request("GET", url)
            json_data = response.json()

            # SparkSession para utilizar o PySpark
            spark = SparkSession.builder \
                .master("local") \
                .appName("ETL1") \
                .config("spark.hadoop.validateOutputSpecs", "false") \
                .getOrCreate()
            spark.sparkContext.setLogLevel('ERROR')

            # Cria um dataframe com os dados obtidos na API
            df = spark.createDataFrame([json_data]) \
                .select(explode("coins").alias("coins")) \
                .select('coins.coin', 'coins.currency', 'coins.currencyRateFromUSD', 'coins.regularMarketTime') \
                .toDF("ativo", "moeda", "cotacao", "data_captura") \
                .withColumn("data_captura", date_format(from_utc_timestamp(from_unixtime("data_captura"), "America/Sao_Paulo"), "dd-MM-yyyy HH:mm")) \
                .withColumn("cotacao", regexp_replace("cotacao", "\.", ",")) \
                .withColumn("data_proc", date_format(from_utc_timestamp(lit(datetime.now()), "America/Sao_Paulo"), "dd-MM-yyyy HH:mm"))

            # Exibe o dataframe
            df.show()
            print("=-=-"*15)

            # Cria uma pasta para armazenar os arquivos CSV caso ela não exista
            if not os.path.exists("df_saved"):
                os.mkdir("df_saved")

            # Salvando os dados em um arquivo CSV
            data_atual = datetime.now().strftime('%d-%m-%Y')
            nome_arquivo = f'df_saved/cotacao_BTC_{data_atual}.csv'
            with open(nome_arquivo, mode='a', newline='') as arquivo:
                writer = csv.writer(arquivo, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if arquivo.tell() == 0:
                    # Se o arquivo estiver vazio, escrever o cabeçalho
                    writer.writerow(
                        ['ativo', 'moeda', 'cotacao', "data_captura", "data_proc"])
                # Escrever a linha com a cotação atual e a data
                writer.writerow([row.ativo, row.moeda, row.cotacao, row.data_captura, row.data_proc]
                                for row in df.collect())

        # Aguarda 30 segundos antes de buscar novamente as informações
        time.sleep(30)
