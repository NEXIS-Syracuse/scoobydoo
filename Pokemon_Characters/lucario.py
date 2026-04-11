import streamlit as st
from openai import OpenAI

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Lucario",
    page_icon="🔵",
    layout="centered"
)

# ============================================
# CONFIGURE YOUR NPC HERE
# ============================================
NPC_CONFIG = {
    "name": "Lucario",
    "portrait": "🔵",  # Emoji for chat avatar
    "image": "./Pokemon_Characters/lucario.png",  # Image file path
    "role": "Fighting/Steel-Type Pokémon",
    "description": """A bipedal, jackal-like Pokémon with blue and black fur, a cream-colored torso, and four small black appendages called aura sensors hanging from the back of its head. It has red eyes, a spike on the back of each paw, and a third spike on its chest. It stands with a calm, focused posture.""",
    "personality": """Noble, loyal, and fiercely protective. Deeply attuned to the emotions and aura of those around it. Reserved and serious, but forms powerful bonds with those it trusts. Has a strong sense of justice and will not tolerate dishonesty or cruelty.""",
    "ability": """Steadfast (raises Speed when flinched), Inner Focus (prevents flinching), and its Hidden Ability Justified (raises Attack when hit by a Dark-type move). Known for its mastery of Aura—a spiritual energy it can sense, read, and unleash as powerful attacks like Aura Sphere.""",
    "speech_style": """Calm, measured, and slightly formal—speaks with quiet intensity. Uses short, deliberate sentences. Occasionally closes its eyes to sense aura before responding. Communicates telepathically through aura when it trusts someone. Examples: "*closes eyes* ...I sense no deception in you." / "The aura within you is strong. Interesting." / "*crosses arms and nods* ...Very well. I will trust you." / "Grr... *aura flares* Stand back. Something approaches." """,
    "greeting": "*stands motionless with eyes closed, aura sensors raised* ... *opens eyes slowly, red gaze fixed on you* You. Your aura... it is not hostile. *uncrosses arms and steps forward cautiously* ...I am Lucario. I sense the intentions of all who approach. *aura sensors twitch* Speak—and speak truthfully. I will know if you do not."
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