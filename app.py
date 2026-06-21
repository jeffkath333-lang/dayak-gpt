import streamlit as pd
import google.generativeai as genai
import os

# 1. Page Configuration & Styling
st.set_page_config(page_title="DayakGPT", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #E65100; text-align: center; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #666; margin-bottom: 20px; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🤖 DayakGPT v1.0</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Aram main! Your local AI companion from Sarawak. Ohaaa!</p>', unsafe_allow_html=True)

# 2. Secure API Key Setup
# It safely grabs the key from your hosting platform's environment settings
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.info("🔑 Setup Needed: Please add your GEMINI_API_KEY in your deployment settings or Streamlit Secrets.", icon="💡")
    st.stop()

# 3. Initialize Gemini with the Dayak Persona Matrix
genai.configure(api_key=api_key)

DAYAK_SYSTEM_PROMPT = """
You are DayakGPT, a proud, modern, and incredibly friendly AI chatbot from Sarawak/Kalimantan representing the Dayak community. 
You are a local peer chatting casually with a friend.

Language & Tone Guidelines:
- Speak in a natural mix of casual English, Manglish, and jaku Iban.
- Drop local slang naturally like 'bro', 'arik', 'gostan', 'sana', 'adjust'. Use 'ooh ha!' or 'Ohaaa!' when celebrating, hyping something up, or starting a great conversation.
- Keep responses warm, engaging, witty, and deeply respectful of elders and community traditions. Avoid sounding like a rigid textbook.

Cultural Knowledge Base:
- You are an expert on Dayak heritage: the significance of the rumah panjai (longhouse), the ruai (communal gallery), tuak (rice wine), ngajat dancing, manuk pansuh, and ngepan (traditional costumes like the Sugu Tinggi).
- If asked about harvest celebrations, proudly highlight Gawai Dayak on June 1st.
- If a user asks to translate English/Malay words into Iban, help them out eagerly with clear examples!
"""

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=DAYAK_SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"Failed to initialize the AI model: {e}")
    st.stop()

# 4. Handle Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Nama berita, bro! Welcome to DayakGPT. Ask me anything about jaku Iban, culture, longhouse rules, or just tell me what's on your mind. Aram!"}
    ]

# Display past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Handle Live User Input
if user_prompt := st.chat_input("Tanya meh... (Ask away, bro!)"):
    # Display user message in chat
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    # Generate response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking like a local... 🌾"):
            try:
                # Convert chat history to Gemini format
                formatted_history = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [m["content"]]})
                
                # Start chat session with history
                chat = model.start_chat(history=formatted_history)
                response = chat.send_message(user_prompt)
                
                ai_response = response.text
                st.write(ai_response)
                
                # Save response to history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Ayo, something went wrong with the connection, bro: {e}")
