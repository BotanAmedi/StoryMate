import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="StoryMate",
    page_icon="📝",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

omgeving = st.sidebar.selectbox("Omgeving", ["PROD"])
st.sidebar.info(f"Actieve omgeving: {omgeving}")

if st.sidebar.button("Nieuw gesprek"):
    st.session_state.clear()
    st.rerun()

vragen = [
    "Wat wil je laten bouwen of oplossen?",
    "Voor wie is dit bedoeld?",
    "Welke meldingen, situaties of taken moeten automatisch herkend worden?",
    "Wat moet StoryMate doen als het niet zeker weet welke categorie klopt?"
]

if "stap" not in st.session_state:
    st.session_state.stap = 0

if "antwoorden" not in st.session_state:
    st.session_state.antwoorden = []

st.markdown("### Intake")

if st.session_state.stap < len(vragen):
    huidige_vraag = vragen[st.session_state.stap]
    antwoord = st.text_area(huidige_vraag, key=f"vraag_{st.session_state.stap}")

    if st.button("Volgende"):
        if not antwoord.strip():
            st.warning("Vul eerst een antwoord in.")
        else:
            st.session_state.antwoorden.append(antwoord.strip())
            st.session_state.stap += 1
            st.rerun()

else:
    st.success("Intake compleet.")

    st.markdown("### Jouw antwoorden")
    for i, antwoord in enumerate(st.session_state.antwoorden):
        st.write(f"**{vragen[i]}**")
        st.write(antwoord)

    if st.button("Genereer user story"):
        with st.spinner("StoryMate maakt je user story..."):

            prompt = f"""
Je bent StoryMate, een AI-assistent voor IT-teams.

Maak een duidelijke Jira-ready user story in het Nederlands.

Gebruik deze input:

Behoefte:
{st.session_state.antwoorden[0]}

Doelgroep:
{st.session_state.antwoorden[1]}

Wat moet herkend of verwerkt worden:
{st.session_state.antwoorden[2]}

Wat moet er gebeuren bij twijfel:
{st.session_state.antwoorden[3]}

Schrijf eenvoudig en duidelijk.

Gebruik exact dit format:

## Beoordeling
Geef aan of dit een user story of epic is.

## User Story
Als [rol] wil ik [functionaliteit], zodat [waarde].

## Acceptatiecriteria

1.
Situatie: ...
Actie: ...
Verwachting: ...

2.
Situatie: ...
Actie: ...
Verwachting: ...

3.
Situatie: ...
Actie: ...
Verwachting: ...

## Systeemimpact
Beschrijf kort welke systemen geraakt kunnen worden.

## Prioriteit
Laag, middel of hoog met korte uitleg.

## Storypoints
Geef een schatting met korte uitleg.

## Labels
Geef 3 tot 6 labels.

Regels:
- Gebruik geen Engelse termen zoals Given, When of Then.
- Gebruik natuurlijk Nederlands.
- Houd de tekst kort en bruikbaar voor Jira.
- Maak geen technische aannames die niet in de input staan.
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            resultaat = response.choices[0].message.content
            st.markdown("### Gegenereerde user story")
            st.markdown(resultaat)
