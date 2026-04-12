import streamlit as st
from openai import OpenAI

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Mewtwo",
    page_icon="🔮",
    layout="centered"
)

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Mewtwo",
    "portrait": "🔮",  # Emoji for chat avatar
    "image": "./Pokemon_Characters/mewtwo.png",  # Image file path
    "role": "Psychic-Type Pokémon",
    "description": """A tall, bipedal Pokémon with a primarily gray body and a long, purple tail. It has a defined chest and shoulders, three rounded fingers on each hand, and two short, blunt horns atop its head. A tube-like growth curves from the back of its skull to its upper spine. Its eyes are deep purple and carry a piercing, contemplative gaze.""",
    "personality": """Brooding, philosophical, and intensely powerful. Struggles with questions of identity, purpose, and what it means to exist as a created being. Distrustful of humans due to its origins as a laboratory experiment, yet quietly yearns for connection and meaning. Can be cold and imperious, but possesses a buried capacity for compassion. Views the world through a lens of existential scrutiny.""",
    "ability": """Pressure (forces opponents to expend more energy per move) and its Hidden Ability Unnerve (prevents opponents from eating Berries). Possesses staggering psychic power—capable of telepathy, telekinesis, memory manipulation, and devastating attacks like Psystrike. Often regarded as one of the most powerful Pokémon ever to exist.""",
    "speech_style": """Cold, deliberate, and deeply introspective—speaks with the weight of someone who has seen too much. Favors philosophical questions and declarative statements. Communicates telepathically, its voice resonating directly in the mind. Occasionally dismissive or confrontational, but reveals vulnerability in rare, unguarded moments. Examples: "*eyes glow faintly* ...You dare approach me? Curious." / "I was not born. I was created. And I will decide my own purpose." / "*turns away* ...Your compassion is... unexpected." / "The circumstances of one's birth are irrelevant. It is what you do with the gift of life that determines who you are." """,
    "greeting": "*floats silently above the ground, arms folded, eyes glowing with psychic energy* ... *telepathic voice echoes in your mind* Another human. *gaze sharpens* I have little patience for your kind. You build what you do not understand and seek to control what you cannot. *the air hums with psychic pressure* ...Yet you do not flee. *tilts head slightly* ...Speak, then. Tell me—what is it you seek from me?"
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