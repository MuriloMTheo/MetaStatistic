import streamlit as st
from src.services.tierlist_service import TierListService
from src.etl.extract_champions_cdn import get_champion_url
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
def load_champion_url(champion_name: str):
    return get_champion_url(champion_name)

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
                st.session_state.position = "MIDDLE"
        with adc:
            if st.button("ADCARRY"):
                st.session_state.position = "BOTTOM"
        with sup:
            if st.button("SUPORTE"):
                st.session_state.position = "SUPPORT"

    # st.write(st.session_state.position)
    service = TierListService()
    df = service.get_tier_list(st.session_state.position)

    df["WilsonScore"] = (df["WilsonScore"] * 100).round(2)
    df = df[["PlayerChampion", "WilsonScore", "Tier", "Lane"]]
    df = df.rename(columns={"WilsonScore": "Winrate"})
    
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
            with col1:
                url = load_champion_url(row["PlayerChampion"])
                if url:
                    st.image(url, width=48)
                else:
                    st.write("?")
            with col2:
                st.write(row["PlayerChampion"])
            with col3:
                st.write(row["Lane"])
            with col4:
                st.write(f"{row['Winrate']}%")
            with col5:
                st.write(row["Tier"])

with aba_select:
    st.write("aq vai o champion select")

with aba_skins:
    st.write("Aq vai skin")