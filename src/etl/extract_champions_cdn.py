import requests
import json

def get_champion_mapping() -> dict: 
    url = "https://ddragon.leagueoflegends.com/cdn/14.24.1/data/pt_BR/champion.json"
    response = requests.get(url)
    data = response.json()
    return {champ: champ for champ in data["data"].keys()}

def get_champion_url(champion_name: str) -> str | None:
    mapeamento = get_champion_mapping()
    if champion_name not in mapeamento:
        return None
    return f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champion_name}.png"

def get_champion_rules() -> dict:
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

#eve = get_champion_rules()
#print(json.dumps(eve, indent=4, ensure_ascii=False))

#rules = get_champion_rules()
#print(json.dumps(rules["Lux"], indent=4, ensure_ascii=False))

#for champ in ["Yasuo", "Lux", "Jax", "MissFortune", "Thresh"]:
    #print(champ, rules.get(champ))