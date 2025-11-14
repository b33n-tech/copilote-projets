import streamlit as st
from typing import Dict, List

st.set_page_config(page_title="StartUp GPS — Prototype", layout="wide")

# ---------- Sample data model (7 blocks -> modules -> cards/tasks) ----------
DEFAULT_STRUCTURE = {
    "Admin & Légal": {
        "emoji": "🔵",
        "modules": {
            "Forme juridique": [
                {"title": "Choisir la forme (1 phrase)", "steps": ["Ecris en 1 phrase la forme juridique souhaitée", "Pourquoi ce choix ? (2 lignes)", "Checklist: SIRET, Statuts, KBIS"]},
                {"title": "SIRET & immatriculation", "steps": ["Lien/Procédure locale (manuel)", "Collecter pièces: ID, adresse, justificatif"]},
            }
        }
    },
    "Finances": {
        "emoji": "🟢",
        "modules": {
            "Runway & Budget": [
                {"title": "Estimations coûts fixes", "steps": ["Liste tes coûts fixes mensuels (3 items minimum)", "Estime un montant pour chaque item"]},
                {"title": "Pricing rapide", "steps": ["Décris l'offre en 1 phrase", "Propose 2 options de prix"]},
            ]
        }
    },
    "Produit": {
        "emoji": "🟣",
        "modules": {
            "MVP": [
                {"title": "Décrire le MVP (1 phrase)", "steps": ["Décris ton MVP en 1 phrase", "3 composants essentiels"]},
                {"title": "Critères d'acceptation", "steps": ["Qu'est-ce qui prouve que le MVP fonctionne ? (KPI) ", "Score minimal d'acceptation"]},
            ]
        }
    },
    "Validation / Marché": {
        "emoji": "🟠",
        "modules": {
            "Interviews utilisateurs": [
                {"title": "Script d'entretien", "steps": ["3 questions ouvertes", "Note 10 retours minimum"]},
            ]
        }
    },
    "Acquisition": {
        "emoji": "🟡",
        "modules": {
            "Canal initial": [
                {"title": "Choisir 1 canal", "steps": ["Sélectionne un canal unique (ex: LinkedIn)", "Message d'approche — template fourni"]},
            ]
        }
    },
    "RH / Structure": {
        "emoji": "🟤",
        "modules": {
            "Roles essentiels": [
                {"title": "Définir 1 rôle critique", "steps": ["Qui fait quoi ? 1 ligne par rôle", "Quel est le livrable attendu ?"]},
            ]
        }
    },
    "Opérations": {
        "emoji": "🔴",
        "modules": {
            "Delivery checklist": [
                {"title": "Process de livraison", "steps": ["Étapes pour livrer la 1ère version", "Qui valide ?"]},
            ]
        }
    },
}

# ---------- Session State helpers ----------
if "structure" not in st.session_state:
    st.session_state.structure = DEFAULT_STRUCTURE

if "selected_block" not in st.session_state:
    st.session_state.selected_block = None

if "selected_module" not in st.session_state:
    st.session_state.selected_module = None

if "selected_card_index" not in st.session_state:
    st.session_state.selected_card_index = 0

if "progress" not in st.session_state:
    # store completion as a dict: block -> module -> list of booleans per card
    st.session_state.progress = {}
    for block, bdata in st.session_state.structure.items():
        st.session_state.progress[block] = {}
        for module, cards in bdata["modules"].items():
            st.session_state.progress[block][module] = [False] * len(cards)


# ---------- Utility functions ----------

ICON_MAP = {
    "done": "✅",
    "in_progress": "🟡",
    "todo": "⚪",
}


def render_header():
    st.markdown("# StartUp GPS — Prototype")
    st.markdown("_Un prototype Streamlit qui illustre l'UX: blocs colorés, cartes, et guidage étape par étape._")


def get_block_progress(block_name: str) -> float:
    modules = st.session_state.progress.get(block_name, {})
    total = 0
    done = 0
    for module, arr in modules.items():
        total += len(arr)
        done += sum(1 for v in arr if v)
    return (done / total) * 100 if total > 0 else 0


def choose_block(block_name: str):
    st.session_state.selected_block = block_name
    # reset module selection
    st.session_state.selected_module = None
    st.session_state.selected_card_index = 0


def choose_module(module_name: str):
    st.session_state.selected_module = module_name
    st.session_state.selected_card_index = 0


# ---------- UI rendering ----------

render_header()

left, right = st.columns([3, 1])

