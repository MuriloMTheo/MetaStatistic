import streamlit as st

st.set_page_config(page_title="Lich Bane Meta", layout="wide")

aba_campeoes, aba_select, aba_skins = st.tabs(["Campeões", "Champion Select", "Champion Skins"])

with aba_campeoes:
    st.write("aq vai a tierlist")

with aba_select:
    st.write("aq vai o champion select")

with aba_skins:
    st.write("Aq vai skin")