import streamlit as st

intro = st.Page("intro.py", title="NPC Playground", icon=":/material/description:", default= True)
charizard = st.Page("Pokemon_Characters/charizard.py", title="Charizard", icon="🔥")
eevee = st.Page("Pokemon_Characters/eevee.py", title="Eevee", icon="🐕")
mewtwo = st.Page("Pokemon_Characters/mewtwo.py", title="Mewtwo", icon="🔮")
lucario = st.Page("Pokemon_Characters/lucario.py", title ="Lucario", icon="🔵")
clint = st.Page("Stardew_Characters/clint.py", title ="Clint", icon="⚒️")
maru = st.Page("Stardew_Characters/maru.py", title ="Maru", icon="🩺")
haley = st.Page("Stardew_Characters/haley.py", title ="Haley", icon="📸")

pg = st.navigation([intro, charizard, eevee, mewtwo, lucario, clint, maru, haley])

st.set_page_config(page_title="NPC Playground", page_icon="🎭")

pg.run()