with left:
    # Blocks view
    st.subheader("Parcours — Blocs")
    cols = st.columns(4)
    i = 0
    for block_name, block in st.session_state.structure.items():
        col = cols[i % 4]
        with col:
            progress = get_block_progress(block_name)
            if st.button(f"{block['emoji']}  {block_name}\n{int(progress)}%", key=f"block_{block_name}"):
                choose_block(block_name)
        i += 1

    st.markdown("---")

    # If a block is selected, show its modules as cards
    if st.session_state.selected_block:
        sb = st.session_state.selected_block
        st.subheader(f"{st.session_state.structure[sb]['emoji']}  {sb}")
        st.write(f"Progress: {int(get_block_progress(sb))}%")

        modules = st.session_state.structure[sb]["modules"]
        for module_name, cards in modules.items():
            st.markdown(f"#### {module_name}")
            # Cards grid
            card_cols = st.columns(min(4, len(cards)))
            for idx, card in enumerate(cards):
                col = card_cols[idx % len(card_cols)]
                with col:
                    status = st.session_state.progress[sb][module_name][idx]
                    st.markdown(f"**{card['title']}**")
                    st.write(ICON_MAP['done'] if status else ICON_MAP['todo'])
                    if st.button("Ouvrir", key=f"open_{sb}_{module_name}_{idx}"):
                        choose_module(module_name)
                        st.session_state.selected_card_index = idx

        st.markdown("---")

        # Card detail view if module selected
        if st.session_state.selected_module:
            mod = st.session_state.selected_module
            cards = st.session_state.structure[sb]['modules'][mod]
            idx = st.session_state.selected_card_index
            card = cards[idx]

            st.subheader(f"{card['title']}")
            steps: List[str] = card['steps']

            # We show one step at a time
            step_key = f"step_index_{sb}_{mod}_{idx}"
            if step_key not in st.session_state:
                st.session_state[step_key] = 0

            si = st.session_state[step_key]
            st.markdown(f"**Étape {si+1} / {len(steps)}**")
            st.info(steps[si])

            # Input based on step
            user_input_key = f"input_{sb}_{mod}_{idx}_{si}"
            if user_input_key not in st.session_state:
                st.session_state[user_input_key] = ""

            st.session_state[user_input_key] = st.text_area(
                "Réponse rapide (1-3 lignes)", st.session_state[user_input_key], key=user_input_key)

            coln = st.columns([1,1,1])
            with coln[0]:
                if st.button("Précédent", key=f"prev_{step_key}"):
                    if st.session_state[step_key] > 0:
                        st.session_state[step_key] -= 1
            with coln[1]:
                if st.button("Suivant", key=f"next_{step_key}"):
                    if st.session_state[step_key] < len(steps)-1:
                        st.session_state[step_key] += 1
            with coln[2]:
                if st.button("Marquer comme fait", key=f"done_{sb}_{mod}_{idx}"):
                    st.session_state.progress[sb][mod][idx] = True
                    st.success("Tâche marquée comme faite ✅")

            st.markdown("---")
            # show small examples/templates
            with st.expander("Exemples & Templates"):
                st.write("- Exemple court 1\n- Template message d'approche\n- Mini-checklist")


with right:
    # Sidebar-like utilities
    st.subheader("Outils rapides")
    st.write("**Vue globale**")
    overall_done = 0
    overall_total = 0
    for block in st.session_state.progress.values():
        for module_arr in block.values():
            overall_total += len(module_arr)
            overall_done += sum(1 for v in module_arr if v)
    st.progress(int((overall_done / overall_total) * 100) if overall_total else 0)
    st.write(f"{overall_done} / {overall_total} tâches")

    st.markdown("---")
    st.subheader("Onboarding (rapide)")
    if st.button("Nouveau projet — Questionnaire"):
        st.session_state.selected_block = None
        st.session_state.selected_module = None
        st.session_state.project_name = st.text_input("Nom du projet", value="Mon projet")
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("Exporter")
    if st.button("Exporter le plan (JSON)"):
        import json
        st.download_button("Télécharger JSON", json.dumps(st.session_state.structure, ensure_ascii=False, indent=2), file_name="plan_projet.json")

    st.markdown("---")
    st.caption("Prototype minimal — utile pour tester l'UX et la logique de découpage.")


# ---------- Footer: tips ----------
st.markdown("---")
st.write("**Conseils produit**: 1) limiter le nombre d'étapes visibles; 2) n'afficher qu'un module à la fois; 3) donner des templates concrets; 4) mesurer la progression pour booster la motivation.")
