import streamlit as st
@st.cache_data
def initialize_access_count():
    return 0

# Função para atualizar o contador de acessos
def update_access_count():
    access_count = initialize_access_count() + 1
    return access_count


st.title("Contador de Acesso")

    # Atualiza o contador quando a página é acessada
access_count = update_access_count()
st.write(f"Esta página foi acessada {access_count} vezes.")
