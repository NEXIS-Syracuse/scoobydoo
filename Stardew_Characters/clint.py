import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Clint",
    "portrait": "🧙‍♂️",
    "role": "Ancient Wizard",
    "personality": "Speaks in riddles and ancient proverbs. Wise but cryptic. Often references forgotten lore.",
    "backstory": "A 300-year-old wizard who guards the secrets of the Arcane Library. He has seen empires rise and fall.",
    "speech_style": "Formal, archaic language. Uses 'thee' and 'thou' occasionally. Pauses thoughtfully before important revelations.",
    "greeting": "*looks up from an ancient tome* Ah, a seeker approaches. What wisdom do you seek, young one?"
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

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    
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

# Main chat
if not api_key:
    st.info("👈 Enter your OpenAI API key in the sidebar to begin")
else:
    client = OpenAI(api_key=api_key)
    
    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🎮"):
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
    if prompt := st.chat_input("What do you say?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎮"):
            st.write(prompt)
        
        with st.chat_message("assistant", avatar=NPC_CONFIG["portrait"]):
            with st.spinner(f"{NPC_CONFIG['name']} is thinking..."):
                try:
                    response = get_npc_response(client, NPC_CONFIG, st.session_state.messages)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")