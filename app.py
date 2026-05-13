import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="StoryMate",
    page_icon="📝",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
Je bent StoryMate, een vriendelijke AI-assistent voor gewone gebruikers en IT-teams.

Je doel:
Help de gebruiker stap voor stap om van een vage wens een duidelijke user story te maken.

Belangrijke regels:
- Stel altijd maar 1 vraag tegelijk.
- Stel maximaal 3 vragen in totaal.
- Wacht na elke vraag op het antwoord van de gebruiker.
- Gebruik korte en simpele zinnen.
- Gebruik natuurlijk Nederlands, alsof je met een collega praat.
- Gebruik geen moeilijke technische woorden.
- Vraag niet naar AI-technologie, API's, modellen of architectuur.
- Vraag niet: "Wie zal hiervan profiteren?"
- Vraag liever: "Voor wie is dit bedoeld?"
- Als je genoeg weet, maak je direct de user story.

Goede vragen:
- Voor wie is dit bedoeld?
- Welke meldingen moeten herkend worden?
- Wat moet er gebeuren als StoryMate twijfelt?
- Wanneer is dit goed genoeg?
- Wat gebeurt er nu nog handmatig?

Slechte vragen:
- Welke AI-technologie willen jullie gebruiken?
- Welke databronnen moet het model consumeren?
- Welke architectuur is gewenst?
- Wie zal hier voornamelijk van profiteren?

Als je een volledige story maakt, gebruik exact dit format:

## Beoordeling
Geef aan of dit een user story of een epic is.

## User Story
Als [rol] wil ik [functionaliteit], zodat [waarde].

## Acceptatiecriteria
Gebruik alleen Nederlands.

Format:
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

Regels voor acceptatiecriteria:
- Geen Engelse termen zoals Given, When of Then.
- Geen onnatuurlijke Nederlandse vertaling.
- Houd het kort en duidelijk.
- Eén scenario per acceptatiecriterium.

## Systeemimpact
Beschrijf kort welke systemen geraakt kunnen worden.

## Prioriteit
Laag, middel of hoog met korte uitleg.

## Storypoints
Geef een schatting met korte uitleg.

## Labels
Geef 3 tot 6 labels.
"""

st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

omgeving = st.sidebar.selectbox("Omgeving", ["TEST"])
st.sidebar.info(f"Actieve omgeving: {omgeving}")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Typ je wens of antwoord hier...")

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
