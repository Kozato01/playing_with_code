import streamlit as st
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

    return horas_trabalho_mes

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
    st.title("Calculadora de Salário Mensal")

    mes = st.number_input("Digite o número do mês (1-12):", min_value=1, max_value=12, value=1)
    ano = st.number_input("Digite o ano:", min_value=1900, max_value=2100, value=2023)
    metodo_calculo = st.selectbox("Escolha o método de cálculo:", ["Por Hora", "Valor Fixo"])
    
    if metodo_calculo == "Por Hora":
        taxa_horaria = st.number_input("Digite sua taxa horária:", min_value=0.0, value=23.0)
        valor_fixo = 0
    else:
        valor_fixo = st.number_input("Digite o valor fixo:", min_value=0.0, value=1500.0)
        taxa_horaria = 0

    horas_trabalho_mes = calcular_horas_trabalho_mes(mes, ano)
    if horas_trabalho_mes == 0:
        st.warning("Mês inválido. Verifique o número do mês.")
        return

    salario_mensal = calcular_salario_com_valor_fixo(horas_trabalho_mes, taxa_horaria, valor_fixo, metodo_calculo)
    despesas_basicas = salario_mensal * 0.60
    poupanca_investimento = salario_mensal * 0.20
    gastos_pessoais = salario_mensal * 0.20

    st.write("Número de horas de trabalho no mês:", horas_trabalho_mes)
    st.write("Salário mensal estimado: R$", salario_mensal)
    st.write('-'*15)
    st.write('Recomendação de divisão do salário.')
    st.write(f'Despesas Básicas: R$ {despesas_basicas:.2f}')
    st.write(f'Poupança e Investimentos: R$ {poupanca_investimento:.2f}')
    st.write(f'Gastos Pessoais: R$ {gastos_pessoais:.2f}')

if __name__ == "__main__":
    main()
