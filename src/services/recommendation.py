from src.services.tierlist_service import TierListService
from src.etl.extract_champions_infos import get_champion_rules
from src.config.settings import CLASS_LACKS_PRIORITY

def recommend_champions(user_role: str, ally_profile: dict, enemy_profile: dict) -> list:
# Função de Recomendação -> 1- Verificação de Tipagem de Dano.
    try:
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

        choice_desc = ""

        if has_ally and has_enemy:
            # Olha o que falta no aliado mas sobra no inimigo
            missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in ally_profile["classes"] and cls in enemy_profile["classes"]]
            ally_lacks_ad = ally_profile["qntAd"] == 0 and enemy_profile["qntAd"] > 0
            ally_lacks_ap = ally_profile["qntAp"] == 0 and enemy_profile["qntAp"] > 0
            equal = ally_profile["qntAp"] == enemy_profile["qntAp"] and ally_profile["qntAd"] == enemy_profile["qntAd"]

            if ally_lacks_ad and not ally_lacks_ap:
                damage_filter = "AD"
                choice_desc = "Time aliado possui MENOS dano AD que o time inimigo - Escolha de dano AD.\n\n"
            elif ally_lacks_ap and not ally_lacks_ad:
                damage_filter = "AP"
                choice_desc = "Time aliado possui MENOS dano AP que o time inimigo - Escolha de dano AP.\n\n"
            elif not equal:
                if ally_profile["qntAp"] > ally_profile["qntAd"]:
                    damage_filter = "AD"
                    choice_desc = "Ambos times possuem AD e AP. Time aliado possui menos AD - Escolha de dano AD.\n\n"
                else:
                    damage_filter = "AP"
                    choice_desc = "Ambos times possuem AD e AP. Time aliado possui menos AP - Escolha de dano AP.\n\n"

        elif has_ally:
            # Só olha o que falta no aliado
            missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in ally_profile["classes"]]

            if ally_profile["qntAd"] == 0:
                damage_filter = "AD"
            elif ally_profile["qntAp"] == 0:
                damage_filter = "AP"
            choice_desc = f'Time aliado não possui dano {damage_filter} - Escolha de dano {damage_filter}.\n\n'

        elif has_enemy:
            # Recomenda o oposto do que o inimigo tem mais
            missing_classes = [cls for cls in CLASS_LACKS_PRIORITY if cls not in enemy_profile["classes"]]        

            if enemy_profile["qntAd"] > enemy_profile["qntAp"]:
                damage_filter = "AD"
            elif enemy_profile["qntAp"] > enemy_profile["qntAd"]:
                damage_filter = "AP"
            choice_desc = f'Time inimigo possui mais dano {damage_filter} - Escolha de dano {damage_filter}.\n\n'

        if damage_filter and user_role.upper() != "ADC":
            filtered_df = df[df["Attack"].isin([damage_filter, "Misto"])]
            if filtered_df.empty:
                filtered_df = df
        else:
            filtered_df = df
            choice_desc = "Sem atribuição ao filtro de tipagem de dano - Provável quantidade igual em ambos os times ou escolha de Atirador.\n\n"

        # Função de Recomendação -> 2- Verificação da classe.
        recommended_classes = []
        for cls in missing_classes:
            recommended_classes.extend(CLASS_LACKS_PRIORITY[cls])
        recommended_classes = list(set(recommended_classes))
        # Aplicando Lambda pois Class é uma lista, isin direto NÃO compararia nesse caso.
        class_filtered  = filtered_df[filtered_df["Class"].apply(lambda classes: any(c in recommended_classes for c in classes))]
        if not class_filtered.empty:
            filtered_df = class_filtered
        choice_desc += f"Classes ausentes no time aliado: {missing_classes}.\n\nClasses recomendadas: {recommended_classes}.\n\n"

        # Função de Recomendação -> 3- Verificação de range.
        if user_role.upper() != "ADC" and ally_profile["rival_range"]:
            rival_range = ally_profile["rival_range"]
            opposite_range = "Melee" if rival_range == "Ranged" else "Ranged"

            range_filtered_df = filtered_df[filtered_df["Range"] == opposite_range]

            if not range_filtered_df.empty:
                best_range_score = range_filtered_df["WilsonScore"].max() # Busca pelo melhor WR para o range filtrado.
                percentil = (filtered_df["WilsonScore"] < best_range_score).mean() * 100 # Indica a porcentagem de valores que são menores que o valor analisado.

                if percentil >= 85: # Se o melhor WR estiver entre os 15% melhores WR, é aplicado o filtro de range.
                        filtered_df = range_filtered_df
                        choice_desc += "Filtro de range aplicado.\n\n"
            else:
                filtered_df = filtered_df
        elif user_role.upper() == "ADC":
            exception_champ = ["Nilah"]
            filtered_df = filtered_df[filtered_df["Class"].apply(lambda classes: "Marksman" in classes) | filtered_df["PlayerChampion"].isin(exception_champ)]

        recommend_champions_top3 = filtered_df.nlargest(3, "WilsonScore")[["PlayerChampion", "Tier", "WilsonScore", "Attack"]].rename(columns={
            "PlayerChampion": "Champion",
            "WilsonScore": "Winrate",
            "Attack": "Dano"}).to_dict(orient="records")

        return choice_desc, recommend_champions_top3
    except Exception as e:
        print(f'Erro ao executar a função recommend_champions: {e}')

if __name__ == "__main__":
    ally = {
        "qntAp": 1,
        "qntAd": 3,
        "classes": ["Fighter","Assassin","Fighter","Marksman","Mage","Tank","Support"],
        "rival_range": "Ranged"
    }
    enemy = {
        "qntAp": 3,
        "qntAd": 2,
        "classes": ["Fighter","Tank","Assassin","Mage","Mage","Assassin","Marksman","Mage","Tank","Support"]
    }

    result = recommend_champions("mid", ally, enemy)
    print(result)

    #service = TierListService()
    #print(service.df[service.df["PlayerChampion"] == "Leona"])
    #print(service.df[service.df["PlayerChampion"] == "Ahri"])
    #print(service.df[service.df["PlayerChampion"] == "Caitlyn"])