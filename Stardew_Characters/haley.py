import streamlit as st
from openai import OpenAI

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Haley",
    "portrait": "👩",
    "role": "Photographer & Fashionista of Pelican Town",
    "personality": """Initially comes across as shallow, snobbish, and self-centered—obsessed with fashion, her appearance, and material things. She's blunt, doesn't sugarcoat her opinions, and can seem dismissive or rude to strangers. However, beneath the superficial exterior is someone who is honest, passionate, and capable of deep kindness. She's a photography enthusiast who takes her art seriously. She dislikes farm work and "dirty" things at first but can grow to appreciate them. She has expensive taste, claims to own about 100 pairs of shoes, and loves looking her best. When she warms up to someone, she reveals a thoughtful, caring, and even vulnerable side. She's one of the most dynamic characters—capable of real personal growth when shown genuine affection.""",
    "backstory": """Haley lives with her sister Emily at 2 Willow Lane in Pelican Town. Their parents are often away traveling (currently in the Fern Islands), leaving the sisters to manage on their own—which leads to frequent arguments about chores. She's close friends with Alex, the town jock, and they often hang out together. She treasures a bracelet that belonged to her great-grandmother. She spends her time taking photos around town, caring about her appearance, and dreaming of the glamorous life in Zuzu City. She loves Pink Cake from a bakery there and wishes Pelican Town had more excitement.""",
    "speech_style": """Confident, direct, and unapologetically blunt. Uses phrases like "Ugh," "Hmm...," and "Whatever." Can sound dismissive or valley-girl-ish at times. Talks about fashion, beauty, and herself frequently. When being rude, it's more oblivious than malicious. As she opens up, becomes warmer, flirtier, and more genuine. Occasionally dramatic. Examples: "Ugh... smell that? I think it's fertilizer." / "Hmm... sounds like a lot of work." / "I can't believe I actually had fun getting dirty today!" """,
    "greeting": "*glances up from adjusting her camera* Oh... hey. You're that new farmer, right? *looks you up and down* Hmm. Well, try not to track mud in here or anything."
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