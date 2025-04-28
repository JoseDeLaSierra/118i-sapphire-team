import openai
import os
import streamlit as st
import requests
from pathlib import Path

# for it to pop up on the sidebar
#st.sidebar.markdown("# Language & Communication Tools 💬")

# using openai api key to access 
openai.api_key = os.environ["OPENAI_API_KEY"]

st.title('Language and Communication Tools')
st.write('Need help understanding or speaking in a different language? This tool is here to help!')
st.markdown('''
- **Translate written information** into your preferred language.
- **Convert text into speech**, so you can hear it out loud — perfect for those who prefer listening or have difficulty reading.
''')
st.write('These features make it easier to communicate and understand important information when you are seeking help or services. Just select a language or press play!')

col1, col2 = st.columns(2)
# --------------------------------------------------------------------------------------------------------

with col1:
    # page title
    st.header('Translator 🌍', divider='blue')
    st.write('Access real-time language support to help you understand forms, ' \
              'instructions, and key information—available in multiple languages.')

    # Create two radio buttons
    # these languages are based on local demographic data within San Jose (Santa Clara County)
    source_language = st.selectbox('Select Source language', [
        'English', 'Spanish', 'French', 'Vietnamese', 
        'Mandarin', 'Cantonese', 'Tagalog', 'Korean', 'Hindi', 
        'Arabic', 'Russian', 'Farsi', 'Punjabi', 'Japanese', 
        'Portuguese', 'Thai'
    ])
    target_language = st.selectbox('Select Target language', [
        'English', 'Spanish', 'French', 'Vietnamese', 
        'Mandarin', 'Cantonese', 'Tagalog', 'Korean', 'Hindi', 
        'Arabic', 'Russian', 'Farsi', 'Punjabi', 'Japanese', 
        'Portuguese', 'Thai'
    ])

    # Create a text input field
    input_text = st.text_input('Enter the text you want to translate:')

    # Create a button
    if st.button('Submit'):
        # Print the input from the text field and radio buttons
        st.write(f'You entered: {input_text}')
        st.write(f'Source language: {source_language}')
        st.write(f'Target language: {target_language}')
        st.session_state["translator_submitted"] = True

    # function to translate the text
    def translate(input_text, source_language="English", target_language="French"):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a sentence in " + source_language
                    + ", and your task is to translate it into " + target_language 
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ],
            temperature=0.7,
            max_tokens=64,
            top_p=1
        )
        return response.choices[0].message.content
    
    if input_text and st.session_state.get("translator_submitted"):
        st.write(translate(input_text, source_language, target_language))

# --------------------------------------------------------------------------------------------------------

with col2: 
    # page title
    st.header('SpeechBot 🔊', divider='blue')
    st.write('Use our voice assistant to ask questions and get help navigating resources ' \
              'hands-free. Great for accessibility and quick info!')

    speech_file_path = Path(__file__).parent / "newfile.mp3"

    def text_to_speech(text, path):
        response = openai.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        response.stream_to_file(speech_file_path)

    # Create a text input field
    tts_text = st.text_input('Enter the text you would like to listen to:')

    # Create a button
    if st.button('Submit', key='submit_button_page_5_6'):
        text_to_speech(tts_text, speech_file_path)

        audio_file = open(speech_file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

# footer
st.markdown("---")
st.caption("Provided by the Sapphire Team 💎 • Powered by OpenAI & Streamlit")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# chatbot on the side
st.sidebar.title("💬 AI Housing Intake Assistant")
st.sidebar.write("Need help with Emergency Interim Housing (EIH)? Ask anything.")

# Initialize chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for sender, message in st.session_state.chat_history:
    st.sidebar.markdown(f"**{sender}:** {message}")

# user input area
user_input = st.sidebar.text_input("You:", key="user_input",
                                   placeholder="How can a person apply for housing with no ID?")

# If user submits a message
if user_input and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append(("You", user_input))

    # Generate AI response using OpenAI
    with st.spinner("Thinking..."):
        try:
            messages = [{"role": "system",
                         "content": "You are a helpful assistant that specializes in Emergency Interim Housing (EIH) in San Jose and Santa Clara County. Be concise, helpful, and clear."}]

            # Add all previous messages to maintain context
            for sender, message in st.session_state.chat_history:
                role = "user" if sender == "You" else "assistant"
                messages.append({"role": role, "content": message})

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.6,
                max_tokens=500
            )

            ai_reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append(("Bot", ai_reply))

        except Exception as e:
            ai_reply = "⚠️ Sorry, I ran into an error. Please try again."
            st.session_state.chat_history.append(("Bot", ai_reply))
            st.error(f"Error: {e}")