import streamlit as st
import google.generativeai as genai

# --- 1. BOTUN BEYNİ (Dünənki uğurlu kodun bura uyğunlaşdırılması) ---
def start_bot():
    try:
        # Secrets-dən açarı götürürük
        api_key = st.secrets["AIzaSyC44lz2MFk9cM5cq_Ma41OCcWCxIk0fL8k"]
        genai.configure(api_key=api_key)
        
        # Sənin açarına uyğun ən yaxşı modeli avtomatik tapırıq
        model_name = 'gemini-1.5-flash' # Standart olaraq bunu seçirik
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                break
        
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")
        return None

# --- 2. SAYTIN DİZAYNI ---
st.set_page_config(page_title="AZ AI - Sahveren", page_icon="🇦🇿")

st.title("🇦🇿 AZ AI Süni İntellekt")
st.info("Dünənki bot artıq saytımızda canlandı!")

# Botu işə salırıq
if "model" not in st.session_state:
    st.session_state.model = start_bot()

# Söhbət tarixçəsini yaradırıq
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. SUAL-CAVAB HİSSƏSİ ---
if prompt := st.chat_input("Sualınızı bura yazın..."):
    # İstifadəçi sualı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı
    if st.session_state.model:
        with st.chat_message("assistant"):
            try:
                response = st.session_state.model.generate_content(prompt)
                ai_message = response.text
                st.markdown(ai_message)
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error("Cavab alınmadı. API açarını yoxlayın.")
    else:
        st.warning("Bot hələ hazır deyil. Secrets hissəsini tənzimləyin.")
