import duckdb
from transform_dataset import partida


def load():
#Etapa responsável por abrir o banco e inserir os dados tratados    
    con = duckdb.connect("data/meta_db/lol.duckdb")
    con.execute("DROP TABLE IF EXISTS PARTIDAS_GERAL")
    con.execute("CREATE TABLE PARTIDAS_GERAL AS SELECT * FROM partida")
    print(f"{len(partida)} linhas carregadas inseridas na tabela PARTIDAS_GERAL")
    con.close()


if __name__ == "__main__":
    load()
