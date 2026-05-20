from src.etl.extract_champions_cdn import get_champion_rules

def build_ally_team_profile(champions: list[str]):
    rules = get_champion_rules()

    ally_team = {
        "qntAp": 0, #Somatória de quantos Ap tem no time aliado.
        "qntAd": 0, #Somatória de quantos Ad tem no time aliado.
        "classes":[], #Classes que seu time possui.
        "rival_range": None #Apenas quando existir preenchimento para o laner rival ao que o user selecionou.
    }

    for champ in champions:
        if champ and champ in rules:
            if rules[champ]["Attack"] == "AP":
                ally_team["qntAp"] += 1
            elif rules[champ]["Attack"] == "AD":
                ally_team["qntAd"] += 1
            elif rules[champ]["Attack"] == "Misto":
                ally_team["qntAp"] += 1
                ally_team["qntAd"] += 1
            ally_team["classes"].extend(rules[champ]["Class"])

def build_enemy_team_profile(champions: list[str]):
    rules = get_champion_rules()

    enemy_team = {
        "qntAp": 0, #Somatória de quantos Ap tem no time aliado.
        "qntAd": 0, #Somatória de quantos Ad tem no time aliado.
        "classes":[] #Classes que seu time possui.
    }
    for champ in champions:
        if champ and champ in rules:
            if rules[champ]["Attack"] == "AP":
                enemy_team["qntAp"] += 1
            elif rules[champ]["Attack"] == "AD":
                enemy_team["qntAd"] += 1
            elif rules[champ]["Attack"] == "Misto":
                enemy_team["qntAp"] += 1
                enemy_team["qntAd"] += 1
            enemy_team["classes"].extend(rules[champ]["Class"])