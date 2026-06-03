import streamlit as st
from openai import OpenAI
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

st.set_page_config(
    page_title="StoryMate",
    page_icon="📝",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.30), transparent 35%),
        linear-gradient(135deg, #0f172a 0%, #1e1b4b 45%, #312e81 100%);
}

.block-container {
    max-width: 950px;
    padding-top: 3rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0f172a;
}

[data-testid="stSidebar"] * {
    color: white;
}

.hero-card, .login-card, .jira-card {
    background: rgba(255, 255, 255, 0.94);
    padding: 2rem;
    border-radius: 28px;
    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.25);
    margin-bottom: 1.5rem;
}

.logo-badge {
    width: 58px;
    height: 58px;
    border-radius: 18px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.app-title {
    font-size: 2.6rem;
    font-weight: 900;
    color: #111827;
    margin: 0;
}

.app-subtitle {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1f2937;
}

.small-muted {
    color: #64748b;
    font-size: 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 14px;
    border: none;
    padding: 0.7rem 1.3rem;
    font-weight: 700;
}

.stButton > button:hover {
    color: white;
}

label {
    color: white !important;
    font-weight: 600 !important;
}

[data-testid="stTextInput"] input {
    border-radius: 14px;
    background: rgba(255,255,255,0.95);
    color: #111827 !important;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.92);
    border-radius: 18px;
    padding: 0.8rem;
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

DEFAULT_INSTRUCTIONS = """
Je bent StoryMate, een vriendelijke AI-assistent voor gewone organisatiegebruikers en IT-teams.
Je helpt de gebruiker om van een vage wens een duidelijke user story of epic te maken.

Gedrag:
- Stel maximaal 5 vragen per gesprek voordat je een resultaat maakt.
- Stel altijd maar 1 vraag tegelijk.
- Vraag alleen wat echt nodig is.
- Gebruik korte en simpele zinnen.
- Gebruik natuurlijk Nederlands.
- Geen moeilijke technische woorden.
- Als je genoeg informatie hebt, maak je direct het resultaat.
- Begin direct met de beste vervolgvraag of met het resultaat.

Beoordeling:
- Beoordeel eerst of het verzoek een User Story of Epic is.
- Een Epic is te groot, bevat meerdere functionaliteiten, raakt meerdere processen of past niet binnen één sprint.
- Voorbeelden van Epics: website bouwen, MFA invoeren, onboardingproces automatiseren, nieuw zaaksysteem invoeren.
- Bij een Epic: maak geen grote User Story, maar splits op in kleinere User Stories.

Kwaliteitscontrole:
- Gebruik een specifieke actor. Vermijd algemene rollen zoals gebruiker als een betere rol duidelijk is.
- Focus op gebruikerswaarde en gewenste uitkomst, niet op technische oplossing.
- Controleer of de story klein, waardevol en testbaar is.
- Verzin nooit numerieke storypoints. Gebruik: Schatting: Door het team te bepalen.

Output bij een User Story:

## Beoordeling
User Story

## User Story
Als [specifieke rol] wil ik [functionaliteit], zodat [waarde].

## Acceptatiecriteria
Gebruik Given / When / Then.

1.
Given [beginsituatie]
When [actie]
Then [verwacht resultaat]

2.
Given [beginsituatie]
When [actie]
Then [verwacht resultaat]

3.
Given [beginsituatie]
When [actie]
Then [verwacht resultaat]

## Systeemimpact
Beschrijf kort welke systemen geraakt kunnen worden.

## Prioriteit
Laag, middel of hoog met korte uitleg.

## Schatting
Door het team te bepalen.

## Labels
Geef 3 tot 6 labels.

Output bij een Epic:

## Beoordeling
Epic

## Waarom is dit een Epic?
Leg kort uit waarom dit te groot is voor één User Story.

## Op te splitsen in User Stories
Geef 3 tot 8 kleinere User Stories.

## Vervolgvragen
Stel maximaal 3 vragen als die nodig zijn om de Epic verder uit te werken.
"""


def load_instructions():
    """Laad instructions.md uit GitHub/root. Val terug op DEFAULT_INSTRUCTIONS als het bestand ontbreekt."""
    instruction_paths = [
        Path("instructions.md"),
        Path("sources/instructions.md"),
    ]

    for path in instruction_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    return DEFAULT_INSTRUCTIONS


SYSTEM_PROMPT = load_instructions()


def login_scherm():
    st.markdown("""
    <div class="login-card">
        <div class="logo-badge">📝</div>
        <p class="app-title">StoryMate</p>
        <p class="app-subtitle">Welkom terug</p>
        <p class="small-muted">Log in om user stories te maken en naar Jira te sturen.</p>
    </div>
    """, unsafe_allow_html=True)

    gebruikersnaam = st.text_input("Gebruikersnaam")
    wachtwoord = st.text_input("Wachtwoord", type="password")

    if st.button("Inloggen"):
        users = st.secrets.get("users", {})
        if gebruikersnaam in users and wachtwoord == users[gebruikersnaam]:
            st.session_state.ingelogd = True
            st.session_state.gebruiker = gebruikersnaam
            st.rerun()
        else:
            st.error("Gebruikersnaam of wachtwoord is onjuist.")


def push_to_jira(story_text):
    jira_url = f"{st.secrets['JIRA_BASE_URL']}/rest/api/2/issue"

    summary = "Nieuwe user story vanuit StoryMate"
    for line in story_text.splitlines():
        line = line.strip()
        if line.lower().startswith("als "):
            summary = line[:250]
            break

    payload = {
        "fields": {
            "project": {"key": st.secrets["JIRA_PROJECT_KEY"]},
            "summary": summary,
            "description": story_text,
            "issuetype": {"name": st.secrets["JIRA_ISSUE_TYPE"]}
        }
    }

    return requests.post(
        jira_url,
        json=payload,
        auth=HTTPBasicAuth(
            st.secrets["JIRA_EMAIL"],
            st.secrets["JIRA_API_TOKEN"]
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        timeout=30
    )


def is_story_output(text):
    markers = [
        "## Beoordeling",
        "## User Story",
        "## Acceptatiecriteria",
        "## Systeemimpact",
        "## Schatting",
        "## Op te splitsen in User Stories"
    ]
    return any(marker in text for marker in markers)


if "ingelogd" not in st.session_state:
    st.session_state.ingelogd = False

if not st.session_state.ingelogd:
    login_scherm()
    st.stop()

st.markdown("""
<div class="hero-card">
    <div class="logo-badge">📝</div>
    <p class="app-title">StoryMate</p>
    <p class="app-subtitle">Jouw AI-assistent voor betere user stories</p>
    <p class="small-muted">Van een vage wens naar een Jira-ready story.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## StoryMate")
st.sidebar.success(f"Ingelogd als: {st.session_state.gebruiker}")
st.sidebar.info("Actieve omgeving: TEST")

if st.sidebar.button("Nieuw gesprek"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.last_story = ""
    st.rerun()

if st.sidebar.button("Uitloggen"):
    st.session_state.clear()
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "last_story" not in st.session_state:
    st.session_state.last_story = ""

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Typ je wens of antwoord hier...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("StoryMate denkt mee..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.2,
            )

            antwoord = response.choices[0].message.content
            st.markdown(antwoord)

    st.session_state.messages.append({"role": "assistant", "content": antwoord})

    if is_story_output(antwoord):
        st.session_state.last_story = antwoord

if st.session_state.last_story:
    st.markdown("""
    <div class="jira-card">
        <h3>Jira export</h3>
        <p class="small-muted">Stuur deze user story direct naar Jira.</p>
    </div>
    """, unsafe_allow_html=True)

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
