import streamlit as st

st.set_page_config(page_title="Outil ultra simple", layout="wide")

# --- Structure visuelle : 5 blocs/sections ---
sections = [
    {"title": "1. Définir le problème", "placeholder": "Écris ici le problème de départ…"},
    {"title": "2. Explorer les options", "placeholder": "Liste les options, même les mauvaises…"},
    {"title": "3. Choisir une direction", "placeholder": "Quelle direction semble logique ?"},
    {"title": "4. Plan d’action simple", "placeholder": "Étapes courtes et faisables une par une…"},
    {"title": "5. Indicateurs (très simples)", "placeholder": "Comment vois-tu que ça marche ?"},
]

st.title("🧩 Outil Décisionnel Ultra Simple")
st.write("Avance bloc par bloc. C’est **visuel**, **clair**, et utilisable par un enfant.")

for section in sections:
    st.subheader(section["title"])
    st.text_area(section["title"], placeholder=section["placeholder"], height=120)
    st.divider()

st.success("Ton outil est prêt 🚀")
