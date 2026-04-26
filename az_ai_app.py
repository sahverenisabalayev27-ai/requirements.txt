import streamlit as st

# --- 1. GOOGLE-UN İSTƏDİYİ "FAYL" MƏNTİQİ ---
# Bu hissə Google-un o qırmızı xətanı verməsinin qarşısını alacaq.

query_params = st.query_params

# Google-un səndən istədiyi fayl adı və içindəki kod
target_file = "googlee9f98e586bf85b6c.html"
verification_code = "google-site-verification: googlee9f98e586bf85b6c.html"

# Əgər kimsə (Google) saytın sonuna ?file=google... yazsa, bu kod işə düşür
if "file" in query_params and query_params["file"] == target_file:
    st.write(verification_code)
    st.stop()

# --- 2. SAYTIN ƏSAS GÖRÜNÜŞÜ (SULTAN MEDIA AI) ---
st.set_page_config(page_title="Sultan Media AI", layout="wide")

st.markdown("<h1 style='text-align: center; color: #a78bfa;'>🚀 Sultan Media AI</h1>", unsafe_allow_html=True)
st.write("---")

st.info("💡 Google Təsdiqləmə rejimi üçün xüsusi link aktivdir.")

# Biznes bölmələri
col1, col2 = st.columns(2)
with col1:
    st.subheader("🤖 AI Biznes")
    st.write("SMM və Satışın avtomatlaşdırılması.")
with col2:
    st.subheader("💰 Gəlir")
    st.write("Abunəlik modeli ilə qazanc.")
