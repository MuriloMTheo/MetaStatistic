import duckdb
import math
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
    
def wilson_lower(wins: int, games: int, z: float = 1.96) -> float:
    if games == 0:
        return 0.0
    p = wins / games
    num = p + z**2/(2*games) - z * math.sqrt((p*(1-p)/games) + (z**2/(4*games**2)))
    den = 1 + z**2/games
    return round(num / den, 4)  

def calculate_winrate(df):
    df = df[(df["Games"] > MIN_GAMES_FOR_TIER)]
    df["Winrate"] = df["Wins"] / df["Games"]
    df["WilsonScore"] = df.apply(
        lambda row: wilson_lower(int(row["Wins"]), int(row["Games"])), axis=1
    )
    return df

if __name__ == "__main__": #testelocal
    dfw = get_raw_stats(DB_PATH)
    dfw = calculate_winrate(dfw)
    print(dfw.head(10))

#print(df[df["PlayerChampion"] == 'Lux'].head())
#print(df["Lane"].unique())