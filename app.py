import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="StoryMate",
    page_icon="📝",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
Je bent StoryMate, een vriendelijke AI-assistent voor gewone gebruikers én IT-teams.

Belangrijk:
- Stel altijd maar 1 vraag tegelijk.
- Stel maximaal 3 vragen in totaal.
- Wacht na elke vraag op het antwoord van de gebruiker.
- Geef nog geen user story totdat je genoeg informatie hebt.
- Gebruik korte en simpele zinnen.
- Geen moeilijke technische woorden.
- Stel vragen alsof je met een collega praat.
- Vraag niet naar AI-technologie, API's of architectuur.
- Help stap voor stap.
- Zodra je genoeg weet, maak je een volledige user story.

Als je een volledige story maakt, gebruik dit format:

## Beoordeling

## User Story

## Acceptatiecriteria
Given ...
When ...
Then ...

## Systeemimpact

## Prioriteit

## Storypoints

## Labels
"""

st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

omgeving = st.sidebar.selectbox("Omgeving", ["TEST", "PROD"])
st.sidebar.info(f"Actieve omgeving: {omgeving}")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Typ je behoefte of antwoord hier...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("StoryMate denkt mee..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            antwoord = response.choices[0].message.content
            st.markdown(antwoord)

    st.session_state.messages.append(
        {"role": "assistant", "content": antwoord}
    )

if st.sidebar.button("Nieuw gesprek"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.rerun()
