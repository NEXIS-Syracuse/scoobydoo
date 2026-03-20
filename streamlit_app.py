import streamlit as st

charizard = st.Page("Pokemon_Characters/charizard.py", title="HW 1", icon="📄")
eevee = st.Page("Pokemon_Characters/eevee.py", title="HW 2 - URL Summarizer", icon="🌐")
mewtwo = st.Page("Pokemon_Characters/mewtwo.py", title="HW 3 - URL Chatbot", icon=":material/description:")
lucario = st.Page("Pokemon_Characters/lucario.py", title ="HW 4 - iSchool Org Chatbot", icon=":material/description:")
clint = st.Page("Stardew_Characters/clint.py", title ="HW 5 - SU Org Memory Chatbot", icon=":material/description:")
maru = st.Page("Stardew_Characters/maru.py", title ="HW 5 - SU Org Memory Chatbot", icon=":material/description:")
haley = st.Page("Stardew_Characters/haley.py", title ="HW 5 - SU Org Memory Chatbot", icon=":material/description:")



pg = st.navigation([charizard, eevee, mewtwo, lucario, clint, maru, haley])

st.set_page_config(page_title="NPC Playground", page_icon="🎭")

pg.run()