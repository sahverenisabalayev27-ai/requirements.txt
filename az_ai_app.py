import streamlit as st
import google.generativeai as genai

# --- 1. BOTUN BEYNİ VƏ API AYARI ---
def start_bot():
    # Sənin verdiyin yeni API açarı
    API_KEY = "AIzaSyC44lz2MFk9cM5cq_Ma41OCcWCxIk0fL8k"
    
    try:
        genai.configure(api_key=API_KEY)
        
        # Ən yaxşı modeli tapırıq
        model_name = 'gemini-1.5-flash'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                break
        
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")
        return None

# --- 2. SAYTIN GÖRÜNÜŞÜ (DİZAYN) ---
st.set_page_config(page_title="AZ AI - Sahveren", page_icon="🇦🇿")

st.title("🇦🇿 AZ AI Süni İntellekt")
st.caption("Sahveren tərəfindən yaradılmış ilk rəsmi AI saytı")
st.markdown("---")

# Botu işə salırıq (yaddaşda saxlayırıq ki, hər dəfə yenidən yüklənməsin)
if "model" not in st.session_state:
    st.session_state.model = start_bot()

# Söhbət tarixçəsini yaradırıq
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları ekranda göstər
for message in st.session_state.
