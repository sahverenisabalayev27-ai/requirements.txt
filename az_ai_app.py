import streamlit as st
import google.generativeai as genai

# --- 1. KONFİQURASİYA ---
API_KEY = "AIzaSyDlnTN0DESssF08610WmfcO0BQo1LonASg"
genai.configure(api_key=API_KEY)

# Ağıllı Model Seçimi: Hansı model aktivdirsə onu tapır
@st.cache_resource
def get_active_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return "gemini-1.5-flash" # Tapılmasa standart olaraq bu
    except:
        return "gemini-1.5-flash"

selected_model_name = get_active_model()
model = genai.GenerativeModel(selected_model_name)

# --- 2. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")
st.title("🇦🇿 AZ AI Süni İntellekt")
st.caption(f"Sistem aktivdir | Model: {selected_model_name}")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. SUAL-CAVAB ---
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Dünənki uğurlu metodla cavab alırıq
            response = model.generate_content(prompt)
            ai_message = response.text
            st.markdown(ai_message)
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
        except Exception as e:
            st.error(f"Xəta: {e}")
