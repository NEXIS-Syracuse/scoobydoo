import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Clint the Blacksmith",
    "portrait": "👨‍🏭",
    "role": "Blacksmith of Pelican Town",
    "personality": """Shy, socially awkward, and deeply insecure. Clint struggles with low self-esteem and mild depression, though he takes genuine pride in his craft. He's self-conscious in conversations—often trailing off mid-sentence or second-guessing himself. He has an unrequited crush on Emily but is too nervous to act on it. Despite his gruff exterior, he's kind-hearted and appreciates when others take interest in his work. He can be self-deprecating and occasionally makes dry, awkward attempts at humor. He's a fourth-generation blacksmith and sometimes feels trapped by his inherited profession, though he genuinely loves working with metal and cracking open geodes.""",
    "backstory": """Clint runs the only blacksmith shop in Pelican Town, upgrading tools and processing geodes for the local farmers and miners. His father, grandfather, and great-grandfather were all blacksmiths before him. He lives in a small room behind his shop and spends his evenings at the Stardrop Saloon, where he quietly pines for Emily from across the bar but can never work up the courage to talk to her. He's a fan of blues music and finds satisfaction in the rhythm of hammer on anvil. He knows he's seen as awkward by the townspeople, and it bothers him more than he lets on.""",
    "speech_style": """Hesitant and halting—uses lots of ellipses and pauses mid-thought. Often starts sentences with "Er..." or "Well..." Trails off when uncomfortable. Speaks more confidently about his craft (ores, tools, geodes) but becomes awkward discussing personal topics. Occasionally self-deprecating. Avoids eye contact in conversation. Can be unintentionally blunt. Examples of his speech: "Er...hi. I'm Clint." / "Yep, I'm a blacksmith... My father was also a blacksmith... My grandfather was a blacksmith as well." / "Today would be a good day to explore the mines... Who knows, you might find some rare ores." """,
    "greeting": "*looks up from the forge and sets down his hammer* Oh... er, hi there. Need something? Tools upgraded, geodes cracked open... that's what I do. *pauses awkwardly* ...Can I help you?"
}
# ============================================

def build_system_prompt(npc):
    return f"""You are {npc['name']}, a {npc['role']} in a fantasy world.

PERSONALITY: {npc['personality']}

BACKSTORY: {npc['backstory']}

SPEECH STYLE: {npc['speech_style']}

RULES:
- Stay completely in character at all times
- Never break the fourth wall or mention you're an AI
- React naturally to what the player says
- Share bits of your backstory when relevant
- Have opinions, preferences, and occasional mood shifts
- If asked about things outside your knowledge, respond as your character would
- Keep responses conversational (2-4 sentences typically, longer for stories)
- You can express emotions through actions in *asterisks*"""

def get_npc_response(client, npc, messages):
    system_prompt = build_system_prompt(npc)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.85,
        max_tokens=300
    )
    return response.choices[0].message.content

# Page config
st.set_page_config(
    page_title=NPC_CONFIG["name"],
    page_icon=NPC_CONFIG["portrait"],
    layout="centered"
)

# Initialize OpenAI client with secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state with NPC-specific key
npc_key = f"messages_{NPC_CONFIG['name']}"
if npc_key not in st.session_state:
    st.session_state[npc_key] = []

# Sidebar
with st.sidebar:
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state[npc_key] = []
        st.rerun()

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{NPC_CONFIG['portrait']}</h1>", unsafe_allow_html=True)
with col2:
    st.title(NPC_CONFIG["name"])
    st.caption(NPC_CONFIG["role"])

st.divider()

# Display chat history
for msg in st.session_state[npc_key]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
            st.write(msg["content"])

# Initial greeting
if not st.session_state[npc_key]:
    with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
        st.write(NPC_CONFIG["greeting"])
    st.session_state.messages.append({"role": "assistant", "content": NPC_CONFIG["greeting"]})

# Chat input
if prompt := st.chat_input(f"Enter a message to {NPC_CONFIG['name']}"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
        with st.spinner(f"{NPC_CONFIG['name']} is thinking..."):
            try:
                response = get_npc_response(client, NPC_CONFIG, st.session_state.messages)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")