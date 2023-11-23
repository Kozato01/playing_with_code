import streamlit as st
import streamlit.components.v1 as components
import datetime
import pandas as pd
import holidays

#Função principal para calcular as horas de trabalho.
def calcular_horas_trabalho_mes(mes, ano):
    if mes < 1 or mes > 12:
        st.error("Mês inválido. O valor do mês deve estar entre 1 e 12.")
        return 0

    if mes == 12:
        proximo_mes = 1
        proximo_ano = ano + 1
    else:
        proximo_mes = mes + 1
        proximo_ano = ano

    # Obtém o último dia do mês informado
    ultimo_dia_mes = datetime.date(proximo_ano, proximo_mes, 1) - datetime.timedelta(days=1)
    num_dias_mes = ultimo_dia_mes.day

    # Conta quantos dias úteis existem no mês, desconsiderando os feriados
    num_dias_uteis = 0
    for dia in range(1, num_dias_mes+1):
        data = datetime.date(ano, mes, dia)
        if data.weekday() < 5 and not verificar_feriado(data):  # Verifica se é um dia útil e não é feriado
            num_dias_uteis += 1

    # Calcula o número total de horas de trabalho no mês
    horas_trabalho_mes = num_dias_uteis * 8

    return horas_trabalho_mes, num_dias_uteis

#Verificação de feriado.
def verificar_feriado(data):
    br_holidays = holidays.Brazil()  # Defina o país desejado

    return data in br_holidays

#Salario Fixo do individuo, talvez der pra melhorar futuramente. 
def calcular_salario_com_valor_fixo(horas_trabalhadas, taxa_horaria, valor_fixo, metodo_calculo):
    if metodo_calculo == "Por Hora":
        salario = horas_trabalhadas * taxa_horaria
    elif metodo_calculo == "Valor Fixo":
        salario = valor_fixo
    else:
        salario = 0  # Caso o método de cálculo seja inválido

    return salario



