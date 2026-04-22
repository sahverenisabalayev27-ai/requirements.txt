import streamlit as st
import google.generativeai as genai

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")

# --- 2. AZƏRBAYCAN BAYRAĞI VƏ BAŞLIQ ---
st.markdown("<h1 style='text-align: center;'>🇦🇿</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #00bfff;'>AZ AI Süni İntellekt</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sahveren tərəfindən Azərbaycan üçün hazırlandı</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. API KONFİQURASİYA (Birbaşa Üsul) ---
# Əgər Secrets işləmirsə, bu üsul 100% işləyəcək
try:
    # BURAYA O UZUN AÇARI YAPIŞDIR
    MY_KEY = "AIzaSyDlnTN0DESssF08610WmfcO0BQo1LonASg" 
    
    genai.configure(api_key=MY_KEY)
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
    st.error(f"Xəta baş verdi: {e}")
