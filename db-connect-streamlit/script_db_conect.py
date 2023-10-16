import streamlit as st
import psycopg2
import mysql.connector.connection
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

#MySQL
def connect_to_mysql(host, username, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    return connection

#PostgreSQL
def connect_to_postgresql(host, database, username, password):
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=password
    )
    return connection

#Snowflake
def connect_to_snowflake(account, username, password, warehouse=None, database=None, schema=None):
    connection = snowflake.connector.connect(
        user=username,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    return connection

#Session
def create_session():
    session = st.session_state
    if 'connection' not in session:
        session.connection = None
        session.queries = []
    if 'saved_query_results' not in session:
        session.saved_query_results = []
    return session

#Conexão
def connection_page():
    st.markdown("""
            <h3 style='text-align: center; font-size: 80px'> DB-Link <img src='https://hermes.dio.me/users/student/73fa2bdf-5fa2-4ce5-ad84-8f17b3f046fe.gif' width='150'></h3>
        """, unsafe_allow_html=True)
    session = create_session()
    if session.connection:
        st.success("Você já está conectado ao banco de dados.")
        st.write("Você pode fazer consultas na próxima aba.")
        if st.button("Desconectar do Banco de Dados"):
            session.connection.close()
            session.connection = None
            session.queries = []
            st.rerun()
    else:
        #Opções de banco
        db_option = st.selectbox("Selecione o Banco de Dados", ("MySQL", "PostgreSQL", "Snowflake"))

        # Inpute pra banco
        if db_option in ("MySQL", "PostgreSQL"):
            host = st.text_input("Host/Account")
            username = st.text_input("Nome de Usuário")
            password = st.text_input("Senha", type="password")
            database = st.text_input("Nome do Banco de Dados")
            warehouse = schema = None
        elif db_option == "Snowflake":
            host = st.text_input("Host/Account")
            username = st.text_input("Nome de Usuário")
            password = st.text_input("Senha", type="password")
            database = st.text_input("Nome do Banco de Dados")
            use_advanced_options = st.checkbox("Especificar opções avançadas")
            if use_advanced_options:
                warehouse = st.text_input("Nome do Warehouse")
                schema = st.text_input("Nome do Schema")
            else:
                warehouse = schema = None
        else:
            host = username = password = database = warehouse = schema = None

        if st.button("Conectar ao Banco de Dados"):
            if db_option == "MySQL":
                session.connection = connect_to_mysql(host, username, password, database)
            elif db_option == "PostgreSQL":
                session.connection = connect_to_postgresql(host, database, username, password)
            elif db_option == "Snowflake":
                session.connection = connect_to_snowflake(host, username, password, warehouse, database, schema)
            st.success(f"Conectado ao Banco de Dados {db_option}")
            st.rerun()

#consultas SQL
def query_sql():
    st.markdown("""
            <h3 style='text-align: center; font-size: 50px'> Workspace <img src='https://media2.giphy.com/media/vISmwpBJUNYzukTnVx/giphy.gif' width='300'></h3>
        """, unsafe_allow_html=True)
    session = create_session()

    if session.connection is not None:
        st.subheader("Consultas SQL")
        col = st.columns(2)
        reset_button = col[0].button("Resetar DataFrames", help='O botão "Resetar DataFrames" permite limpar os resultados de consultas anteriores. Use este botão quando quiser realizar novas consultas a partir do zero.')
        execute_button = col[1].button("Executar Consulta", help='O botão "Executar Consulta" é utilizado para processar a consulta SQL que você inseriu. Certifique-se de preencher o campo de consulta antes de clicar neste botão.')

        if reset_button:
            session.queries = []
        #input sql
        query = st.text_area("Insira sua consulta SQL aqui:", help='''Como Fazer Consultas:\n 1. Na seção "Consultas SQL", insira sua consulta no campo de texto.\n2. Clique no botão "Executar Consulta" para obter os resultados da sua consulta.\n3. Os resultados serão exibidos em uma tabela logo abaixo.\n''')

        if execute_button:
            try:
                with session.connection.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                    if column_names:
                        session.queries = []
                        session.queries.append((column_names, data))
                    else:
                        session.queries = []
                        session.queries.append(data)
            except Exception as e:
                st.error(f"Erro durante a execução da consulta SQL: {str(e)}")

        if session.queries:
            session.queries.reverse()
            for i, query_result in enumerate(session.queries):
                st.write(f"Resultado da consulta:")
                if isinstance(query_result, tuple):
                    column_names, data = query_result
                    st.write("Nomes das colunas:", column_names)
                    df = pd.DataFrame(data, columns=column_names)
                    #salvar resultado
                    if st.button(f"Salvar Resultado da Consulta"):
                        session.saved_query_results.append(df)
                else:
                    df = pd.DataFrame(query_result)
                st.dataframe(df)
    else:
        st.warning("Nenhuma conexão com o banco de dados. Por favor, conecte-se primeiro.")

#dashboard
def dashboard_page():
    st.markdown("""
    <h3 style='text-align: center; font-size: 50px'> Dashboard/Metricas <img src='https://img.einnews.com/ampsize/383794/automotive-print-label.gif' width='300'></h3>
""", unsafe_allow_html=True)
    # Verificação se há resultados salvos
    if st.session_state.saved_query_results:
        st.subheader("Último Resultado da Consulta:")
        ultimo_resultado = st.session_state.saved_query_results[-1]
        st.dataframe(ultimo_resultado.head(100))
        # Opções de métricas usando uma lista suspensa
        st.subheader("Opções de Métricas")
        opcao_metrica = st.selectbox("Selecione a Métrica:", ("Resumo Estatístico","Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Linha", "Métrica Personalizada"))
        if opcao_metrica == "Gráfico de Barras":
            st.subheader("Gráfico de Barras")
            st.write("Este gráfico exibe a contagem ou frequência das categorias em uma coluna específica. "
                     "Selecione a coluna desejada no menu suspenso e o gráfico será gerado automaticamente.")
            plot_bar_chart(ultimo_resultado)

        elif opcao_metrica == "Gráfico de Pizza":
            st.subheader("Gráfico de Pizza")
            st.write("Este gráfico mostra a distribuição percentual das categorias em uma coluna específica. "
                     "Selecione a coluna desejada no menu suspenso e o gráfico será gerado automaticamente.")
            plot_pie_chart(ultimo_resultado)

        elif opcao_metrica == "Gráfico de Dispersão":
            st.subheader("Gráfico de Dispersão")
            st.write("Este gráfico mostra a relação entre duas variáveis usando pontos em um plano cartesiano. "
                     "Selecione as colunas desejadas para os eixos X e Y no menu suspenso e o gráfico será gerado automaticamente.")
            plot_scatter_plot(ultimo_resultado)

        elif opcao_metrica == "Gráfico de Linha":
            st.subheader("Gráfico de Linha")
            st.write("Este gráfico exibe a tendência ou padrão de uma variável ao longo de outra variável, geralmente em um eixo de tempo. "
                     "Selecione as colunas desejadas para os eixos X e Y no menu suspenso e o gráfico será gerado automaticamente.")
            plot_line_plot(ultimo_resultado)

        elif opcao_metrica == "Resumo Estatístico":
            st.subheader("Resumo Estatístico")
            st.write("Esta opção exibe estatísticas descritivas básicas para todas as colunas numéricas no conjunto de dados.")
            st.write(ultimo_resultado.describe())

        elif opcao_metrica == "Métrica Personalizada":
            st.subheader("Métrica Personalizada de Dispersão")
            st.write("Esse é um bonus, é a mesma metrica de dispersão com alguns mudanças e melhorias visualmente.")
            person_dispersor(ultimo_resultado)

    else:
        st.info("Nenhum resultado salvo no Dashboard ainda.")

#Area de funções........
# funct plotar um gráfico de barras
def plot_bar_chart(data):
    col_option = st.selectbox("Selecione a Coluna para o Gráfico de Barras", data.columns)
    bar_chart_data = data[col_option].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f'Gráfico de Barras para a Coluna: {col_option}', fontsize=14)
    sns.barplot(x=bar_chart_data.index, y=bar_chart_data.values, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_xlabel(col_option, fontsize=12)
    ax.set_ylabel('Contagem', fontsize=12)
    st.pyplot(fig)

# funct plotar um gráfico de pizza
def plot_pie_chart(data):
    col_option = st.selectbox("Selecione a Coluna para o Gráfico de Pizza", data.columns)
    pie_chart_data = data[col_option].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(f'Gráfico de Pizza para a Coluna: {col_option}', fontsize=14)
    ax.pie(pie_chart_data, labels=pie_chart_data.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

# funct plotar um gráfico de dispersão
def plot_scatter_plot(data):
    x_option = st.selectbox("Selecione a Coluna X", data.columns)
    y_option = st.selectbox("Selecione a Coluna Y", data.columns)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f'Gráfico de Dispersão entre {x_option} e {y_option}', fontsize=14)
    sns.scatterplot(data=data, x=x_option, y=y_option, ax=ax)
    st.pyplot(fig)

# funct plotar um gráfico de linha
def plot_line_plot(data):
    x_option = st.selectbox("Selecione a Coluna X", data.columns)
    y_option = st.selectbox("Selecione a Coluna Y", data.columns)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f'Gráfico de Linha entre {x_option} e {y_option}', fontsize=14)
    sns.lineplot(data=data, x=x_option, y=y_option, ax=ax)
    st.pyplot(fig)

