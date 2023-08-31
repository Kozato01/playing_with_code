import streamlit as st
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
# Atualiza o contador
count = viewspages()
#css
html_custom = """
<style>
.counter-container {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    font-size: 14px;
    font-weight: bold;
    margin-top: -40px;
    margin-right: -200px;
    color: green; /* Escolha as cores! */
}
</style>
"""
st.markdown(html_custom, unsafe_allow_html=True)
st.markdown(f'<div class="counter-container">Acessos: {count}</div>', unsafe_allow_html=True)

