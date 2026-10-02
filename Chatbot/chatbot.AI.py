

import streamlit as st
from google import genai
import webbrowser
import os


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# API KEY
# --------------------------------------------------

# IMPORTANT:
# Set your API key as an environment variable.
# Do NOT put your real API key directly in this file.

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.info(
        "Please set your Gemini API key as an environment variable "
        "and restart Streamlit."
    )
    st.stop()


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "chat_data" not in st.session_state:
    st.session_state.chat_data = []


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🤖 My ChatBot")
st.write("Ask me anything!")


# --------------------------------------------------
# DISPLAY OLD MESSAGES
# --------------------------------------------------

for role, message in st.session_state.chat_data:

    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)

    else:
        with st.chat_message("assistant"):
            st.markdown(message)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input("How can I help you?")


if user_input:

    # Save user message
    st.session_state.chat_data.append(
        ("user", user_input)
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)


    # Convert input to lowercase
    user_input_lower = user_input.lower().strip()


    # --------------------------------------------------
    # SPECIAL COMMANDS
    # --------------------------------------------------

    if user_input_lower in [
        "hi",
        "hello",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        bot_response = (
            "Hello! 👋 I'm your AI chatbot. "
            "How can I help you today?"
        )


    elif (
        "who built you" in user_input_lower
        or "who build you" in user_input_lower
        or "who designed you" in user_input_lower
        or "who developed you" in user_input_lower
    ):

        bot_response = (
            "I am a personal AI chatbot created by a CSE Engineer. 🤖"
        )


    elif "open youtube" in user_input_lower:

        webbrowser.open("https://www.youtube.com")

        bot_response = "Sure! Opening YouTube. ▶️"


    elif "open google" in user_input_lower:

        webbrowser.open("https://www.google.com")

        bot_response = "Sure! Opening Google. 🔎"


    elif "open spotify" in user_input_lower:

        webbrowser.open("https://www.spotify.com")

        bot_response = "Sure! Opening Spotify. 🎵"


    # --------------------------------------------------
    # GEMINI RESPONSE
    # --------------------------------------------------

    else:

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input
            )

            bot_response = response.text

            if not bot_response:
                bot_response = (
                    "Sorry, I couldn't generate a response."
                )

        except Exception as e:

            bot_response = (
                "Sorry, something went wrong while "
                "connecting to Gemini.\n\n"
                f"Error: `{e}`"
            )


    # --------------------------------------------------
    # SAVE BOT RESPONSE
    # --------------------------------------------------

    st.session_state.chat_data.append(
        ("assistant", bot_response)
    )


    # --------------------------------------------------
    # DISPLAY BOT RESPONSE
    # --------------------------------------------------

    with st.chat_message("assistant"):
        st.markdown(bot_response)