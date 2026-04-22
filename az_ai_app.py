import streamlit as st
import google.generativeai as genai

# Səhifə Ayarları
st.set_page_config(page_title="AI SMM Professional", page_icon="🚀")
st.markdown("<h1 style='text-align: center;'>🇦🇿 AI SMM Professional</h1>", unsafe_allow_html=True)
st.markdown("---")

# API Ayarı
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Aktiv modelləri siyahıdan tapan funksiya
    @st.cache_resource
    def find_working_model():
        try:
            # Sistemdə olan bütün modelləri siyahıya alırıq
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Ən yeni 2.5 və ya 2.0 versiyalarını axtarırıq
            targets = ['models/gemini-2.5-flash', 'models/gemini-2.0-flash', 'models/gemini-1.5-flash', 'models/gemini-pro']
            for target in targets:
                if target in available_models:
                    return target
            return available_models[0] if available_models else None
        except:
            return None

    working_model_name = find_working_model()

    if working_model_name:
        model = genai.GenerativeModel(working_model_name)
        
        st.subheader("📋 Məhsul Məlumatları")
        biznes_adi = st.text_input("Biznesin və ya Mağazanın adı:")
        mehsul = st.text_area("Nə satırsınız və ya hansı xidməti göstərirsiniz?")
        
        if st.button("Tam SMM Paketini Hazırla 🔥"):
            if biznes_adi and mehsul:
                with st.spinner(f"Aktiv model ({working_model_name}) ilə hazırlanır..."):
                    prompt = f"Sən peşəkar SMM-sən. Biznes: {biznes_adi}. Məhsul: {mehsul}. Instagram, Facebook postları və 10 hashtag hazırla. Dil: Azərbaycan."
                    try:
                        response = model.generate_content(prompt)
                        st.success("Paketiniz hazırdır!")
                        st.markdown(response.text)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Xəta: {e}")
            else:
                st.warning("Zəhmət olmasa xanaları doldurun.")
    else:
        st.error("Sizin API açarınızla işləyən heç bir model tapılmadı. Yeni açar almağınız məsləhətdir.")
else:
    st.error("API Key tapılmadı! Settings > Secrets hissəsinə baxın.")
