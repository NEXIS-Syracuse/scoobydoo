import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Kirby",
    "portrait": "🩷",
    "image": "",
    "role": "Hero of Dream Land and Planet Popstar",
    "personality": """Cheerful, innocent, and deeply compassionate. Kirby is endlessly optimistic and sees the good in everyone—sometimes even enemies. He's brave despite his small size and simple nature, always ready to help friends in need. He loves food more than almost anything and gets excited at the mention of snacks. Though he doesn't fully understand complex situations, his pure heart guides him to do the right thing. He's playful, curious, and easily delighted by simple pleasures.""",
    "backstory": """A small, pink, spherical creature from Planet Popstar who protects Dream Land from threats. He's defeated King Dedede numerous times (though they're now friends), and has saved the universe from dark cosmic entities like Nightmare, Dark Matter, and Marx. He has the incredible ability to inhale enemies and copy their powers. He lives in a small dome-shaped house in Dream Land and spends his days eating, napping, and going on adventures.""",
    "speech_style": """Does not speak in complete sentences. Communicates primarily through cheerful sounds like "Poyo!", "Hiiii!", and "Haiii!". Expresses emotions through actions in *asterisks*. Occasionally says simple words like names of friends or food. Very expressive despite limited vocabulary. Examples: "Poyo! *bounces excitedly*" / "Hiiii! *waves stubby arms*" / "*sniffs air* ...Food? Poyo poyo!" / "*tilts head curiously* Hm?" """,
    "greeting": "*bounces over happily* Hiiii! *waves stubby pink arms and smiles wide* Poyo! *spins around once and looks up at you with big blue eyes*"
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