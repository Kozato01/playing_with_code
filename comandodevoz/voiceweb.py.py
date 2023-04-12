# libs
import speech_recognition as sr  # import libs de reconhecimento de voz
from itertools import islice    # import função de fatiamento de iteráveis
import webbrowser               # import libs de navegação na web
from googlesearch import search # import função de pesquisa do Google
import os                       # import libs para operações do sistema operacional
import time                     # import libs para trabalhar com sleep


"""
Opa!, beleza? Eu fiz esse código de busca por voz no meu tempo livre, é tipo minha Alexa de pobre, sabe? 
Eu queria ter grana pra implementar com a API do ChatGPT, mas ainda não tenho dinheiro sobrando.
Mas quem sabe no futuro eu não faço algo ainda mais legal? Por enquanto, essa é a minha versão humilde, mas que já tá ajudando bastante. 
Se você tiver alguma sugestão pra melhorar, pode falar que eu tô aberto a ideias. Até mais!


"""

# Limpeza do prompt de comando
def clearcode():
    print("um momento...")
    time.sleep(3)
    return os.system("cls")

# Inicializando a variável do reconhecedor de voz
r = sr.Recognizer()           

while True:
    clearcode()
    
    #Configurando o microfone como fonte de áudio
    with sr.Microphone() as source:  
        print("Você está utilizando um código por comando de voz, para sair, apenas diga ""TAPIOCA""\n")
        print("Fale algo...")
        audio = r.listen(source)    # Iniciando a escuta do áudio do microfone

    try:
        text = r.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {text}")
        
        # Se a palavra "tapioca" estiver na fala, finaliza o programa
        if "tapioca" in text.lower():  
            print("Finalizando o programa...")
            break
        else:
            pesquisa = text + "site:br"
            urls = search(pesquisa, num_results=10)  

            # Abre o segundo resultado encontrado na busca
            for url in islice(urls, 1):  
                webbrowser.open(url)

    except sr.UnknownValueError:
        print("Não foi possível reconhecer a fala.") 
    except sr.RequestError as e:
        print("Erro ao conectar-se ao serviço de reconhecimento de fala: {0}".format(e))
