import duckdb
from src.config.settings import DB_PATH, MIN_GAMES_FOR_TIER

def get_raw_stats (db_path: str):
    con = duckdb.connect(db_path)

    df = con.execute("""
        SELECT PlayerChampion, Lane, Count(*) AS Games, SUM(Win) AS Wins
        FROM PARTIDAS_GERAL
        GROUP BY PlayerChampion, Lane              
    """).df()

    con.close()
    return df
    
def calculate_winrate(df):
    df = df[(df["Games"] > MIN_GAMES_FOR_TIER)]
    df["Winrate"] = df["Wins"] / df["Games"]
    return df

if __name__ == "__main__": #testelocal
    dfw = get_raw_stats(DB_PATH)
    dfw = calculate_winrate(dfw)
    print(dfw.head(10))

#print(df[df["PlayerChampion"] == 'Lux'].head())
#print(df["Lane"].unique())