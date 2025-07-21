import streamlit as st
import requests
import base64

# --- Convert local image to base64 for background ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{b64_data}"

custom_bg = get_base64_image(r"C:\Users\VivoBook\Program\Agentic-Chatbot-GS\doll-looking-two-buttons.jpg")


# Set up the page
st.set_page_config(page_title="Agentic GSBot", layout="centered", page_icon="🤖")

# Theme toggle
theme = st.radio("🎨 Select Theme:", ["Light", "Dark"], horizontal=True)

# Define theme-specific colors
if theme == "Dark":
    overlay_color = "rgba(10, 10, 10, 0.85)"
    text_color = "#EAF6FF"
    input_text_color = "#EAF6FF"
    bubble_bg = "#1f1f1f"
    bubble_text = "#F8F9FA"
    button_bg = "#333333"
    button_hover = "#555555"
    input_bg = "#2c2c2c"
    input_border = "#999"
else:
    overlay_color = "rgba(255, 255, 255, 0.88)"
    text_color = "#000000"
    input_text_color = "#000000"
    bubble_bg = "#f1f1f1"
    bubble_text = "#000000"
    button_bg = "#4B8BBE"
    button_hover = "#6BA3D6"
    input_bg = "white"
    input_border = "#ccc"

# Inject custom CSS
st.markdown(f"""
    <style>
        html, body, [class*="stApp"] {{
            background-image: url('{custom_bg}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: {text_color};
        }}
        .block-container {{
            background-color: {overlay_color};
            padding: 2rem;
            border-radius: 12px;
        }}
        textarea, input, select {{
            color: {input_text_color} !important;
            background-color: {input_bg} !important;
            border: 1px solid {input_border} !important;
            padding: 0.5rem;
            border-radius: 6px;
        }}
        textarea::placeholder, input::placeholder {{
            color: #aaa !important;
        }}
        textarea:focus, input:focus {{
            border-color: #4B8BBE !important;
            outline: none !important;
            box-shadow: 0 0 4px #4B8BBE55;
        }}
        .chat-bubble {{
            background: {bubble_bg};
            color: {bubble_text};
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-size: 16px;
            line-height: 1.5;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.25);
        }}
        label, h1, h3, .markdown-text-container p {{
            color: {text_color} !important;
        }}
        button[kind="primary"] {{
            background-color: {button_bg} !important;
            color: white !important;
            border: 1px solid #888 !important;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            transition: background-color 0.3s ease;
        }}
        button[kind="primary"]:hover {{
            background-color: {button_hover} !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
        }}
    </style>
""", unsafe_allow_html=True)

# UI Header
st.markdown(f"""
    <div style="text-align: center;">
        <h1 style="color:#4B8BBE;">🤖 Agentic GSBot</h1>
        <p style="font-size:18px;">Create and Interact with AI Agents of GS</p>
    </div>
    <hr style='border: 1px solid #bbb;'>
""", unsafe_allow_html=True)

# AI Agent Definition
st.markdown("### 🧠 Define Your AI Agent")
system_prompt = st.text_area("System Prompt", height=70, placeholder="Type your system prompt here...")

# Model Configuration
st.markdown("### ⚙️ Model Configuration")
provider = st.radio("Select Provider:", ("Groq", "OpenAI"), horizontal=True)

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

selected_model = st.selectbox(
    "Select Model:", 
    MODEL_NAMES_GROQ if provider == "Groq" else MODEL_NAMES_OPENAI
)

# Web Search Option
st.markdown("### 🌐 Web Search")
allow_web_search = st.checkbox("Allow Web Search")

# User Query
st.markdown("### 💬 Enter Your Query")
user_query = st.text_area("Ask Anything...", height=150)
API_URL = "https://56082140288f.ngrok-free.app/chat"
# Replace with your ngrok forwarding URL


# Ask Agent Button
if st.button("🚀 Ask Agent!"):
    if user_query.strip():
        with st.spinner("🧠 Thinking..."):
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(f"⚠️ {response_data['error']}")
                    else:
                        final_response = response_data.get("response", str(response_data))
                        st.markdown("### ✅ Agent Response")
                        st.markdown(f"<div class='chat-bubble'>{final_response}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: {e}")
    else:
        st.warning("⚠️ Please enter a query before submitting.")
