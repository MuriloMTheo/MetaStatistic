from src.services.tierlist_service import TierListService
from src.etl.extract_champions_infos import get_champion_rules
from src.config.settings import CLASS_LACKS_PRIORITY

def recommend_champions(user_role: str, ally_profile: dict, enemy_profile: dict) -> list:
# Função de Recomendação -> 1- Verificação de Tipagem de Dano.
    service = TierListService()
    df = service.get_tier_list(user_role.upper())

    rules = get_champion_rules()

    # Altera df para receber uma coluna com os atributos dos campeões
    df["Attack"] = df["PlayerChampion"].map(lambda champ: rules[champ]["Attack"] if champ in rules else None)
    df["Range"]  = df["PlayerChampion"].map(lambda champ: rules[champ]["Range"]  if champ in rules else None)
    df["Class"]  = df["PlayerChampion"].map(lambda champ: rules[champ]["Class"]  if champ in rules else None)

    df = df.dropna(subset=["Attack", "Range", "Class"])

    has_ally  = (ally_profile["qntAp"] + ally_profile["qntAd"]) > 0 # Retorna True or False
    has_enemy = (enemy_profile["qntAp"] + enemy_profile["qntAd"]) > 0

    damage_filter = None

    if has_ally and has_enemy:
        # Olha o que falta no aliado mas sobra no inimigo
        missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in ally_profile["classes"] and cls in enemy_profile["classes"]]
        ally_lacks_ad = ally_profile["qntAd"] == 0 and enemy_profile["qntAd"] > 0
        ally_lacks_ap = ally_profile["qntAp"] == 0 and enemy_profile["qntAp"] > 0

        if ally_lacks_ad and not ally_lacks_ap:
            damage_filter = "AD"
        elif ally_lacks_ap and not ally_lacks_ad:
            damage_filter = "AP"

    elif has_ally:
        # Só olha o que falta no aliado
        missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in ally_profile["classes"]]

        if ally_profile["qntAd"] == 0:
            damage_filter = "AD"
        elif ally_profile["qntAp"] == 0:
            damage_filter = "AP"

    elif has_enemy:
        # Recomenda o oposto do que o inimigo tem mais
        missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in enemy_profile["classes"]]        

        if enemy_profile["qntAd"] > enemy_profile["qntAp"]:
            damage_filter = "AD"
        elif enemy_profile["qntAp"] > enemy_profile["qntAd"]:
            damage_filter = "AP"

    if damage_filter:
        filtered_df = df[df["Attack"].isin([damage_filter, "Misto"])]
        if filtered_df.empty:
            filtered_df = df  #fallback
    else:
        filtered_df = df

    # Função de Recomendação -> 2- Verificação da classe.
    recommended_classes = []
    for cls in missing_classes:
        recommended_classes.extend(CLASS_LACKS_PRIORITY[cls])
    recommended_classes = list(set(recommended_classes))
    # Aplicando Lambda pois Class é uma lista, isin direto NÃO compararia nesse caso.
    filtered_df = filtered_df[filtered_df["Class"].apply(lambda classes: any(c in recommended_classes for c in classes))]

    # Função de Recomendação -> 3- Verificação de range.
    if user_role != "adc" and ally_profile["rival_range"]:
        rival_range = ally_profile["rival_range"]
        opposite_range = "Melee" if rival_range == "Ranged" else "Ranged"

        range_filtered_df = filtered_df[filtered_df["Range"] == opposite_range]

        if not range_filtered_df.empty:
            best_range_score = range_filtered_df["WilsonScore"].max() # Busca pelo melhor WR para o range filtrado.
            percentile_75 = filtered_df["WilsonScore"].quantile(0.75) # Retorna o valor do WR mínimo para estar entre os melhores 25%.

            if best_range_score >= percentile_75: # Se o melhor WR for maior que o mínimo para estar entre os 25%, entra.
                    filtered_df = range_filtered_df
        else:
            filtered_df
    #return damage_filter, recommended_classes, missing_classes
    return filtered_df

if __name__ == "__main__":
    #testee: ambos os times preenchidos
    ally = {
        "qntAp": 2,
        "qntAd": 0,
        "classes": ["Mage", "Support"],
        "rival_range": "Ranged"
    }
    enemy = {
        "qntAp": 1,
        "qntAd": 3,
        "classes": ["Tank", "Fighter", "Tank", "Marksman"]
    }

    result = recommend_champions("jungle", ally, enemy)
    print(result)