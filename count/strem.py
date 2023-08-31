import streamlit as st

# Função para ler ou inicializar o contador de acessos
def get_access_count():
    try:
        with open('access_count.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Função para atualizar e exibir o contador de acessos
def update_access_count():
    count = get_access_count() + 1
    with open('access_count.txt', 'w') as f:
        f.write(str(count))
    return count

def main():
    st.title("Contador de Acesso")

    # Atualiza o contador quando a página é acessada
    access_count = update_access_count()
    st.write(f"Esta página foi acessada {access_count} vezes.")

if __name__ == '__main__':
    main()
