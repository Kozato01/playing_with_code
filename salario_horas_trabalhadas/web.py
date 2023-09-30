import streamlit as st
import streamlit.components.v1 as components
import datetime
import holidays

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

def verificar_feriado(data):
    br_holidays = holidays.Brazil()  # Defina o país desejado

    return data in br_holidays

def calcular_salario_com_valor_fixo(horas_trabalhadas, taxa_horaria, valor_fixo, metodo_calculo):
    if metodo_calculo == "Por Hora":
        salario = horas_trabalhadas * taxa_horaria
    elif metodo_calculo == "Valor Fixo":
        salario = valor_fixo
    else:
        salario = 0  # Caso o método de cálculo seja inválido

    return salario

def main():
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(100deg, #000000, #154360);
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
    
    st.title("Calculadora de Salário Mensal")

    mes = st.number_input("Digite o número do mês (1-12):", min_value=1, max_value=12, value=1)
    ano = st.number_input("Digite o ano:", min_value=1900, max_value=2100, value=2023)
    metodo_calculo = st.selectbox("Escolha o tipo:", ["Por Hora", "Valor Fixo"])
    
    if metodo_calculo == "Por Hora":
        taxa_horaria = st.number_input("Digite sua taxa horária:", min_value=0.0, value=23.0)
        valor_fixo = 0
    else:
        valor_fixo = st.number_input("Digite o valor fixo:", min_value=0.0, value=1500.0)
        taxa_horaria = 0

    horas_trabalho_mes, num_dias_uteis = calcular_horas_trabalho_mes(mes, ano)
    if horas_trabalho_mes == 0:
        st.warning("Mês inválido. Verifique o número do mês.")
        return
        
    imposto_escolha = st.checkbox("Incluir imposto?", value=False)
    porcentagem = st.number_input("Digite a porcentagem do imposto:", min_value=0, max_value=100, value=6) if imposto_escolha else 0

    DAS_escolha = st.checkbox("Incluir DAS?", value=False)
    valor_das = 71 if DAS_escolha else 0
    #st.number_input("Valor do DAS:", min_value=0, value=71.0) 

    salario_mensal = calcular_salario_com_valor_fixo(horas_trabalho_mes, taxa_horaria, valor_fixo, metodo_calculo)

    imposto_calculado = (salario_mensal * (porcentagem/100)) + valor_das 
    salario_liquido = salario_mensal - imposto_calculado

    st.write("Número de dias úteis de trabalho no mês:", num_dias_uteis)
    st.write("Número de horas de trabalho no mês:", horas_trabalho_mes)
    st.write("Salário mensal bruto estimado: R$", salario_mensal)
    
    salario_final = salario_mensal
    if imposto_escolha and DAS_escolha:
        st.write("Valor do imposto: R$", imposto_calculado)
        st.write("Salário mensal liquido estimado: R$", salario_liquido)
        salario_final = salario_liquido

# indicações pra galera
    despesas_basicas = salario_final * 0.60
    poupanca_investimento = salario_final * 0.20
    gastos_pessoais = salario_final * 0.20
    
    st.write('-'*15)
    st.write('Recomendação de divisão do salário.')
    st.write(f'Despesas Básicas: R$ {despesas_basicas:.2f}')
    st.write(f'Poupança e Investimentos: R$ {poupanca_investimento:.2f}')
    st.write(f'Gastos Pessoais: R$ {gastos_pessoais:.2f}')

    icon_link = """
    <a href="https://www.linkedin.com/in/wylliams-d-342906121/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="30" />
    </a>
    """
    components.html(icon_link, height=40)
    
if __name__ == "__main__":
    main()
