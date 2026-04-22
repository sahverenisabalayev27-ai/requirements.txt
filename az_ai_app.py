import streamlit as st
import google.generativeai as genai

# Səhifə Ayarları
st.set_page_config(page_title="AI SMM Ümumi Paket", page_icon="🚀")

st.markdown("<h1 style='text-align: center;'>🇦🇿 AI SMM Professional</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Biznesinizi süni intellektlə böyüdün</p>", unsafe_allow_html=True)
st.markdown("---")

# API Təhlükəsizliyi
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Sadə Giriş Formu
    st.subheader("📋 Məhsul Məlumatları")
    biznes_adi = st.text_input("Biznesin və ya Mağazanın adı:")
    mehsul = st.text_area("Nə satırsınız və ya hansı xidməti göstərirsiniz?")
    
    if st.button("Tam SMM Paketini Hazırla 🔥"):
        if biznes_adi and mehsul:
            with st.spinner("Sizin üçün bütün sosial media planı hazırlanır..."):
                
                # Süni intellektə "Ümumi" tapşırıq veririk
                prompt = f"""
                Sən peşəkar SMM və Marketinq mütəxəssisisən. 
                Biznes adı: {biznes_adi}
                Məhsul/Xidmət: {mehsul}
                
                Lütfən aşağıdakıları Azərbaycan dilində, çox cəlbedici və peşəkar şəkildə hazırla:
                1. Instagram üçün emoji ilə zəngin post mətni və 15 hashtag.
                2. Facebook üçün daha ətraflı məlumatlandırıcı post.
                3. Bu məhsulu daha çox satmaq üçün 3 qısa reklam ideyası.
                4. Story-lərdə paylaşmaq üçün 3 maraqlı fikir.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("Paketiniz hazırdır!")
                    
                    # Nəticəni gözəl formada göstəririk
                    st.markdown("### ✨ Hazır SMM Paketiniz")
                    st.code(response.text, language="markdown") # Rahat kopyalamaq üçün
                    
                    st.info("Yuxarıdakı mətni kopyalayıb birbaşa paylaşa bilərsiniz!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Xəta baş verdi: {e}")
        else:
            st.warning("Lütfən bütün xanaları doldurun.")
else:
    st.error("API Key tapılmadı! Zəhmət olmasa Secrets bölməsini yoxlayın.")
