import requests

def get_champion_mapping() -> dict:
# Funcao que faz um mapeamento de todos os personagens do jogo e sua url de icon
    url = "https://ddragon.leagueoflegends.com/cdn/14.24.1/data/pt_BR/champion.json"
    response = requests.get(url)
    data = response.json()
    return {champ: f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champ}.png" for champ in data["data"].keys()}

def get_champion_rules() -> dict:
# Funcao que traz os stats dos personagens do jogo
    url = "https://ddragon.leagueoflegends.com/cdn/14.24.1/data/pt_BR/champion.json"
    response = requests.get(url)
    data = response.json()

    result = {}

    for champ_name, champ_info in data["data"].items():
        attack = champ_info["info"]["attack"]
        magic = champ_info["info"]["magic"]

        if attack > magic:
            damage = "AD"
        elif magic > attack:
            damage = "AP"
        else:
            damage = "Misto"
        result[champ_name] = {
            "Attack": damage,
            "Range": "Ranged" if champ_info["stats"]["attackrange"] >= 350 else "Melee",
            "Class": champ_info["tags"]
        }

    return result