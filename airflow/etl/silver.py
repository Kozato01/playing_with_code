from raw import df_personagem, df_local

df_personagem = df_personagem.rename(columns={"id": "id","name": "nome", "status": "status","species": "especie","type"\
                                          :"tipo","gender":"genero","origin": "origem","location": "local","image":"imagem",\
                                            "episode":"episodio" ,"url": "url","created": "datacreated"}).replace("unknown", "Desconhecido")\
                                                .replace("Alive", "Vivo").replace("Dead", "Morto").replace("", "Não informado")\
                                                .replace("Male", "Masculino").replace("Female", "Feminino")

df_local = df_local[["name", "type", "dimension", "residents"]].rename(columns={"name": "Local", "type": "tipo", \
                                                                                "dimension":"dimensão", "residents": "moradores"})\
                                                                                .replace("", "Não Informado")


