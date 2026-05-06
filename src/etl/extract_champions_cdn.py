import requests

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