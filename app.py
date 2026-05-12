import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="StoryMate", page_icon="📝", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

behoefte = st.text_area(
    "Wat wil je laten bouwen of oplossen?",
    placeholder="Bijvoorbeeld: We willen maandrapportages automatisch kunnen exporteren..."
)

if st.button("Genereer user story"):
    if not behoefte.strip():
        st.warning("Vul eerst een behoefte in.")
    else:
        with st.spinner("StoryMate denkt mee..."):
            prompt = f"""
Je bent StoryMate, een AI-assistent voor IT-teams.

Maak van onderstaande behoefte een Jira-ready user story in het Nederlands.

Behoefte:
{behoefte}

Geef output in dit format:

## User Story
Als [rol] wil ik [functionaliteit], zodat [waarde].

## Acceptatiecriteria
1.
2.
3.
4.
5.

## Systeemimpact
Beschrijf welke systemen mogelijk geraakt worden.

## Prioriteit
Low / Medium / High met korte uitleg.

## Storypoints
Schatting met korte uitleg.

## Labels
Geef 3 tot 6 labels.
"""

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            st.markdown(response.output_text)
