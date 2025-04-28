"""Resources & Help Page
Streamlit app to provide emergency support links, resource recommendations, and an integrated EIH chatbot.
"""
import streamlit as st
import pandas as pd 
import numpy as np
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")



# page title
st.title('Resources Locator 📍')


# Ai Resource recommender
st.text("This AI-powered tool will locate any resources specific to an area!")

needs = st.multiselect(
    "Select the services you need to locate:",
    ["Meals", "Mental Health Support", "Job Assistance", "Medical Access", 
     "Family Shelter", "Pet-Friendly Housing"]
)

user_city = st.text_input("What city are you in?", placeholder="e.g., San Jose")

if st.button("🔍 Get AI-Powered Resource Suggestions"):
    if not needs:
        st.warning("Please select at least one need.")
    elif not user_city:
        st.warning("Please enter your city.")
    else:
        prompt = f"I'm in {user_city}. I need services for: {', '.join(needs)}. Recommend resources and a short explanation for each."
        with st.spinner("Finding personalized resources..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're an AI that recommends real local services for housing and social support."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success("📋 AI Suggestions:")
            st.markdown(response.choices[0].message.content.strip())

st.markdown("---")
st.text('These resources listed below are mainly tailored for the San Jose/Santa Clara County area.')

# title for san jose resources
st.subheader('Resource Locations', divider='blue')

   # for ___ housing
st.markdown('''
- **[HomeFirst Services](https://www.homefirstscc.org/)**  
  Services: Emergency shelters, transitional housing, outreach''')
   # for ___ housing
st.markdown('''
- **[Bill Wilson Center](https://www.billwilsoncenter.org/)**  
  Services: Youth & young adults, emergency shelter, family support''')
   # for ___ housing
st.markdown('''
- **[CityTeam San Jose](https://www.cityteam.org/san-jose)**  
  Services: Food, shelter, addiction recovery, and transitional housing''')

# ----------------------------------------------------------------
# for shelter locations
st.subheader('Emergency Shelters', divider= 'blue')

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.33, -121.88],
    columns=['lat', 'lon'])
st.map(df)
st.link_button("Click for more map examples", "https://docs.streamlit.io/develop/api-reference/charts/st.map")
   
# ----------------------------------------------------------------

# for local food banks and basic needs
st.subheader('Local Food Banks & Basic Needs', divider= 'blue')
st.markdown('''
- **[Second Harvest of Silicon Valley](https://www.shfb.org/)**  
  Services: Free groceries, food pantries  
- **[Sacred Heart Community Service](https://sacredheartcs.org/)**  
  Services: Clothing, food, financial assistance, case management
''')

# ----------------------------------------------------------------
#for legal aid services
st.subheader('Legal Aid', divider= 'blue')
# ----------------------------------------------------------------

# for medical care resources
st.subheader('Medical Care', divider= 'blue')
st.markdown('''
- **[Gardner Health Services](https://gardnerhealthservices.org/)**  
  Services: Primary care, behavioral health, substance use treatment  
- **[Santa Clara Valley Medical Center](https://www.scvmc.org/)**  
  Services: Emergency medical, clinics, urgent care
''')

# for crisis resources
st.subheader('Crisis Lines', divider= 'blue')

col1, col2 = st.columns(2)
with col1:
  st.subheader('Domestic Violence & Safety')
  st.markdown('''
  - **[Next Door Solutions](https://nextdoorsolutions.org/)**  
    24/7 Hotline: (408) 279-2962  
  - **[YWCA Silicon Valley](https://www.ywca-sv.org/)**  
    Services: Safe housing, advocacy, counseling
  ''')
with col2: 
  st.subheader('Mental Health Support')
  st.markdown('''
  - **[988 Suicide & Crisis Lifeline](https://www.988lifeline.org/)**  
    Call/Text: 988 (24/7, Free, Confidential)
  - **[NAMI (National Alliance on Mental Illness)](https://www.nami.org/)**  
    Helpline:  1-800-950-NAMI (6564)
  ''')


col3, col4 = st.columns(2)
with col3:
  st.subheader('Veterans Crisis Line')
  st.markdown('''
  - **[Veterans Crisis Line](https://www.veteranscrisisline.net/)**  
    Call:    Dial 988 then press 1  
    Text:    838255
  ''')
with col4: 
  st.subheader('Human Trafficking Hotline')
  st.markdown('''
  - **[Human Trafficking Hotline](https://www.humantraffickinghotline.org/)**  
    Call:    1-888-373-7888  
    Text:    “HELP” to 233733
  ''')
   


# ----------------------------------------------------------------
# for transportation support
st.subheader('Transportation Support', divider= 'blue')
st.subheader('Local (San Jose / Santa Clara County)')
st.markdown('''
- **VTA Access Paratransit**  
  A shared-ride service for people with disabilities who are unable to use VTA's fixed-route services.  
  Website: https://www.vta.org/access-paratransit (this website does't work anymore)
- **VTA Reduced Fare Clipper Card**  
  Seniors, youth, and people with low income may qualify for discounted public transportation fares.  
  Website: https://www.clippercard.com/ClipperWeb/
- **Destination: Home – Transportation Assistance**  
  Works with service providers to offer transportation vouchers and support as part of homelessness response.  
  Website: https://destinationhomesv.org/
- **Sacred Heart Community Service**  
  Offers case management and can connect individuals with transportation assistance for job interviews, medical appointments, etc.  
  Website: https://www.sacredheartcs.org/
- **LifeMoves** (for referred clients)  
  Sometimes provides limited transportation support like bus passes or shuttle services.  
  Website: https://www.lifemoves.org/
''')
st.subheader('Statewide/National')
st.markdown('''
- **United Way 211**  
  Call 2-1-1 or visit https://www.211.org for help finding transportation services near you based on ZIP code.
- **Catholic Charities of Santa Clara County**  
  Provides transportation help for seniors and low-income families as part of wraparound support.  
  Website: https://www.catholiccharitiesscc.org
- **Non-Emergency Medical Transportation (NEMT)**  
  If you’re a Medi-Cal recipient, you may be eligible for free rides to medical appointments.  
  Info: Call your Medi-Cal managed care provider.
''')
# ----------------------------------------------------------------

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