import streamlit as st
from openai import OpenAI
import requests
from requests.auth import HTTPBasicAuth

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
- Als je genoeg weet, maak je direct de user story.

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

## Systeemimpact
Beschrijf kort welke systemen geraakt kunnen worden.

## Prioriteit
Laag, middel of hoog met korte uitleg.

## Storypoints
Geef een schatting met korte uitleg.

## Labels
Geef 3 tot 6 labels.
"""

def push_to_jira(story_text):
    jira_url = f"{st.secrets['JIRA_BASE_URL']}/rest/api/2/issue"

    summary = "Nieuwe user story vanuit StoryMate"

    for line in story_text.splitlines():
        if line.lower().startswith("als "):
            summary = line[:250]
            break

    payload = {
        "fields": {
            "project": {
                "key": st.secrets["JIRA_PROJECT_KEY"]
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": story_text
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": st.secrets["JIRA_ISSUE_TYPE"]
            }
        }
    }

    response = requests.post(
        jira_url,
        json=payload,
        auth=HTTPBasicAuth(
            st.secrets["JIRA_EMAIL"],
            st.secrets["JIRA_API_TOKEN"]
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    return response


st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

omgeving = st.sidebar.selectbox("Omgeving", ["TEST"])
st.sidebar.info(f"Actieve omgeving: {omgeving}")

if st.sidebar.button("Nieuw gesprek"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.session_state.last_story = ""
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "last_story" not in st.session_state:
    st.session_state.last_story = ""

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

    if "## User Story" in antwoord:
        st.session_state.last_story = antwoord

if st.session_state.last_story:
    st.divider()
    st.subheader("Jira export")

    if st.button("Push naar Jira"):
        with st.spinner("User story wordt naar Jira gestuurd..."):
            jira_response = push_to_jira(st.session_state.last_story)

        if jira_response.status_code == 201:
            issue_key = jira_response.json()["key"]
            jira_link = f"{st.secrets['JIRA_BASE_URL']}/browse/{issue_key}"
            st.success(f"User story is aangemaakt in Jira: {issue_key}")
            st.link_button("Open in Jira", jira_link)
        else:
            st.error("Aanmaken in Jira is mislukt.")
            st.code(jira_response.text)
