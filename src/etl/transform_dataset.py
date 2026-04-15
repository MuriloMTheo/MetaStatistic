import pandas as pd
from extract_dataset import path

champion = pd.read_csv(path + "/ChampionTbl.csv")
item = pd.read_csv(path + "/ItemTbl.csv")
matchstats = pd.read_csv(path + "/MatchStatsTbl.csv")
matchtbl = pd.read_csv(path + "/MatchTbl.csv")
ranking = pd.read_csv(path + "/RankTbl.csv")
summoner = pd.read_csv(path + "/SummonerMatchTbl.csv")
team = pd.read_csv(path + "/TeamMatchTbl.csv")

champ_enemy = champion.rename(columns={
    "ChampionId": "EnemyChampionFk",
    "ChampionName": "EnemyChampion"
})

champ_player = champion.rename(columns={
    "ChampionId": "ChampionFk",
    "ChampionName": "PlayerChampion"
})
item1 = item.rename(columns={"ItemID":"item1","ItemName" : "ItemSlot1"})
item2 = item.rename(columns={"ItemID":"item2","ItemName" : "ItemSlot2"})
item3 = item.rename(columns={"ItemID":"item3","ItemName" : "ItemSlot3"})
item4 = item.rename(columns={"ItemID":"item4","ItemName" : "ItemSlot4"})
item5 = item.rename(columns={"ItemID":"item5","ItemName" : "ItemSlot5"})
item6 = item.rename(columns={"ItemID":"item6","ItemName" : "ItemSlot6"})

partida = (
    matchstats
    .merge(champ_enemy, on="EnemyChampionFk", how="left")
    .merge(summoner, left_on="SummonerMatchFk", right_on="SummonerMatchId", how="left")
    .merge(champ_player, on="ChampionFk", how="left")
    .merge(item1, on = "item1", how="left")
    .merge(item2, on = "item2", how="left")
    .merge(item3, on = "item3", how="left")
    .merge(item4, on = "item4", how="left")
    .merge(item5, on = "item5", how="left")
    .merge(item6, on = "item6", how="left")
    .merge(matchtbl, left_on="MatchFk", right_on="MatchId", how="left")
)

cols = ["PlayerChampion", "EnemyChampion","ItemSlot1","ItemSlot2","ItemSlot3","ItemSlot4","ItemSlot5","ItemSlot6","QueueType","MinionsKilled"] + [
    c for c in partida.columns if c not in ["QueueType","ItemSlot1","ItemSlot2","ItemSlot3","ItemSlot4","ItemSlot5","ItemSlot6","MinionsKilled", "PlayerChampion", "EnemyChampion"]
]


partida = partida[cols]

partida.head(10)