import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def process_data(df, columns, metrics):
    try:
        if len(columns) == 0:
            st.write("Selecione pelo menos uma coluna para processar.")
            return

        processed_data = df[columns].agg(metrics)
        st.write("Resultados do Processamento:")
        st.write(processed_data)
    except Exception as e:
        st.write(f"Erro: Ocorreu um erro ao processar os dados - {str(e)}")


def visualize_data(df, columns, plot_type):
    try:
        if len(columns) == 0:
            st.write("Selecione pelo menos uma coluna para visualizar.")
            return

        st.write("Dados Selecionados:")
        st.dataframe(df[columns])

        if plot_type == "Gráfico de Barras":
            st.write("Selecione a coluna para o gráfico:")
            selected_column = st.selectbox("Coluna", columns)
            fig = go.Figure(data=[go.Bar(x=df.index, y=df[selected_column])])
            st.plotly_chart(fig)

        elif plot_type == "Scatter Plot":
            if len(columns) < 2:
                st.write("Selecione pelo menos duas colunas para os eixos.")
                return

            st.write("Selecione as colunas para os eixos:")
            x_axis = st.selectbox("Eixo X", columns, index=0)
            y_axis = st.selectbox("Eixo Y", columns, index=1)
            fig = go.Figure(data=[go.Scatter(x=df[x_axis], y=df[y_axis], mode='markers')])
            st.plotly_chart(fig)

            for i, (x, y) in enumerate(zip(df[x_axis], df[y_axis])):
                fig.add_annotation(x=x, y=y, text=f"{y:.2f}", showarrow=False, font=dict(color='black', size=8))

        elif plot_type == "Histograma":
            if len(columns) == 0:
                st.write("Selecione uma coluna para o histograma.")
                return

            st.write("Selecione a coluna para o histograma:")
            selected_column = st.selectbox("Coluna", columns)
            fig = go.Figure(data=[go.Histogram(x=df[selected_column])])
            st.plotly_chart(fig)

            for x, y in zip(*fig.histogram(df[selected_column])):
                fig.add_annotation(x=x, y=y, text=f"{y}", showarrow=False, font=dict(color='black', size=8))

        elif plot_type == "Gráfico de Pizza":
            if len(columns) == 0:
                st.write("Selecione uma coluna para o gráfico de pizza.")
                return

            st.write("Selecione a coluna para o gráfico:")
            selected_column = st.selectbox("Coluna", columns)
            data = df[selected_column].value_counts()
            labels = data.index
            values = data.values
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            st.plotly_chart(fig)

    except Exception as e:
        st.write(f"Erro: Ocorreu um erro ao visualizar os dados - {str(e)}")


def main():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(111deg, #2B4E28, #03CEEB);
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
    st.title("Importar Arquivos CSV")

    st.write("Selecione um arquivo CSV para importar:")

    file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if file is None:
        st.warning("Nenhum arquivo CSV foi selecionado.")
        return

    try:
        df = pd.read_csv(file)
        st.write("Dados importados:")
        st.dataframe(df)

        option = st.radio("Escolha uma opção:", ("Processar Dados", "Visualizar Dados"))

        if option == "Processar Dados":
            selected_columns = st.multiselect("Selecione as colunas:", df.columns)
            selected_metrics = st.multiselect("Selecione as métricas:", ["mean", "sum", "min", "max"])
            process_data(df, selected_columns, selected_metrics)
        elif option == "Visualizar Dados":
            selected_columns = st.multiselect("Selecione as colunas:", df.columns)
            plot_type = st.selectbox("Selecione o tipo de gráfico:", ("Gráfico de Barras", "Scatter Plot", "Histograma", "Gráfico de Pizza"))
            visualize_data(df, selected_columns, plot_type)

    except pd.errors.EmptyDataError:
        st.warning("O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        st.warning("Ocorreu um erro ao ler o arquivo CSV. Verifique se o formato do arquivo está correto.")


if __name__ == '__main__':
    main()
