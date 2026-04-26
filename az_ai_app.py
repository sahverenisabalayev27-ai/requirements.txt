import streamlit as st

# 1. GOOGLE TƏSDİQİ ÜÇÜN ƏN QƏTİ ÜSUL
# Bu hissə saytın HTML-nin tam yuxarısına Google-un kodunu yerləşdirir.
st.set_page_config(page_title="Sultan Media AI", layout="wide")

# Google bu meta etiketini sayt açılan kimi görməlidir
st.markdown(
    f"""
    <head>
        <meta name="google-site-verification" content="googlee9f98e586bf85b6c.html" />
    </head>
    """,
    unsafe_allow_html=True
)

# 2. ALTERNATİV YOL (Əgər Google linklə yoxlasa)
# Bu hissə saytın sonuna ?verify yazanda kodu ekrana çıxarır
q_params = st.query_params
if "verify" in q_params:
    st.write("google-site-verification: googlee9f98e586bf85b6c.html")
    st.stop()

# --- SAYTIN MƏZMUNU (SULTAN MEDIA AI) ---
st.markdown("<h1 style='text-align: center; color: #a78bfa;'>🚀 Sultan Media AI</h1>", unsafe_allow_html=True)
st.write("---")

st.info("💡 Google Təsdiqləmə rejimi aktivdir. Zəhmət olmasa Google Console-da 'Verify' düyməsini sıxın.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🤖 AI Biznes Asistanı")
    st.write("SMM, Satış və Müştəri xidmətləri üçün ağıllı həllər.")

with col2:
    st.subheader("💰 Gəlir Modeli")
    st.write("Aylıq abunəlik və premium xidmətlərlə biznesinizi böyüdün.")
