# Use uma imagem base do Python
FROM python:3.8

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos (se houver)
COPY requirements.txt .

# Instale as dependências do aplicativo
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório atual para o contêiner
COPY . .

# Exponha a porta em que o Streamlit será executado (por padrão, a porta 8501)
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "scripty.conect.py"]
