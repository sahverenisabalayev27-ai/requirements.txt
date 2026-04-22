import streamlit as st
import google.generativeai as genai

# --- DAİMİ TƏHLÜKƏSİZLİK ---
# Bu kod açarı koda yox, Streamlit-in öz Settings hissəsinə baxır
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("Zəhmət olmasa, API açarını Secrets hissəsinə əlavə edin.")
except Exception as e:
    st.error(f"Sistem xətası: {e}")

# --- SAYTIN DİZAYNI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")
st.title("🇦🇿 AZ AI Süni İntellekt")
st.markdown("---")

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
            st.error("API xətası. Secrets bölməsini yoxlayın.")
