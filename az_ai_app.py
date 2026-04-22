import streamlit as st
import google.generativeai as genai

# Səhifə başlığı
st.title("🇦🇿 AZ AI Süni İntellekt")

# Secrets-dən açarı götürürük
try:
    # BURADA DİQQƏT: Secrets-də yazdığın adla eyni olmalıdır
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if prompt := st.chat_input("Sualınızı yazın..."):
        st.chat_message("user").markdown(prompt)
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
except Exception as e:
    st.error(f"Xəta: {e}")
    st.info("Zəhmət olmasa Secrets hissəsində GEMINI_API_KEY əlavə edin.")
