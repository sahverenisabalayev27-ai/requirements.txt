import streamlit as st
import google.generativeai as genai

# --- KONFİQURASİYA ---
# Bura yeni emailinlə aldığın API açarını dırnaq içində yaz
API_KEY = "AIzaSyC44lz2MFk9cM5cq_Ma41OCcWCxIk0fL8k" 
genai.configure(api_key=API_KEY)

# Modeli sazlayırıq
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SAYTIN GÖRÜNÜŞÜ ---
st.set_page_config(page_title="AZ AI", page_icon="🇦🇿")

st.title("🇦🇿 AZ AI Süni İntellekt")
st.markdown("---")

# Söhbət tarixçəsi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual daxil etmə sahəsi
if prompt := st.chat_input("Mənə bir sual ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Cavabın alınması
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Xəta: {e}")
