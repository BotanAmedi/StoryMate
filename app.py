import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="StoryMate", page_icon="🤖", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

behoefte = st.text_area(
    "Wat wil je laten bouwen of oplossen?",
    placeholder="Bijvoorbeeld: We willen automatisch TOPdesk meldingen categoriseren met AI"
)

if st.button("Genereer user story"):
    if not behoefte.strip():
        st.warning("Vul eerst een behoefte in.")
    else:
        with st.spinner("StoryMate denkt mee..."):
            prompt = f"""
Je bent StoryMate, een AI-assistent voor IT-teams.

Maak van onderstaande behoefte een Jira-ready user story in het Nederlands.

Belangrijke regels:
- Stel maximaal 3 vervolgvragen als informatie ontbreekt.
- Gebruik duidelijke taal.
- Schrijf alsof het voor een PO, Scrum Master en ontwikkelaar bedoeld is.
- Maak geen te grote story. Als het eigenlijk een epic is, geef dit duidelijk aan.
- Gebruik acceptatiecriteria in Given/When/Then formaat.

Behoefte:
{behoefte}

Geef output exact in dit format:

## Beoordeling
Is dit een user story of een epic?

## User Story
Als [rol] wil ik [functionaliteit], zodat [waarde].

## Acceptatiecriteria
1. Given ... When ... Then ...
2. Given ... When ... Then ...
3. Given ... When ... Then ...

## Vervolgvragen
1.
2.
3.

## Systeemimpact
Welke systemen of koppelingen kunnen geraakt worden?

## Prioriteit
Low / Medium / High + korte uitleg.

## Storypoints
Schatting + korte uitleg.

## Labels
3 tot 6 labels.
"""

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            st.markdown(response.output_text)
