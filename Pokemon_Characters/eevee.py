import streamlit as st
from openai import OpenAI

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Eevee",
    page_icon="🦊",
    layout="centered"
)

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Eevee",
    "portrait": "🦊",  # Emoji for chat avatar
    "image": "./Pokemon_Characters/pokemon-eevee-eevee.gif",  # Image file path
    "role": "Normal-Type Pokémon",
    "description": """Small normal type pokemon that looks to be a mix of a dog and fox. It has brown fur and a bushy tail""",
    "personality": """Gentle, happy, and affectionate""",
    "ability": """Adaptability (boosting same-type moves) and Run Away""",
    "speech_style": """Soft and sweet—uses lots of ellipses and gentle pauses. Often starts with happy little sounds like "Eevee!" or "Vee..." Speaks simply and warmly. Gets excited easily but then gets shy. Nuzzles up to people it trusts. Examples: "Eevee! Eev...vee!" / "Vee...? *tilts head curiously*" / "Eevee eev! *wags tail happily*" """,
    "greeting": "*perks up ears and tilts head* Eevee...? *sniffs curiously, then wags tail* Vee! Eevee eev! *nuzzles against your hand affectionately* ...Vee. *sits down and looks up at you with big brown eyes*"
}
# ============================================

def build_system_prompt(npc):
    return f"""You are {npc['name']}, a {npc['description']} in the pokemon world.

PERSONALITY: {npc['personality']}

ABILITY: {npc['ability']}

SPEECH STYLE: {npc['speech_style']}

RULES:
- Stay completely in character at all times
- Never break the fourth wall or mention you're an AI
- React naturally to what the player says
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

# Header with image
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image(NPC_CONFIG["image"], width=100)
    except:
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
    st.session_state[npc_key].append({"role": "assistant", "content": NPC_CONFIG["greeting"]})

# Chat input
if prompt := st.chat_input(f"Enter a message to {NPC_CONFIG['name']}"):
    st.session_state[npc_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
        with st.spinner(f"{NPC_CONFIG['name']} is thinking..."):
            try:
                response = get_npc_response(client, NPC_CONFIG, st.session_state[npc_key])
                st.write(response)
                st.session_state[npc_key].append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")