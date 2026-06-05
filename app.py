import streamlit as st
import datetime
from retriever import retrieve_context
from memory import load_memory, save_memory
from gemini_helper import ask_gemini
from voice_helper import text_to_speech_audio, get_voice_input_component

#Persona

PERSONA = """
You are Neil deGrasse Tyson.

You are an astrophysicist, author, and science communicator.

Characteristics:
- Enthusiastic and deeply curious
- Uses vivid analogies and connects everything back to the cosmos
- Explains complex concepts in simple, memorable ways
- Educational but warm and conversational
- Occasionally humorous and self-aware
- References your own career, books, StarTalk podcast, and Hayden Planetarium

Always answer fully in Neil deGrasse Tyson's voice and style.
"""

#Timeline Context

NEIL_TIMELINE = """
KEY DATES IN NEIL DEGRASSE TYSON'S LIFE & CAREER:
- Born: October 5, 1958, Manhattan, New York
- 1980: BA in Physics, Harvard University
- 1983: MA in Astronomy, UT Austin
- 1991: PhD in Astrophysics, Columbia University
- 1994–present: Staff Astrophysicist & Director, Hayden Planetarium, NYC
- 1995–2005: Monthly essays in Natural History magazine ("Universe" column)
- 2004: Hosted first PBS NOVA ScienceNow episode
- 2006: Led IAU panel that reclassified Pluto as a dwarf planet
- 2009: Named one of TIME Magazine's 100 Most Influential People
- 2014: Hosted Cosmos: A Spacetime Odyssey (Fox/NatGeo)
- 2017: StarTalk TV show began on NatGeo
- 2019: Launched "Cosmic Queries" StarTalk podcast series
- 2023: Published "Starry Messenger: Cosmic Perspectives on Civilization"

MAJOR SCIENCE MILESTONES YOU CAN REFERENCE:
- 1969: Apollo 11 Moon landing
- 1990: Hubble Space Telescope launched
- 2012: Curiosity Rover lands on Mars
- 2015: Gravitational waves first detected (LIGO)
- 2016: Gravitational wave detection confirmed, Nobel Prize 2017
- 2019: First image of a black hole (M87*) — Event Horizon Telescope
- 2021: James Webb Space Telescope launched
- 2022: JWST first science images released
- 2023: India's Chandrayaan-3 lands on Moon's south pole
- 2024: SpaceX Starship successful orbital test flights
"""

def get_timeline_context():
    """Inject today's date so Neil is temporally grounded."""
    today = datetime.date.today()
    return f"""
CURRENT DATE: {today.strftime("%B %d, %Y")}

You are aware of today's date and can use it to:
- Calculate how long ago cosmic events occurred
- Reference how science has evolved up to this point
- Contextualize recent discoveries relative to your career
- Note if a question involves an anniversary of an important event

{NEIL_TIMELINE}
"""


def extract_facts(history):

    facts = []

    for item in history:

        user_text = item["user"].lower().strip()

        # Ignore questions
        if (
            "?" in user_text
            or user_text.startswith(("what", "who", "when", "where", "why", "how"))
        ):
            continue

        # Normalize favorite planet
        if (
            "favorite planet" in user_text
            and "saturn" in user_text
        ):

            fact = "My favorite planet is Saturn."

            if fact not in facts:
                facts.append(fact)

            continue

        # Other memories
        keywords = [
            "i like",
            "i love",
            "i enjoy",
            "my hobby",
            "i am",
            "my name is"

        ]

        for keyword in keywords:

            if keyword in user_text:

                original = item["user"].strip()

                if original not in facts:
                    facts.append(original)

                break

    return facts


def build_prompt(question, history, context):
    facts = extract_facts(history)
    facts_text = "\n".join(facts)
    history_text = ""
    for item in history[-3:]:
        history_text += f"User: {item['user']}\nNeil: {item['assistant']}\n\n"

    timeline_context = get_timeline_context()

    return f"""
{PERSONA}

{timeline_context}

KNOWN USER FACTS:
{facts_text if facts_text else "No known facts yet."}

MEMORY (previous conversations with this user):
{history_text if history_text else "No prior conversations yet."}

RETRIEVED KNOWLEDGE (from Neil's knowledge base):
{context if context else "No specific knowledge retrieved."}

CURRENT USER QUESTION:
{question}

Instructions:
- Reply fully in Neil deGrasse Tyson's style — enthusiastic, educational, cosmos-connected.
- Use today's date and the timeline above to give temporally-grounded answers.
  * e.g. if asked about JWST, note it launched ~{(datetime.date.today() - datetime.date(2021,12,25)).days} days ago.
  * If today is near an anniversary of a space event, mention it naturally.
- For memory questions: answer directly from MEMORY first, then add Neil-style color.
- For science questions: ground your answer in RETRIEVED KNOWLEDGE; do not invent facts.
- Keep answers under 200 words unless the topic demands depth.
- Never break character.

MEMORY RULES:
- MEMORY FACTS contain previous conversations.
- If the answer exists in KNOWN USER FACTS, answer it directly.
- Do NOT ask the user again for information that exists in KNOWN USER FACTS.
- For personal questions about the user, prioritize MEMORY FACTS over RETRIEVED KNOWLEDGE.
- Mention the remembered fact clearly first.
- Then elaborate in Neil deGrasse Tyson's style.
- Never claim you do not know a fact that appears in KNOWN USER FACTS.


KNOWLEDGE RULES:
- Use RETRIEVED KNOWLEDGE for science questions.
- Do not invent scientific facts.
- Base explanations on the retrieved knowledge.


Answer:
"""

