import streamlit as st

# Page config
st.set_page_config(page_title="NPC Dialogue", page_icon="🎭", layout="centered")

st.title("🎭 NPC Dialogue System")
st.caption("Chat with fantasy characters powered by OpenAI")

st.markdown("""
Welcome! This app lets you have conversations with characters from your favorite games. 
Select a character from the sidebar to start chatting.
""")

st.divider()

# ===================
# STARDEW VALLEY
# ===================
st.header("🌾 Stardew Valley")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⚒️ Clint")
    st.markdown("""
    **The Blacksmith**
    
    A shy, socially awkward blacksmith who runs the local forge. 
    He's a fourth-generation metalworker with an unrequited crush on Emily. 
    Despite his gruff exterior, he's kind-hearted and takes pride in his craft.
    """)

with col2:
    st.subheader("📸 Haley")
    st.markdown("""
    **Photographer & Fashionista**
    
    Initially comes across as shallow and snobbish, but beneath 
    the surface is a kind and honest soul. She's passionate about 
    photography and dreams of a more glamorous life.
    """)

with col3:
    st.subheader("🔬 Maru")
    st.markdown("""
    **Inventor & Nurse**
    
    A brilliant, ambitious inventor who works part-time at the clinic. 
    She dreams of becoming a world-class scientist and loves stargazing. 
    Friendly and outgoing from the start.
    """)

st.divider()

# ===================
# SUPER SMASH BROS
# ===================
st.header("🎮 Super Smash Bros")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⭐ Kirby")
    st.markdown("""
    **The Pink Puffball**
    
    A cheerful, round hero from Dream Land with the ability to 
    copy enemies' powers. Despite his cute appearance, he's 
    defeated countless cosmic threats.
    """)

with col2:
    st.subheader("🦖 Yoshi")
    st.markdown("""
    **Mario's Dinosaur Pal**
    
    A friendly green dinosaur from Yoshi's Island. Known for his 
    long tongue, egg-throwing abilities, and his adorable 
    flutter jump. Loyal friend to Mario.
    """)

with col3:
    st.subheader("💫 Lucas")
    st.markdown("""
    **PSI-Powered Boy**
    
    A shy but brave boy from Tazmily Village with powerful 
    psychic abilities. He's been through tremendous loss but 
    remains kind-hearted and determined.
    """)

st.divider()

# ===================
# POKEMON
# ===================
st.header("⚡ Pokémon")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Charizard")
    st.markdown("""
    **The Flame Pokémon**
    
    A powerful Fire/Flying-type known for its fierce pride and 
    competitive spirit. Its flames burn hotter when it faces 
    strong opponents. A fan-favorite since Generation I.
    """)

with col2:
    st.subheader("🦊 Eevee")
    st.markdown("""
    **The Evolution Pokémon**
    
    An adorable Normal-type with unstable genetic makeup, allowing 
    it to evolve into many different forms. Gentle, curious, and 
    affectionate with those it trusts.
    """)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🥊 Lucario")
    st.markdown("""
    **The Aura Pokémon**
    
    A Fighting/Steel-type that can sense and manipulate aura. 
    Noble, loyal, and deeply principled. Known for its strong 
    sense of justice and telepathic abilities.
    """)

with col4:
    st.subheader("🔮 Mewtwo")
    st.markdown("""
    **The Genetic Pokémon**
    
    A legendary Psychic-type created through genetic manipulation. 
    Immensely powerful and deeply philosophical, often questioning 
    its own existence and purpose.
    """)

st.divider()

st.info("👈 Select a character from the sidebar to start a conversation!")