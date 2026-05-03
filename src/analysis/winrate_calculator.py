import duckdb

con = duckdb.connect("data/meta_db/lol.duckdb")

df = con.execute("""
    SELECT PlayerChampion, Lane, Count(*) AS Games, SUM(Win) AS Wins
    FROM PARTIDAS_GERAL
    GROUP BY PlayerChampion, Lane              
""").df()

con.close()