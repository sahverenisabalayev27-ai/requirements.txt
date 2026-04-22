import streamlit as st
import google.generativeai as genai

# Səhifə Ayarları
st.set_page_config(page_title="AI SMM Ümumi Paket", page_icon="🚀")

st.markdown("<h1 style='text-align: center;'>🇦🇿 AI SMM Professional</h1>", unsafe_allow_html=True)
st.markdown("---")

# API Ayarı
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Modelləri yoxlayan funksiya
    def get_model():
        for m_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(m_name)
                # Test sorğusu
                m.generate_content("test", generation_config={"max_output_tokens": 1})
                return m
            except:
                continue
        return None

    model = get_model()

    if model:
        st.subheader("📋 Məhsul Məlumatları")
        biznes_adi = st.text_input("Biznesin və ya Mağazanın adı:")
        mehsul = st.text_area("Nə satırsınız və ya hansı xidməti göstərirsiniz?")
        
        if st.button("Tam SMM Paketini Hazırla 🔥"):
            if biznes_adi and mehsul:
                with st.spinner("Sizin üçün bütün sosial media planı hazırlanır..."):
                    prompt = f"Sən peşəkar SMM-sən. Biznes: {biznes_adi}. Məhsul: {mehsul}. Instagram, Facebook postları və reklam ideyaları hazırla."
                    try:
                        response = model.generate_content(prompt)
                        st.success("Paketiniz hazırdır!")
                        st.code(response.text)
                    except Exception as e:
                        st.error(f"Xəta: {e}")
            else:
                st.warning("Xanaları doldurun.")
    else:
        st.error("Sizin API açarınız üçün heç bir model (Flash və ya Pro) tapılmadı. Lütfən yeni API açarı alın.")
else:
    st.error("API Key tapılmadı! Secrets bölməsini yoxlayın.")
