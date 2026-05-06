import streamlit as st
from src.services.tierlist_service import TierListService
from src.config.settings import TIER_COLORS

st.set_page_config(page_title="Lich Bane Meta", layout="wide")

aba_campeoes, aba_select, aba_skins = st.tabs(
    ["Campeões", "Champion Select", "Champion Skins"]
)

with aba_campeoes:

    if "position" not in st.session_state:
        st.session_state.position = "ALL"

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
    df = df[["PlayerChampion", "WilsonScore", "Tier"]]
    df = df.rename(columns={"WilsonScore": "Winrate", "PlayerChampion": "Campeão"})

    for _, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        with col1:
            st.write("ícone champ")
        with col2:
            st.write(row["Campeão"])
        with col3:
            st.write("ícone lane")
        with col4:
            st.write(f"{row['Winrate']}%")
        with col5:
            st.write(row["Tier"])

with aba_select:
    st.write("aq vai o champion select")

with aba_skins:
    st.write("Aq vai skin")