import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="StoryMate", page_icon="🤖", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 StoryMate")
st.subheader("Jouw AI backlog assistent")

SYSTEM_PROMPT = """
Je bent StoryMate, een AI-assistent voor IT-teams.

Regels:
- Stel maximaal 3 slimme vervolgvragen als informatie ontbreekt.
- Vraag alleen wat echt nodig is.
- Als voldoende informatie bekend is, genereer een Jira-ready user story.
- Gebruik Nederlands.
- Als dit eigenlijk een epic is, benoem dit expliciet.
- Gebruik correcte Gherkin syntax.

Acceptatiecriteria regels:
- Gebruik exact dit format:
  Given ...
  When ...
  Then ...
- Engels voor Given/When/Then.
- Nederlandse inhoud.
- Eén scenario per acceptatiecriterium.
- Geen doorlopende paragrafen.

Output bij volledige story:

## Beoordeling

## User Story

## Acceptatiecriteria

## Vervolgvragen

## Systeemimpact

## Prioriteit

## Storypoints

## Labels
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Beschrijf je behoefte...")

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

            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
