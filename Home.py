"""Main Landing Page
Streamlit app landing page for SmartHaven, offering access to all EIH-related tools and chatbot support.
"""
import streamlit as st
import pandas as pd 
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# title
st.title('SmartHaven')

# introduction
st.markdown("👋 **Welcome to SmartHaven!** We're here to support your Emergency Interim Housing (EIH) journey. Explore the tools below to get started.")

# for table of contents
st.subheader('Table of Contents', divider= 'blue')

st.page_link("pages/EIH_Budget_Overview.py", label="EIH Budget Overview", icon="💰")
st.page_link("pages/Language_&_Communication_Tools.py", label="Language & Communication Tools", icon="💬")
st.page_link("pages/Reddit_Sentiment_Analyzer.py", label="Reddit Sentiment Analyzer", icon="📊")
st.page_link("pages/Resources_Locator.py", label="Resources Locator", icon="📍")
st.page_link("pages/Stakeholder_Involvement.py", label="Stakeholder Involvement", icon="🤝")

# button to apply for emergency housing or directed to it
# Clear call-to-action: “Apply for Emergency Housing”

# general crisis hotline or emergency contacts displayed prominently
# for contact info for the shelter hotline
st.subheader('Emergency Contacts', divider= 'blue')
st.write("If you are seeking emergency hotlines, here are some contacts!")
st.markdown('''
For further assistance or inquiries: 
            
- **Here4You Shelter Hotline**: **(408) 385-2400** (Available daily from 9:00 AM to 7:00 PM)
- **Email**: [homewardbound@sanjoseca.gov](mailto:homewardbound@sanjoseca.gov)
- **Address**: 200 E. Santa Clara St., San José, CA 95113
- **TTY**: **(800) 735-2922**
''')

st.text("If you want to see more tailored resources, check out our resources page!")

# footer
st.markdown("---")
st.caption("Provided by the Sapphire Team 💎 • Powered by OpenAI & Streamlit ")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# for it to pop up on the sidebar
# st.sidebar.markdown("# Home 🏠")
# st.sidebar.markdown("---")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# chatbot on the side
st.sidebar.title("💬 AI Intake Housing Assistant")
st.sidebar.write("Need help with Emergency Interim Housing (EIH)? Ask anything.")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.session_state.chat_history = [] #older

# user input area
user_input = st.sidebar.text_input("You:", key="user_input", placeholder="e.g., Can I apply for shelter if I have a pet?")

# If user submits a message
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(("You", user_input))

    with st.spinner("Thinking..."):
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that specializes in Emergency Interim Housing (EIH) "
                        "in San Jose and Santa Clara County. Be concise, helpful, and clear."
                    ),
                }
            ]

            # Maintain full context from previous interactions
            for sender, message in st.session_state.chat_history:
                role = "user" if sender == "You" else "assistant"
                messages.append({"role": role, "content": message})

            # OpenAI chat completion
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.6,
                max_tokens=500
            )

            bot_reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append(("Bot", bot_reply))

   # try:
   #     response = openai.ChatCompletion.create(
   #         model="gpt-4",  # or "gpt-3.5-turbo"
   #         messages=st.session_state.messages,
   #     )
   #     reply = response["choices"][0]["message"]["content"]
   #     st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            bot_reply = "⚠️ Sorry, I ran into an error. Please try again."
            st.session_state.chat_history.append(("Bot", bot_reply))
            st.sidebar.error(f"API Error: {e}")

# Display full chat history in the sidebar
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.sidebar.markdown(f"🧍 **{sender}:** {message}")
    else:
        st.sidebar.markdown(f"🤖 **{sender}:** {message}")
