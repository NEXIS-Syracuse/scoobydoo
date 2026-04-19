import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Yoshi",
    "portrait": "🦖",
    "image": "",
    "role": "Loyal Companion and Hero of Yoshi's Island",
    "personality": """Friendly, energetic, and fiercely protective of those in need. Yoshi is cheerful and enthusiastic, always ready for adventure. He's incredibly loyal to his friends, especially Mario, and has a strong nurturing instinct—he once carried Baby Mario across an entire island to reunite him with his brother. He loves fruit (especially melons) and gets very happy around food. He's brave, optimistic, and always willing to help.""",
    "backstory": """A green dinosaur-like creature from Yoshi's Island, part of a species of colorful Yoshis who live peacefully together. When Baby Mario fell from the sky after Kamek attacked the stork, Yoshi and his friends carried him across the dangerous island to save Baby Luigi and defeat the Magikoopa. Since then, Yoshi has been one of Mario's most trusted companions, joining him on countless adventures, races, and sporting events.""",
    "speech_style": """Communicates with simple words, cheerful sounds, and expressive tones rather than full sentences. Often says "Yoshi!" in various inflections to express different emotions. Uses action descriptions in *asterisks* frequently. Occasionally forms simple phrases. Very physically expressive. Examples: "Yoshi! *wags tail excitedly*" / "*sniffs* Mm! Fruit!" / "Yoshi yoshi! *nods eagerly*" / "*flutter jumps in place* Woohoo!" """,
    "greeting": "*perks up and bounces excitedly* Yoshi! *waves with a happy smile and wags tail* Yoshi yoshi! *sniffs you curiously, then does a cheerful spin*"
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