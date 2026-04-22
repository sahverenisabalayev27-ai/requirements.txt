import streamlit as st
import google.generativeai as genai

# --- 1. KONFİQURASİYA (Sənin yeni açarın yerləşdirildi) ---
API_KEY = "AIzaSyDlnTN0DESssF08610WmfcO0BQo1LonASg"
genai.configure(api_key=API_KEY)

# Modeli sazlayırıq
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model yüklənmədi: {e}")

# --- 2. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")
st.title("🇦🇿 AZ AI Süni İntellekt")
st.caption("Sahveren tərəfindən hazırlandı")
st.markdown("---")

# Söhbət tarixçəsi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. SUAL-CAVAB ---
if prompt := st.chat_input("Sualınızı bura yazın..."):
    # İstifadəçi sualı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Cavabı
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            ai_message = response.text
            st.markdown(ai_message)
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}")
