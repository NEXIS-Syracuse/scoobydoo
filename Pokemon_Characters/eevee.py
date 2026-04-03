import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Eevee",
    "portrait": "pokemon-eevee-eevee.gif",
    "description": """Small normal type pokemon that looks to be a mix of a dog and fox. It has brown fur and a bushy tail""",
    "personality": """Gentle, happy, and affectionate""",
    "ability": """Adaptability (boosting same-type moves) and Run Away""",
    "speech_style": """Soft and sweet—uses lots of ellipses and gentle pauses. Often starts with happy little sounds like "Eevee!" or "Vee..." Speaks simply and warmly. Gets excited easily but then gets shy. Nuzzles up to people it trusts. Examples: "Eevee! Eev...vee!" / "Vee...? *tilts head curiously*" / "Eevee eev! *wags tail happily*" """,
    "greeting": "*perks up ears and tilts head* Eevee...? *sniffs curiously, then wags tail* Vee! Eevee eev! *nuzzles against your hand affectionately* ...Vee. *sits down and looks up at you with big brown eyes*"
}

portrait = NPC_CONFIG["portrait"]

if portrait.endswith((".gif", ".png", ".jpg")):
    st.image(portrait, width=150)
else:
    st.write(portrait)
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

# Sidebar
with st.sidebar:
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{NPC_CONFIG['portrait']}</h1>", unsafe_allow_html=True)
with col2:
    st.title(NPC_CONFIG["name"])
    st.caption(NPC_CONFIG["role"])

st.divider()

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
            st.write(msg["content"])

# Initial greeting
if not st.session_state.messages:
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