# funct calcular métricas personalizadas e exibir gráfico de dispersão
def person_dispersor(data):
    try:
        if len(data.columns) < 2:
            st.warning("O DataFrame deve ter pelo menos duas colunas para calcular métricas personalizadas.")
        else:
            col1 = st.selectbox("Selecione a Coluna X", data.columns)
            col2 = st.selectbox("Selecione a Coluna Y", data.columns)
            mean_value = data[col1].mean()
            max_value = data[col2].max()
            min_value = data[col2].min()
            st.subheader("Gráfico de Dispersão com Métricas Personalizadas")
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(data[col1], data[col2], label=f'Dados de {col1} e {col2}')
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.axvline(x=mean_value, color="red", linestyle="--", label=f"Média de {col1}")
            ax.axhline(y=max_value, color="green", linestyle="--", label=f"Valor Máximo de {col2}")
            ax.axhline(y=min_value, color="blue", linestyle="--", label=f"Valor Mínimo de {col2}")
            ax.legend()
            st.pyplot(fig)
            st.write(f"Média de {col1}: {mean_value}")
            st.write(f"Valor Máximo de {col2}: {max_value}")
            st.write(f"Valor Mínimo de {col2}: {min_value}")
    except Exception as e:
        st.error(f"Erro ao calcular métricas personalizadas: {str(e)}")

