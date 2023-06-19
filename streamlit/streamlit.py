
import streamlit as st
import snowflake.connector
import pandas as pd
import base64
import pyperclip
import openai as gpt


st.set_page_config(
    page_title="Home",
    page_icon="✌️",
)


# Configuração do Snowflake
snowflake_account = ''
snowflake_user = ''
snowflake_password = ''
snowflake_database = ''
snowflake_schema = ''


# Função para executar consultas SQL no Snowflake
def execute_query(query):
    conn = snowflake.connector.connect(
        account=snowflake_account,
        user=snowflake_user,
        password=snowflake_password,
        database=snowflake_database,
        schema=snowflake_schema
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return results, column_names

# Função para exportar dados para um arquivo CSV
def export_to_csv(dataframe):
    csv_data = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resultado.csv">Clique aqui para baixar o arquivo CSV</a>'
    return href

# API da gpt
gpt.api_key = ""

# Interface do Streamlit
def get_chat_response(prompt):
    response = gpt.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.write("Código GPT copiado com sucesso!")
    
def main():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(100deg, #2B4E88, #11CEEB);
             background-attachment: fixed;
             background-size: cover;
             font-family: Arial, sans-serif;
            font-size: 14px;
            color: white;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    

    
    st.title("Playground ☀️ SQL")

    # Adiciona uma borda lateral esquerda para o chat
    st.sidebar.title("ChatGPT")

    # Campo de entrada para o chat
    chat_input = st.sidebar.text_input("Digite uma mensagem:")

    # Botão para enviar a mensagem do chat
    if st.sidebar.button("Enviar"):
        if chat_input:
            # Lógica para obter a resposta do ChatGPT
            chat_prompt = "Usuário: " + chat_input
            chat_response = get_chat_response(chat_prompt)

            # Exibe a resposta do ChatGPT
            st.sidebar.markdown(chat_response)


    if st.sidebar.button('Copiar'):
        if chat_input:
            gpt_code = get_chat_response(chat_input)
            copy_to_clipboard(gpt_code)
            

    query = st.text_area("Digite sua consulta SQL:")
    # Botão para executar a consulta SQL
    if st.button("Executar SQL"):
        if query:
            results, column_names = execute_query(query)
            if results:
                st.write("Resultado da consulta:")
                df = pd.DataFrame(results, columns=column_names)
                st.dataframe(df)
                
                st.markdown(export_to_csv(df), unsafe_allow_html=True)

            else:
                st.write("Nenhum resultado encontrado.")
        else:
            st.write("Digite uma consulta SQL válida.")
    
if __name__ == '__main__':
    main()