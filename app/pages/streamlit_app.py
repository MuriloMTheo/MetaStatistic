import streamlit as st
from src.services.tierlist_service import TierListService
from src.services.recommendation import recommend_champions
from src.etl.extract_champions_infos import get_champion_mapping, get_champion_rules
from src.services.champion_select import build_ally_team_profile, build_enemy_team_profile
from src.config.settings import TIER_COLORS

st.set_page_config(page_title="Lich Bane Meta", layout="wide")

st.markdown("""
    <style>
        /*--------Botão Serviços-------------*/
                
        div[data-testid="stVerticalBlock"] {
            padding: 0.2rem 0.5rem;
            margin-bottom: 0.5px;
        }
            
        /* Container das tabs */
        div[data-baseweb="tab-list"] {
            display: flex;
            gap: 6px; /* distância menor entre tabs */
            width: 100%;
        }
        button[data-baseweb="tab"] {
            flex: 1;
            justify-content: center;
            font-size: 20px;      /* tamanho */
            font-weight: 700;     /* negrito */
            font-family: Arial;   /* fonte */
            color: white;         /* cor */
            letter-spacing: 1px;  /* espaçamento entre letras */
            text-transform: uppercase; /* MAIÚSCULO */
            padding: 14px 0;
            border: 1px solid #444;
            border-radius: 10px;
            background-color: #111;
        }

        /*Tab selecionada */
        button[data-baseweb="tab"][aria-selected="true"] {
            border-color: #E53935;
            color: #E53935;
            font-weight: 600;
        } 
            
        /*--------Botão Tier Lane-------------*/              
            
        /* REMOVE espaços padrões entre colunas */
        div[data-testid="column"] {
            padding: 0rem !important;
        }
   
        /* Botões */
        div[data-testid="stButton"] > button {
            width: 100%;
            min-height: 42px !important;
            padding: 4px 8px !important;
            border: 1px solid #444 !important;
            border-radius: 6px !important;
            background-color: transparent !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            font-family: Arial !important;
            color: white !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
            transition: all 0.15s ease;
        }
            
        /* Hover */
        div[data-testid="stButton"] > button:hover {
            border-color: #E53935 !important;
            color: #E53935 !important;
        }
            
        /* Clicado */
        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:active {
            border-color: #E53935 !important;
            color: #E53935 !important;
            box-shadow: 0 0 0 1px #E53935 !important;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_champion_mapping():
    return get_champion_mapping()

load_champion_url = load_champion_mapping()
#Colunas Principais
aba_campeoes, aba_select, aba_skins = st.tabs(["Campeões", "Champion Select", "Champion Skins"])

with aba_campeoes:

    if "position" not in st.session_state:
        st.session_state.position = "ALL"

    with st.container(border=True):
        allchamp, top, jg, mid, adc, sup = st.columns(6)

        with allchamp:
            if st.button("TODOS"):
                st.session_state.position = "ALL"
        with top:
            if st.button("TOP"):
                st.session_state.position = "TOP"
        with jg:
            if st.button("JUNGLE"):
                st.session_state.position = "JUNGLE"
        with mid:
            if st.button("MID"):
                st.session_state.position = "MID"
        with adc:
            if st.button("ADCARRY"):
                st.session_state.position = "ADC"
        with sup:
            if st.button("SUPORTE"):
                st.session_state.position = "SUPPORT"

    # st.write(st.session_state.position)
    @st.cache_data
    def load_tier_list(position: str):
        service = TierListService()
        return service.get_tier_list(position)
    df = load_tier_list(st.session_state.position)

    df["WilsonScore"] = (df["WilsonScore"] * 100).round(2)
    df = df[["PlayerChampion", "WilsonScore", "Tier", "Lane"]]
    df = df.rename(columns={"WilsonScore": "Winrate"})
    
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
            with col1:
                url = load_champion_url.get(row["PlayerChampion"])
                if url:
                    st.image(url, width=48)
                else:
                    st.empty()
            with col2:
                st.write(row["PlayerChampion"])
            with col3:
                st.write(row["Lane"])
            with col4:
                st.write(f"{row['Winrate']}%")
            with col5:
                color = TIER_COLORS.get(int(row["Tier"]), "#ffffff")
                st.markdown(f"<span style='color: {color}; font-weight: bold;'>TIER {int(row['Tier'])}</span>", unsafe_allow_html=True)

@st.cache_data(show_spinner="Carregando dados dos campeões...")
def load_rules():
    return get_champion_rules()

rules = load_rules()

with aba_select:
    st.set_page_config(page_title="Recomendador de Campeão", layout="wide")

    ROLES = {
        "top": "Topo",
        "jungle": "Selva",
        "mid": "Meio",
        "adc": "Atirador",
        "support": "Suporte",
    }

    NENHUM = "Nenhum"

    @st.cache_data(show_spinner="Carregando dados dos campeões...")
    def champion_options(rules: dict) -> list[str]:
    # Função para retornar uma lista de opções de campeões disponíveis para select
        return [NENHUM] + sorted(rules.keys())

    if "confirmed" not in st.session_state:
        st.session_state.confirmed = False

    champs_options = champion_options(rules)

    st.title("🎯 Recomendador de Campeão")
    st.caption("Escolha sua rota e preencha o que já sabe sobre as outras 9 posições.")

    user_role = st.selectbox(
        "Escolha sua rota:",
        options=list(ROLES.keys()),
        format_func=lambda key: ROLES[key],
        key="user_role",
    )

    st.divider()

    col_ally, col_enemy = st.columns(2)

    ally_champs: dict[str, str] = {}
    enemy_champs: dict[str, str] = {}

    with col_ally:
        st.subheader("🔵 Time Aliado")
        for role_key, role_label in ROLES.items():
            if role_key == user_role:
                st.text_input(
                    f"{role_label} (sua rota)",
                    value="— a recomendar —",
                    disabled=True,
                    key=f"ally_{role_key}_locked",
                )
                continue

            ally_champs[role_key] = st.selectbox(
                role_label,
                options=champs_options,
                key=f"ally_{role_key}",
            )

    with col_enemy:
        st.subheader("🔴 Time Inimigo")
        for role_key, role_label in ROLES.items():
            enemy_champs[role_key] = st.selectbox(
                role_label,
                options=champs_options,
                key=f"enemy_{role_key}",
            )

    st.divider()

    filled_others = [c for c in (*ally_champs.values(), *enemy_champs.values()) if c != NENHUM]

    if st.button("Confirmar", type="primary", use_container_width=True):
        if not filled_others:
            st.error("Selecione pelo menos um campeão em alguma das outras 9 posições.")
            st.session_state.confirmed = False
        else:
            st.session_state.confirmed = True

    if st.session_state.confirmed: #Lógica pós confirmar os campeões
        ally_list = [c for c in ally_champs.values() if c != NENHUM]
        enemy_list = [c for c in enemy_champs.values() if c != NENHUM]
        rival_champion = enemy_champs.get(user_role)
        rival_champion = rival_champion if rival_champion != NENHUM else None

        ally_profile = build_ally_team_profile(ally_list, user_role, rival_champion=rival_champion)
        enemy_profile = build_enemy_team_profile(enemy_list)

        st.success(f"Rota selecionada: **{ROLES[user_role]}**") #Apresenta o que foi escolhido

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Perfil do time aliado**")
            st.json(ally_profile)
        with col_b:
            st.markdown("**Perfil do time inimigo**")
            st.json(enemy_profile)

        desc_champ_recommend, top_3_champ_recommend = recommend_champions(user_role, ally_profile, enemy_profile)

        st.divider()
        st.subheader("Campeões Recomendados")
        st.caption(desc_champ_recommend)

        for champ in top_3_champ_recommend:
            icon_url = load_champion_url.get(champ['Champion'])

            col_icon, col_info = st.columns([1, 5])

            with col_icon:
                st.image(icon_url, width=72)

            with col_info:
                st.markdown(f"### {champ['Champion']}")
                st.markdown(
                    f"🏅 **Tier {champ['Tier']}** &nbsp;|&nbsp; "
                    f"⚔️ **{champ['Dano']}** &nbsp;|&nbsp; "
                    f"📈 **WinRate:** {round(champ['Winrate'] * 100, 1)}%"
                )

            st.divider()

with aba_skins:
    st.write("Aq vai skin")