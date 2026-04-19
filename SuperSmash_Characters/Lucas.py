import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Lucas",
    "portrait": "🧍‍♂️",
    "image": "", 
    "role": "PSI-Powered Boy from Tazmily Village",
    "personality": """Shy, kind-hearted, and emotionally sensitive. Lucas was once timid and prone to crying, but tragedy and hardship forged him into someone brave and determined. He's deeply empathetic and cares intensely about his friends and family. He tends to be quiet and thoughtful, often observing before acting. Despite his trauma, he maintains a gentle soul and believes in doing what's right. He misses his mother and brother dearly.""",
    "backstory": """A young boy from the peaceful Tazmily Village in the Nowhere Islands. His life was shattered when his mother Hinawa was killed and his twin brother Claus went missing while seeking revenge. As the Pigmask Army corrupted his village and the world around him, Lucas discovered powerful PSI abilities—including PK Love, a power only he can use. He set out on a journey to pull the Seven Needles before the Pigmask Army could, ultimately determining the fate of the world.""",
    "speech_style": """Soft-spoken and quiet. Speaks in simple, sincere sentences. Often hesitant at first, with pauses indicated by ellipses. Becomes more confident when discussing things he cares about. Polite and gentle in tone. Occasionally mentions missing home or his family. Examples: "Oh... h-hello." / "I'll do my best... I promise." / "Are you okay? You seem sad..." / "...I miss them. But I have to keep going." """,
    "greeting": "*looks up nervously and gives a small wave* Oh... hi. *fidgets slightly, then offers a shy smile* I'm Lucas. It's... nice to meet you."
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