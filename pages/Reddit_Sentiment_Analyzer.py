"""Reddit Sentiment Analyzer
Streamlit app for analyzing the sentiment of recent Reddit posts by subreddit or keyword, including a sidebar chatbot for EIH support.
"""
import os

import openai
import streamlit as st
import praw
from openai import OpenAI

import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static


# Static locations for more reliable heatmap pins


# Convert sentiment string into numeric score

SAN_JOSE_SPOTS = {
    "Diridon Station": (37.3295, -121.9026),
    "Kelley Park": (37.3208, -121.8469),
    "Guadalupe River": (37.3425, -121.9010),
    "Downtown San Jose": (37.3336, -121.8896),
    "Reid-Hillview Airport": (37.3329, -121.8197),
    "East San Jose": (37.3534, -121.8298),
    "Roosevelt Park": (37.3476, -121.8676),
    "San Jose Airport": (37.3639, -121.9289)
}


def match_known_location(text):
    for place in SAN_JOSE_SPOTS:
        if place.lower() in text.lower():
            return place
    return None


def sentiment_score(text):
    text = text.lower()
    if "positive" in text:
        return 1.0
    elif "negative" in text:
        return -1.0
    elif "mixed" in text or "concern" in text or "inquisitive" in text or "neutral" in text:
        return 0.5
    else:
        return 0.2  # treat as soft signal

# Simplified place extraction function
def extract_place(text):
    text = text.lower()
    for place in SAN_JOSE_SPOTS:
        if place.lower() in text:
            return place
    return None

# Main map function
def geo_sentiment_map(posts, default_location=(37.3382, -121.8863)):
    m = folium.Map(location=default_location, zoom_start=13)
    heat_data = []

    for post in posts:
        place = post.get("place")
        sentiment = post.get("sentiment", "neutral")
        coords = SAN_JOSE_SPOTS.get(place)

        if not coords:
            continue

        score = sentiment_score(sentiment)
        abs_score = abs(score)

        # 🔥 Add to heatmap
        if score != 0:
            heat_data.append([coords[0], coords[1], abs_score])

        # 📍 Add sentiment marker (color-coded)
        if score > 0.5:
            color = "green"
        elif score < 0:
            color = "red"
        else:
            color = "blue"

        folium.Marker(
            location=coords,
            popup=f"{place} → {score}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    # 💡 Show heat layer
    if heat_data:
        from folium.plugins import HeatMap
        HeatMap(
            heat_data,
            radius=15,
            blur=25,
            min_opacity=0.4
        ).add_to(m)

    # 🧪 Show map
    folium_static(m)




client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Initialize Reddit client
reddit = praw.Reddit(

    client_id=st.secrets["REDDIT_CLIENT_ID"],
    client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
    user_agent="reddit_sentiment_app"
)

st.title("📊 Reddit Sentiment Analyzer")
st.markdown("Analyze sentiment of recent Reddit posts from a specific subreddit or keyword.")



# Making a selection menu instead of text input
subreddit_name = st.selectbox(
    "Choose a subreddit:",
    options=["SanJose", "santaclara", "Sunnyvale", "sanfrancisco",
             "oakland", 'Fremont', 'SFhomeless', 'hayward'],
    index=0
)

search_term = st.selectbox(
    "Choose a keyword (optional):",
    options=["encampment", "tent", "shelter", "housing", "crime", "safety",
             "jobs", "mental health", "community", "sweeps",
             "displacement", 'eviction', "homelessness"],
    index=0
)

limit = st.slider("Number of posts to analyze", min_value=1, max_value=100, value=10, step=1)

if st.button("Analyze"):
    with st.spinner("Fetching Reddit posts..."):
        try:
            posts = []
            if search_term:
                submissions = reddit.subreddit(subreddit_name).search(search_term, limit=limit)
            else:
                submissions = reddit.subreddit(subreddit_name).hot(limit=limit)

            for post in submissions:
                posts.append({"title": post.title, "selftext": post.selftext})

        except Exception as e:
            st.error(f"Failed to fetch posts: {e}")
            posts = []

    if posts:
        st.success("Fetched posts. Analyzing sentiment...")
        filtered_posts = []

        for post in posts:
            content = f"{post['title']} {post['selftext']}"
            place = match_known_location(content)
            if not place:
                continue  # Skip post if it doesn't mention a known location
            post["matched_place"] = place
            filtered_posts.append(post)

        for idx, post in enumerate(filtered_posts, start=1):
            content = f"{post['title']} {post['selftext']}".strip()
            if not content:
                continue

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful sentiment analysis tool."},
                        {"role": "user", "content": f"Analyze the sentiment of this Reddit post: {content}"}
                    ]
                )
                sentiment = response.choices[0].message.content
                post["sentiment"] = sentiment
                post["subreddit"] = subreddit_name
                post["place"] = post["matched_place"]

                st.markdown(f"**Post {idx}:** {post['title']}")
                st.markdown(f"**Sentiment:** {sentiment}")
                st.divider()

            except Exception as e:
                st.warning(f"OpenAI error for post {idx}: {e}")
                continue

    st.subheader("📍 Sentiment by Location")
    geo_sentiment_map(posts)

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