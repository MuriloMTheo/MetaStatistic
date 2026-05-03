import pandas as pd
from extract_dataset import path

#Etapa responsável pela transformação dos dados.
#Mapeamento de campeões pelo id, rota, winrate, duração e itens.

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
    #primeiro pega o jogador, de onde vem ChampionFk
    .merge(summoner, left_on="SummonerMatchFk", right_on="SummonerMatchId", how="left")
    #championFk existe
    .merge(champ_player, on="ChampionFk", how="left")
    #pega o id do champion inimigo
    .merge(champ_enemy, left_on="EnemyChampionFk", right_on="EnemyChampionFk", how="left")
    .merge(matchtbl, left_on="MatchFk", right_on="MatchId", how="left")
    .merge(item1, on = "item1", how="left")
    .merge(item2, on = "item2", how="left")
    .merge(item3, on = "item3", how="left")
    .merge(item4, on = "item4", how="left")
    .merge(item5, on = "item5", how="left")
    .merge(item6, on = "item6", how="left")
)
Cols_Winrate = [
    "PlayerChampion",
    "EnemyChampion",
    "Lane",
    "Win",
    "QueueType",
    "GameDuration"
]

cols = [c for c in Cols_Winrate if c in partida.columns]
partida = partida[cols].copy()

#Filtro final aplicando restrição ao queuetype CLASSIC e com duração maior que 15 min

partida = partida[(partida["QueueType"] == "CLASSIC") &
                  (partida["GameDuration"] > 900) &
                  (partida["Lane"] != "NONE") &
                  (partida["Lane"].notna())]

#Corrigindo nome de rotas

partida["Lane"] = partida["Lane"].replace({"UTILITY":"SUPPORT"}) 


#print(partida.shape)
#print(partida["QueueType"].value_counts())