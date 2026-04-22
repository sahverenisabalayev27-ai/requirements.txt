import streamlit as st
import google.generativeai as genai

# --- 1. KONFİQURASİYA ---
API_KEY = "AIzaSyDlnTN0DESssF08610WmfcO0BQo1LonASg"
genai.configure(api_key=API_KEY)

# Ağıllı Model Seçimi
@st.cache_resource
def get_active_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

selected_model_name = get_active_model()

# --- BOTUN XARAKTERİ (Sistem Təlimatı) ---
instruction = (
    "Sənin adın AZ AI-dır. Sən Sahveren tərəfindən yaradılmış ağıllı köməkçisən. "
    "Bütün suallara ilk növbədə Azərbaycan dilində cavab verməyə çalış. "
    "Amma istifadəçi başqa dildə (İngilis, Rus, Türk və s.) yazarsa, həmin dildə də mükəmməl cavab ver. "
    "Mehriban, köməkcil və dəqiq ol."
)

model = genai.GenerativeModel(
    model_name=selected_model_name,
    system_instruction=instruction
)

# --- 2. SAYTIN DİZAYNI ---
st.set_page_config(page_title="AZ AI - Sahveren", page_icon="🇦🇿")
st.title("🇦🇿 AZ AI Süni İntellekt")
st.caption(f"Sahveren tərəfindən təkmilləşdirildi | Model: {selected_model_name}")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. SUAL-CAVAB ---
if prompt := st.chat_input("Mənə istənilən dildə sual ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Bot artıq təlimatlara uyğun cavab verəcək
            response = model.generate_content(prompt)
            ai_message = response.text
            st.markdown(ai_message)
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
        except Exception as e:
            st.error(f"Xəta: {e}")
