import streamlit as st
import google.generativeai as genai

# Səhifəni sadə başladırıq ki, ağ ekran olmasın
st.set_page_config(page_title="Sultan AI", layout="centered")

st.title("💎 Sultan AI: Aktivasiya Paneli")

# API Key daxil etmə hissəsi
api_key = st.text_input("Google AI Key-i bura yapışdırın:", type="password")

if api_key:
    try:
        # Boşluqları təmizləyirik ki, 'invalid' xətası verməsin
        clean_key = api_key.strip()
        genai.configure(api_key=clean_key)
        
        # Ən stabil modeli seçirik
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test sorğusu göndəririk
        if st.button("Sistemi Yoxla"):
            with st.spinner("Sultan AI cavab gözləyir..."):
                response = model.generate_content("Salam, sistem işləyir?")
                st.success("Təbriklər! Sistem tam işləkdir.")
                st.write(f"AI Cavabı: {response.text}")
                
    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")
        st.info("Məsləhət: API Key-i yenidən kopyalayın və ya 5 dəqiqə gözləyin.")
else:
    st.warning("Zəhmət olmasa, yuxarıdakı qutuya API Key-inizi daxil edin.")
