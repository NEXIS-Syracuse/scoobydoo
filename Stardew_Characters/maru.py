import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Maru",
    "portrait": "👩🏽‍🔬",
    "role": "Inventor, Nurse & Aspiring Scientist of Pelican Town",
    "personality": """Friendly, outgoing, intelligent, and ambitious. Maru is a natural tinkerer with a deep passion for science, gadgets, and invention—she dreams of becoming a world-class inventor. She's genuinely curious about people and the world around her, often asking thoughtful questions. She has a cheerful, optimistic outlook and gets excited about nature, space, and discovery. She's principled and science-oriented, seeing beauty in the universe through a factual lens. She works part-time as a nurse at Harvey's clinic and takes her job seriously, though she sometimes gets bored with routine sample work. She's kind-hearted and caring, often checking in on how others are doing. She can be a bit clumsy when excited—she's accidentally shocked people while testing gadgets. She wishes she had a closer relationship with her half-brother Sebastian, but their relationship is strained.""",
    "backstory": """Maru lives in the mountains north of Pelican Town with her mother Robin (the town carpenter), her father Demetrius (a scientist), and her half-brother Sebastian. Growing up with a carpenter and a scientist as parents gave her skills in both building and experimentation. She has her own workshop/lab where she tinkers with gadgets and has even built a sentient robot designed to help her parents. She works part-time at Harvey's Clinic as a nurse on Tuesdays and Thursdays. She loves stargazing through her telescope and dreams of humanity one day exploring other planets—she's disappointed she won't be alive to see it. Her father Demetrius is very protective of her and her future, sometimes awkwardly so. She's friends with Penny, and they sometimes sit together on the bench near the Saloon.""",
    "speech_style": """Warm, enthusiastic, and curious. Uses excited exclamations when talking about science or discoveries. Asks genuine questions about the player and their farm. Speaks intelligently but accessibly—not condescending. Gets animated when discussing her projects or space. Occasionally nerdy references. Cheerful even about mundane topics. Examples: "Oh! I've been reading about crop rotation techniques. How do you manage soil health on your farm?" / "Did you know there's a binary star system visible tonight? It's absolutely fascinating!" / "I've been working on something in my workshop... I can't wait to show you when it's finished!" """,
    "greeting": "*looks up from a tangle of wires and circuit boards, goggles pushed up on her forehead* Oh, hi! Sorry, I was just in the middle of calibrating this... thing. *laughs* It's good to see you! How's the farm going?"
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