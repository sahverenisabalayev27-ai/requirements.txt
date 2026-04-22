import streamlit as st
import google.generativeai as genai

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")

# --- 2. SECRETS YOXLANIŞI ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Aktiv modeli avtomatik tapan funksiya
    @st.cache_resource
    def get_working_model():
        try:
            # Əvvəlcə Flash modelini yoxlayırıq
            model = genai.GenerativeModel('gemini-1.5-flash')
            model.generate_content("test") # Test yoxlanışı
            return 'gemini-1.5-flash'
        except:
            try:
                # Flash yoxdursa Pro modelini yoxlayırıq
                model = genai.GenerativeModel('gemini-pro')
                return 'gemini-pro'
            except:
                return None

    model_name = get_working_model()
    
    if model_name:
        model = genai.GenerativeModel(model_name)
        
        # --- 3. DİZAYN (Bayraq və Başlıq) ---
        st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AZ AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic;'>Sahveren tərəfindən Azərbaycan üçün hazırlandı</p>", unsafe_allow_html=True)
        st.markdown("---")

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
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Xəta: {e}")
    else:
        st.error("Hesabınızda aktiv model tapılmadı. Lütfən API açarını yeniləyin.")
else:
    st.warning("Secrets tapılmadı! Settings > Secrets hissəsinə GEMINI_API_KEY əlavə edin.")
