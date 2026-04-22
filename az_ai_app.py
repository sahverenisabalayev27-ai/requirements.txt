import streamlit as st
import google.generativeai as genai

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")

# --- 2. DİZAYN (Bayraq və Başlıq) ---
st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sahveren tərəfindən Azərbaycan üçün hazırlandı</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. AĞILLI MODEL SEÇİMİ ---
def initialize_bot():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets hissəsində API açarı tapılmadı!")
        return None
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Mövcud modelləri yoxlayırıq
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ən yeni modelləri üstün tuturuq
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target)
        # Əgər heç biri yoxdursa, siyahıdakı ilk modeli götür
        return genai.GenerativeModel(models[0]) if models else None
    except Exception as e:
        st.error(f"Modellər yüklənərkən xəta: {e}")
        return None

model = initialize_bot()

# --- 4. SÖHBƏT HİSSƏSİ ---
if model:
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
                # Botun Azərbaycan dilində cavab verməsini təmin edirik
                response = model.generate_content(f"Cavabı Azərbaycan dilində ver: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Cavab alınmadı: {e}")