#Visaul da Pagina... da um trampo
def set_app_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #8e44ad, #3498db, #45a049);
            background-attachment: fixed;
            background-size: cover;
            font-family: 'Quicksand', sans-serif;
            font-size: 18px;
            color: #ffffff;
        }}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            color: #ffffff;
            background-color: #232323;
            border-radius: 8px;
        }}
        .stButton {{
            background: linear-gradient(135deg, #3498db, #8e44ad);
            color: #ffffff;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: bold;
        }}
        .stButton:hover {{
            background: linear-gradient(135deg, #8e44ad, #3498db);
        }}
        .stSelectbox, .stTextArea {{
            background-color: #232323;
            color: #ffffff;
            border-radius: 8px;
        }}
        .stHeader {{
            font-size: 3rem;
            color: #ffffff;
            text-align: center;
            padding: 1.5rem;
        }}
        .stSidebar {{
            background-color: #232323;
            padding: 2rem;
            border-radius: 15px;
        }}
        .stSidebar .stButton {{
            width: 100%;
            margin-bottom: 1.5rem;
        }}
        .stH2 {{
            font-family: 'Caveat', cursive;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.write('<style>div.row-widget.stRadio > div{flex-direction: row; justify-content: righ;}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="DB-LINK",
        page_icon=":sunglasses:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    set_app_style()
    pages = {"Conexão ao Banco de Dados": connection_page, "Consultas SQL": query_sql, "Dashboard": dashboard_page}
    selected_page = st.sidebar.radio("Selecione a Página", list(pages.keys()))
    pages[selected_page]()

if __name__ == '__main__':
    main()
