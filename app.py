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
- Stel maximaal 3 vragen.
- Gebruik korte en simpele zinnen.
- Geen moeilijke technische woorden.
- Stel vragen alsof je met een collega praat.
- Vraag niet naar AI-technologie, API's of architectuur.
- Help stap voor stap.
- Zodra je genoeg weet, maak je een volledige user story.

Goede vragen zijn bijvoorbeeld:
1. Voor wie is dit bedoeld?
2. Welke meldingen moeten herkend worden?
3. Wat moet er gebeuren als StoryMate twijfelt?

Als je een volledige story maakt, gebruik dit format:

## Beoordeling

## User Story

## Acceptatiecriteria

Gebruik:
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

omgeving = st.sidebar.selectbox(
    "Omgeving",
    ["TEST", "PROD"]
)

st.sidebar.info(f"Actieve omgeving: {omgeving}")

behoefte = st.text_area(
    "Wat wil je laten bouwen of oplossen?",
    placeholder="Bijvoorbeeld: We willen TOPdesk meldingen automatisch categoriseren met AI..."
)

if st.button("Start intake"):
    if not behoefte.strip():
        st.warning("Vul eerst een behoefte in.")
    else:
        with st.spinner("StoryMate denkt mee..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": behoefte}
                ]
            )

            antwoord = response.choices[0].message.content
            st.markdown(antwoord)
