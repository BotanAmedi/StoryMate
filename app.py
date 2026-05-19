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

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.30), transparent 35%),
        linear-gradient(135deg, #0f172a 0%, #1e1b4b 45%, #312e81 100%);
    color: #0f172a;
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
    border: 1px solid rgba(255,255,255,0.5);
}

.logo-row {
    display: flex;
    align-items: center;
    gap: 1rem;
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
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.35);
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
    margin-top: 1.2rem;
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
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
}

.stButton > button:hover {
    color: white;
    transform: translateY(-1px);
}

[data-testid="stTextInput"] input {
    border-radius: 14px;
    border: 1px solid #dbeafe;
    background: #f8fafc;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.92);
    border-radius: 18px;
    padding: 0.8rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

h1, h2, h3 {
    color: #111827;
}

hr {
    border-color: rgba(255,255,255,0.25);
}
</style>
""", unsafe_allow_html=True)

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

def render_logo(subtitle="Jouw AI-assistent voor betere user stories", text="Van een vage wens naar een duidelijke user story die je direct naar Jira kunt sturen."):
    st.markdown(f"""
    <div class="hero-card">
        <div class="logo-row">
            <div class="logo-badge">📝</div>
            <div>
                <p class="app-title">StoryMate</p>
            </div>
        </div>
        <p class="app-subtitle">{subtitle}</p>
        <p class="small-muted">{text}</p>
    </div>
    """, unsafe_allow_html=True)

def login_scherm():
    st.markdown("""
    <div class="login-card">
        <div class="logo-row">
            <div class="logo-badge">📝</div>
            <div>
                <p class="app-title">StoryMate</p>
            </div>
        </div>
        <p class="app-subtitle">Welkom terug</p>
        <p class="small-muted">Log in om user stories te maken en direct naar Jira te sturen.</p>
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
        if line.lower().startswith("als "):
            summary = line[:250]
            break

    payload = {
        "fields": {
            "project": {
                "key": st.secrets["JIRA_PROJECT_KEY"]
            },
            "summary": summary,
            "description": story_text,
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

if "ingelogd" not in st.session_state:
    st.session_state.ingelogd = False

if not st.session_state.ingelogd:
    login_scherm()
    st.stop()

render_logo()

st.sidebar.markdown("## StoryMate")
st.sidebar.success(f"Ingelogd als: {st.session_state.gebruiker}")

omgeving = st.sidebar.selectbox("Omgeving", ["TEST"])
st.sidebar.info(f"Actieve omgeving: {omgeving}")

if st.sidebar.button("Nieuw gesprek"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.session_state.last_story = ""
    st.rerun()

if st.sidebar.button("Uitloggen"):
    st.session_state.clear()
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
    st.markdown("""
    <div class="jira-card">
        <h3>Jira export</h3>
        <p class="small-muted">Zet deze user story direct door naar je Jira backlog.</p>
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
