import streamlit as st
import streamlit.components.v1 as components
import datetime
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

#counter page
def viewspages():
    try:
        with open("counter.txt", "r") as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0
    count += 1
    with open("counter.txt", "w") as file:
        file.write(str(count))
    return count


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


#Função de execução.
def main():
    set_app_style()
    count = viewspages()
    st.markdown(f'<div class="counter-container">Views: {count}  <img src="https://media2.giphy.com/media/69IXObwFH221tvWgz1/giphy.gif?cid=ecf05e470l46rlrwccrxjo7nfs88hafpud8vvtfqes0lc9iy&ep=v1_gifs_related&rid=giphy.gif&ct=s" width="35"> </div>', unsafe_allow_html=True)

    #Titulo
    st.markdown("# Calculadora de Salário Mensal <img src='https://3.bp.blogspot.com/-KIZ9p-k2cdI/WvRiMSwk7BI/AAAAAAAA7DQ/TXiSbwbbQUQqGROhg5vsi4y7-JdKFBxpgCLcBGAs/s1600/i%2Bbelieve%2Bi%2Bcan%2Bfly%2BI%2BBELIEVE%2BI%2BCAN%2BTOUCH%2BSKY.gif' width='50'>", unsafe_allow_html=True)

    message = st.chat_message("assistant", avatar="🧑‍💻")
    message.write("Bem-vindo ao nosso Calculador de Salário! Aqui, simplificamos o processo de entender o seu rendimento. Seja você um profissional CLT ou PJ, nosso site oferece uma maneira fácil e rápida de calcular seu salário líquido, levando em consideração impostos e DAS. Otimize suas finanças de forma inteligente. Experimente agora!")
    mes = st.number_input("Digite o número do mês (1-12):", min_value=1, max_value=12, value=datetime.datetime.today().month)
    ano = st.toggle("Deseja escolher o ano?", help='Estamos usando o ano atual, caso deseje utilizar outro ano, marque a opção abaixo.' )
    if ano:
        ano = st.number_input("Digite o ano:", min_value=1900, max_value=2100, value=datetime.datetime.today().year)
    else:
        ano = datetime.datetime.today().year

    metodo_calculo = st.radio("Escolha o tipo:", ["Por Hora", "Valor Fixo"], help='Escolha o tipo de pagamento que você recebe') 
    valor_fixo, taxa_horaria = 0, 0
    if metodo_calculo == "Por Hora":
        taxa_horaria = st.number_input("Digite sua taxa horária:", min_value=0.0, value=0.0)
    else:
        valor_fixo = st.number_input("Digite o valor fixo:", min_value=0.0, value=0.0)
        

    horas_trabalho_mes, num_dias_uteis = calcular_horas_trabalho_mes(mes, ano)
    if horas_trabalho_mes == 0:
        st.warning("Mês inválido. Verifique o número do mês.")
        return
        
    imposto_escolha = st.toggle("Incluir imposto?", value=False)
    DAS_escolha = st.toggle("Incluir DAS?", value=False)
    porcentagem = st.number_input("Digite a porcentagem do imposto:", min_value=0, max_value=100, value=6) if imposto_escolha else 0
    valor_das = 71 if DAS_escolha else 0

    salario_mensal = calcular_salario_com_valor_fixo(horas_trabalho_mes, taxa_horaria, valor_fixo, metodo_calculo)
    imposto_calculado = (salario_mensal * (porcentagem/100)) + valor_das 
    salario_liquido = salario_mensal - imposto_calculado

    st.write("Número de dias úteis de trabalho no mês:", num_dias_uteis)
    st.write("Número de horas de trabalho no mês:", horas_trabalho_mes)
    st.write("Salário mensal bruto estimado: R$", salario_mensal)
    
    salario_final = salario_mensal
    if imposto_escolha or DAS_escolha:
        st.write("Valor do imposto: R$", imposto_calculado)
        st.write("Salário mensal liquido estimado: R$", salario_liquido)
        salario_final = salario_liquido
   
    st.write('-'*15)
    st.write('Recomendação de divisão do salário.')
    st.write(f'Despesas Básicas: R$ {(salario_final * 0.60):.2f}')
    st.write(f'Poupança e Investimentos: R$ {(salario_final * 0.20):.2f}')
    st.write(f'Gastos Pessoais: R$ {(salario_final * 0.20):.2f}')

    add_linked_in_icon()
    #css especificos da page.
    html_custom_contador = """
    <style>
    .counter-container {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        font-size: 25px;
        font-weight: bold;
        margin-top: -40px;
        margin-right: -200px;
        color: #000000; /* Cor do texto: preto */
        background: linear-gradient(45deg, #ff5733, #ffbd33);
        background-attachment: fixed;
        background-size: auto;
        background-clip: text; /* Aplica o gradiente apenas ao texto */
        -webkit-background-clip: text; /* Necessário para navegadores baseados em Webkit, como Chrome e Safari */
        text-fill-color: transparent; /* Torna a cor do texto transparente */
        -webkit-text-stroke: 0.2px #ff5733; /* Contorno de texto: espessura e cor laranja */
        text-stroke: 1px #ff5733;
    }
    </style>
    """


    st.markdown(html_custom_contador, unsafe_allow_html=True)

    #feactures de texto
    #radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    borda_infinita("https://i.pinimg.com/originals/61/f9/51/61f951ee6770732cba132c4b89c316b5.gif", 50)

if __name__ == "__main__":
    main()