#Visual da Pagina
def set_app_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #2a1958, #7045af, #d53f8c);
            background-attachment: fixed;
            background-size: cover;
            font-family: 'Roboto', sans-serif;
            font-size: 18px;
            color: #ffffff;
        }}
        .stTextInput > div > div > input {{
            color: #333333;
        }}
        .stButton {{
            background-color: #ff9f00;
            color: #ffffff;
            border-radius: 10px;
        }}
        .stButton:hover {{
            background-color: #ff8000;
        }}
        .stSelectbox, .stTextArea {{
            background-color: #333333;
            color: #ffffff;
            border-radius: 5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#Links
def add_linked_in_icon():
    icon_link = """
    <a href="https://www.linkedin.com/in/wylliams-d-342906121/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="30" />
    </a>
    """
    components.html(icon_link, height=40)

def borda_infinita(gif_url, border_height):
    # Define o estilo CSS para o layout do GIF
    css_style = f"""
    <style>
        .gif-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: {border_height}px; /* Altura da "borda" */
            overflow: hidden;
            z-index: 999; /* Z-index alto para ficar acima do conteúdo abaixo */
        }}
        .gif {{
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
        }}
    </style>
    """

    # Adiciona o estilo CSS ao aplicativo
    st.markdown(css_style, unsafe_allow_html=True)

    # HTML para o GIF e a "borda"
    html_content = f"""
    <div class="gif-container">
        <img class="gif" src="{gif_url}" alt="GIF">
    </div>
    """

    # Renderiza o HTML
    st.markdown(html_content, unsafe_allow_html=True)


def main():
    set_app_style()
    
    st.markdown("# Calculadora de Salário Mensal <img src='https://3.bp.blogspot.com/-KIZ9p-k2cdI/WvRiMSwk7BI/AAAAAAAA7DQ/TXiSbwbbQUQqGROhg5vsi4y7-JdKFBxpgCLcBGAs/s1600/i%2Bbelieve%2Bi%2Bcan%2Bfly%2BI%2BBELIEVE%2BI%2BCAN%2BTOUCH%2BSKY.gif' width='50'>", unsafe_allow_html=True)

    message = st.chat_message("assistant", avatar="🧑‍💻")
    message.write("Bem-vindo ao nosso Calculador de Salário! Aqui, simplificamos o processo de entender o seu rendimento. Seja você um profissional CLT ou PJ, nosso site oferece uma maneira fácil e rápida de calcular seu salário líquido, levando em consideração impostos e DAS. Otimize suas finanças de forma inteligente. Experimente agora!")

    # Configuração de mês e ano
    col1, col2 = st.columns(2)
    mes = col1.number_input("Digite o número do mês (1-12):", min_value=1, max_value=12, value=datetime.datetime.today().month)
    ano = col2.number_input("Digite o ano:", min_value=1900, max_value=2100, value=datetime.datetime.today().year) if st.toggle("Deseja escolher o ano?", help='Estamos usando o ano atual, caso deseje utilizar outro ano, marque a opção abaixo.') else datetime.datetime.today().year
    
    # Opção para escolher dias úteis manualmente
    opcao_calculo_dias = st.checkbox("Escolher dias úteis manualmente", value=False, help="Marque para inserir manualmente o número de dias úteis trabalhado.")
    
    if opcao_calculo_dias:
        num_dias_uteis_manual = st.number_input("Número de dias úteis de trabalho no mês (opcional):", min_value=0, max_value=31, value=0)
        num_dias_uteis = num_dias_uteis_manual
        st.warning("Você escolheu inserir manualmente o número de dias úteis.")
    else:
        num_dias_uteis = calcular_horas_trabalho_mes(mes, ano)[1]

    # Método de cálculo do salário
    metodo_calculo = st.radio("Escolha o tipo:", ["Por Hora", "Valor Fixo"], help='Escolha o tipo de pagamento que você recebe') 
    valor_fixo, taxa_horaria = 0, 0
    if metodo_calculo == "Por Hora":
        taxa_horaria = st.number_input("Digite sua taxa horária:", min_value=0.0, value=0.0)
    else:
        valor_fixo = st.number_input("Digite o valor fixo:", min_value=0.0, value=0.0)

    # Cálculo das horas de trabalho
    horas_trabalho_mes, _ = calcular_horas_trabalho_mes(mes, ano)
    horas_trabalho_mes = num_dias_uteis * 8  # Atualiza as horas de trabalho com base nos dias úteis inseridos

    if horas_trabalho_mes == 0:
        st.warning("Mês inválido. Verifique o número do mês.")
        return

    # Opções de imposto e DAS
    imposto_escolha = st.toggle("Incluir imposto?", value=False)
    DAS_escolha = st.toggle("Incluir DAS?", value=False)

    if imposto_escolha:
        porcentagem = st.number_input("Porcentagem do imposto (%)", min_value=0, max_value=100, value=6)
    else:
        porcentagem = 0

    valor_das = 71 if DAS_escolha else 0

    # Cálculo do salário
    salario_mensal = calcular_salario_com_valor_fixo(horas_trabalho_mes, taxa_horaria, valor_fixo, metodo_calculo)
    imposto_calculado = (salario_mensal * (porcentagem/100)) + valor_das 
    salario_liquido = salario_mensal - imposto_calculado

    # Apresentação dos resultados
    st.write("Número de dias úteis de trabalho no mês:", num_dias_uteis)
    st.write("Número de horas de trabalho no mês:", horas_trabalho_mes)
    st.write("Salário mensal bruto estimado: R$", salario_mensal)
    
    salario_final = salario_mensal
    if imposto_escolha or DAS_escolha:
        st.write("Valor do imposto: R$", imposto_calculado)
        st.write("Salário mensal líquido estimado: R$", salario_liquido)
        salario_final = salario_liquido
   
    # Mostrar ou ocultar a recomendação de divisão do salário
    mostrar_recomendacao = st.checkbox("Mostrar Recomendação de divisão do salário", value=False)
    
    if mostrar_recomendacao:
        st.write('-'*15)
        st.write('Recomendação de divisão do salário:')
        
        # Dados para a tabela
        percentual_despesas = st.slider("Percentual para Despesas Básicas (%)", min_value=0, max_value=100, value=60)
        percentual_poupanca = st.slider("Percentual para Poupança e Investimentos (%)", min_value=0, max_value=100, value=20)
        percentual_gastos_pessoais = 100 - percentual_despesas - percentual_poupanca
            
        dados_tabela = {
            'Categoria': ['Despesas Básicas', 'Poupança e Investimentos', 'Gastos Pessoais'],
            'Percentual': [f'{percentual_despesas}%', f'{percentual_poupanca}%', f'{percentual_gastos_pessoais}%'],
            'Valor (R$)': [f'R$ {(salario_final * percentual_despesas/100):.2f}', f'R$ {(salario_final * percentual_poupanca/100):.2f}', f'R$ {(salario_final * percentual_gastos_pessoais/100):.2f}']
        }

        if imposto_escolha:
            valor_imposto = salario_final * porcentagem / 100
            dados_tabela['Categoria'].append('Imposto')
            dados_tabela['Percentual'].append(f'{porcentagem}%')
            dados_tabela['Valor (R$)'].append(f'R$ {valor_imposto:.2f}')

        if DAS_escolha:
            dados_tabela['Categoria'].append('DAS')
            dados_tabela['Percentual'].append('Fixo')
            dados_tabela['Valor (R$)'].append(f'R$ {valor_das:.2f}')

        # Adiciona uma linha para a soma dos valores na tabela
        soma_valores = salario_final * percentual_despesas/100 + salario_final * percentual_poupanca/100 + salario_final * percentual_gastos_pessoais/100
        
        dados_tabela['Categoria'].append('Valor Final ')
        dados_tabela['Percentual'].append('--------')
        dados_tabela['Valor (R$)'].append(f'R$ {soma_valores:.2f}')

        # Cria o DataFrame
        df_tabela = pd.DataFrame(dados_tabela)

        # Define estilos para a tabela
        styles = [
            dict(selector="th", props=[("font-size", "110%"), ("text-align", "center"), ("background-color", "#824caf"), ("color", "white")]),
            dict(selector="td", props=[("font-size", "100%"), ("text-align", "center"), ("background-color", "#f2f2f2"), ("color", "black")]),
            dict(selector="tr:hover", props=[("background-color", "#e0e0e0")]),
            dict(selector="td, th", props=[("border", "2px solid #0c0c12")]),
            dict(selector="table", props=[("border-collapse", "collapse"), ("width", "100%")]),
            dict(selector="caption", props=[("caption-side", "bottom")])
        ]
        # Exibe a tabela com estilos personalizados
        st.table(df_tabela.style.set_table_styles(styles))

    add_linked_in_icon()
    # Features de texto
    # Radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    borda_infinita("https://i.pinimg.com/originals/61/f9/51/61f951ee6770732cba132c4b89c316b5.gif", 50)

if __name__ == "__main__":
    main()
