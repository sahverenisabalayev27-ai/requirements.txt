import streamlit as st
import google.generativeai as genai

# --- 1. SƏHİFƏ AYARLARI (Brauzer nişanı və İkon) ---
st.set_page_config(
    page_title="AZ AI - Azərbaycan", 
    page_icon="🇦🇿", 
    layout="centered"
)

# --- 2. AZƏRBAYCAN BAYRAĞI VƏ BAŞLIQ ---
# Səhifənin ən yuxarısına böyük bayraq və başlıq qoyuruq
st.markdown("<h1 style='text-align: center;'>🇦🇿</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #00bfff;'>AZ AI Süni İntellekt</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Sahveren tərəfindən Azərbaycan üçün hazırlandı</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. TƏHLÜKƏSİZ KONFİQURASİYA (Secrets-dən oxuyur) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Söhbət tarixçəsi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Sual-cavab hissəsi
    if prompt := st.chat_input("Mənə bir şey yaz..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Bota Azərbaycan dilində danışmağı tapşırırıq
                full_prompt = f"Sən Azərbaycanlı köməkçisən. Sualı Azərbaycan dilində cavablandır: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("API ilə bağlı problem oldu. Lütfən biraz gözləyin.")
else:
    st.error("API açarı tapılmadı! Zəhmət olmasa 'Secrets' hissəsinə əlavə edin.")
