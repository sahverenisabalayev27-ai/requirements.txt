import streamlit as st
import google.generativeai as genai

# --- DAİMİ VƏ TƏHLÜKƏSİZ HƏLL ---
try:
    # Açar burada yazılmır, sistemin gizli yaddaşından (Secrets) oxunur
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Sistem xətası: API açarı 'Secrets' bölməsində tapılmadı.")

# --- SAYTIN QALAN HİSSƏSİ ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")
st.title("🇦🇿 AZ AI Süni İntellekt")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Xəta: {e}")