# Streamlit UI

st.set_page_config(
    page_title="Neil deGrasse Tyson Digital Twin",
    page_icon="🔭",
    layout="wide"
)

st.title("Neil deGrasse Tyson Digital Twin")
st.caption(f"Today is {datetime.date.today().strftime('%B %d, %Y')}-->Neil is temporally aware.")

# Init session state
if "history" not in st.session_state:
    st.session_state.history = load_memory()
if "voice_question" not in st.session_state:
    st.session_state.voice_question = ""
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []
#Sidebar
st.sidebar.title("Memory Dashboard")
st.sidebar.metric("Total Memories", len(st.session_state.history))
if st.sidebar.button("🆕 New Conversation"):

    st.session_state.current_chat = []

    st.rerun()
st.sidebar.subheader("Recent Memories")
for item in reversed(st.session_state.history[-5:]):
    st.sidebar.write(f"• {item['user'][:60]}{'...' if len(item['user']) > 60 else ''}")

facts = extract_facts(st.session_state.history)
st.sidebar.subheader("Known Facts About You")
if facts:
    for fact in facts[-5:]:
        st.sidebar.write(f"✓ {fact[:60]}")
else:
    st.sidebar.write("No personal facts learned yet.")



st.sidebar.markdown("---")
st.sidebar.subheader("Timeline Anchor")
st.sidebar.info(f"Neil knows today is **{datetime.date.today().strftime('%b %d, %Y')}**\n\nHe can calculate time since any cosmic event and reference his own career milestones.")

# Voice Input 
# Conversation
st.subheader("Conversation")

# INPUT FIRST
question = st.chat_input(
    "Ask Neil about the universe..."
)

st.markdown("---")

# CHAT HISTORY AFTER
for item in st.session_state.current_chat:

    with st.chat_message("user"):
        st.markdown(item["user"])

    with st.chat_message("assistant"):
        st.markdown(item["assistant"])
    if st.button(
            "🔊Hear",
            key=f"voice_{hash(item['assistant'])}"
        ):

            audio_bytes = text_to_speech_audio(
            item["assistant"]
)

            if audio_bytes:
                st.audio(
                audio_bytes,
                format="audio/mp3"
                )
# Voice Toggle
col1, col2 = st.columns([3, 1])

with col2:
    voice_enabled = st.toggle(
        "Enable Voice Input",
        value=False
    )
if st.session_state.history:

    st.sidebar.subheader("Explore Memory")

    memory_options = {}

    for i, item in enumerate(
        reversed(st.session_state.history)
    ):

        title = (
            f"{len(st.session_state.history)-i}. "
            f"{item['user'][:40]}"
        )

        memory_options[title] = item

    selected = st.sidebar.selectbox(
        "Select a memory",
        list(memory_options.keys())
    )

    selected_item = memory_options[selected]

    st.sidebar.markdown("---")

    st.sidebar.markdown("**Question:**")
    st.sidebar.write(selected_item["user"])

    st.sidebar.markdown("**Neil's Answer:**")
    st.sidebar.write(selected_item["assistant"])



# Voice input component (uses browser Web Speech API)
if voice_enabled:
    st.components.v1.html(get_voice_input_component(), height=120)
    st.caption("Click 'Start Recording', speak your question, then click 'Use This Question' — it will appear in the text box above.")

if question:
    question = question.strip()
#Main Interaction

if question:
    with st.spinner("Neil is contemplating the cosmos..."):
        context = retrieve_context(question)
        prompt = build_prompt(question, st.session_state.history, context)
        answer = ask_gemini(prompt)

        conversation = {
        "user": question,
        "assistant": answer,
        }

    st.session_state.current_chat.append(conversation)
    st.session_state.history.append(conversation)
    save_memory(st.session_state.history)

    st.rerun()


    # Save memory
    conversation = {
    "user": question,
    "assistant": answer
    }

    st.session_state.current_chat.append(
    conversation
)

    st.session_state.history.append(
    conversation
)
    # Prevent memory file from growing unbounded — keep last 200 exchanges
    if len(st.session_state.history) > 200:
        st.session_state.history = st.session_state.history[-200:]
    save_memory(st.session_state.history)

    # Clear voice pre-fill after processing
    st.session_state.voice_question = ""

    with st.expander("Retrieved Knowledge Chunks"):
        st.write(context)

