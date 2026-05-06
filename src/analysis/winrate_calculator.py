import duckdb
import math
import pandas as pd
from src.config.settings import DB_PATH, MIN_GAMES_FOR_TIER, MIN_LANE_RATIO

def get_raw_stats (db_path: str):
    con = duckdb.connect(db_path)

    df = con.execute(f"""
        SELECT *
        FROM (
            SELECT
                PlayerChampion,
                Lane,
                COUNT(*) AS Games,
                SUM(Win) AS Wins,
                COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY PlayerChampion) AS Ratio
            FROM PARTIDAS_GERAL
            GROUP BY PlayerChampion, Lane
        ) t
        WHERE Ratio >= {MIN_LANE_RATIO}          
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
    df = df[(df["Games"] > MIN_GAMES_FOR_TIER)] #Apenas se tiver mais que o mínimo de games por tier
    df["Winrate"] = df["Wins"] / df["Games"] #Calculo WR bruto
    df["WilsonScore"] = df.apply( #Calculo WR por WilsonScore
        lambda row: wilson_lower(int(row["Wins"]), int(row["Games"])), axis=1
    )
    return df

def get_tier_champion(df):
    tier1 = df["WilsonScore"].quantile(0.8)
    tier2 = df["WilsonScore"].quantile(0.6)
    tier3 = df["WilsonScore"].quantile(0.4)
    tier4 = df["WilsonScore"].quantile(0.2)

    #Function Pandas para fazer o corte de forma dinâmica com base nos valores do WR
    tier = pd.cut(df["WilsonScore"], bins=[-1, tier4, tier3, tier2, tier1, 1], labels=[5, 4, 3, 2, 1])  
    df["Tier"] = tier
    return df

def winrate_orchestrator() -> pd.DataFrame:
#Função responsável por orquestrar todos as outras na chamada
    dfw = get_raw_stats(DB_PATH)
    dfw = calculate_winrate(dfw)
    dfw = get_tier_champion(dfw)
    return dfw

if __name__ == "__main__": #testelocal
    dfw = get_raw_stats(DB_PATH)
    dfw = calculate_winrate(dfw)
    dfw = get_tier_champion(dfw)
    #print(dfw.head(10))
    #print(dfw["WilsonScore"].describe())
    print(dfw[dfw["PlayerChampion"] == 'Ahri'].head())
    #print(dfw["Lane"].unique())
    
