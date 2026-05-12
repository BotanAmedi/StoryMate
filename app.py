import streamlit as st

st.set_page_config(
    page_title="StoryMate",
    page_icon="📝",
    layout="centered"
)

st.title("📝 StoryMate")
st.subheader("Jouw AI-assistent voor betere user stories")

st.write(
    "Van een vage behoefte naar een duidelijke user story met acceptatiecriteria."
)

omgeving = st.sidebar.selectbox(
    "Omgeving",
    ["TEST", "PROD"]
)

st.sidebar.info(f"Actieve omgeving: {omgeving}")

behoefte = st.text_area(
    "Wat wil je laten bouwen of oplossen?",
    placeholder="Bijvoorbeeld: We willen maandrapportages automatisch kunnen exporteren..."
)

if st.button("Start intake"):
    if not behoefte:
        st.warning("Vul eerst een behoefte in.")
    else:
        st.success("Intake gestart")

        st.markdown("### Vervolgvragen")
        st.write("1. Voor welke gebruikersgroep is dit bedoeld?")
        st.write("2. Welk probleem lost dit op?")
        st.write("3. Welke systemen zijn hierbij betrokken?")
        st.write("4. Wanneer is dit succesvol?")

        st.markdown("### Concept user story")
        st.info(
            f"Als gebruiker wil ik {behoefte.lower()}, zodat dit proces duidelijker, sneller of beter wordt."
        )
