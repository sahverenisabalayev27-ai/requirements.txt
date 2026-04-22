import streamlit as st
import google.generativeai as genai

# Səhifə Ayarları
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")

# --- BAYRAQ VƏ BAŞLIQ ---
st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sahveren tərəfindən Azərbaycan üçün hazırlandı</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SECRETS-DƏN OXUMA ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Xəta: {e}. Ehtimal ki, açar yenə bloklanıb. Zəhmət olmasa yeni açar alıb Secrets-ə qoyun.")
else:
    st.warning("Secrets tapılmadı! Settings > Secrets hissəsinə GEMINI_API_KEY əlavə edin.")
