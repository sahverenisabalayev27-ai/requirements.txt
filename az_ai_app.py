import streamlit as st

# 1. GOOGLE TƏSDİQLƏMƏ VƏ SAYT AYARLARI
st.set_page_config(page_title="AZ AI | Global Portal", page_icon="🤖", layout="wide")

# Google kodu bura yerləşdirildi (Xətanı silən əsas sətir)
st.markdown("""
    <head>
        <meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />
    </head>
""", unsafe_allow_html=True)

# 2. ANA PANEL VƏ BÖLMƏLƏR
st.title("🤖 AZ AI Dünyasına Xoş Gəldiniz!")

# Menyu (İtən bölmələri bura bərpa edirik)
with st.sidebar:
    st.header("AZ AI İdarəetmə")
    page = st.selectbox("Bölmə seçin:", ["🏠 Ana Səhifə", "🎮 Oyunlar", "📚 Təhsil Portalı", "⚙️ Sultan Paneli"])

if page == "🏠 Ana Səhifə":
    st.success("Sistem Google tərəfindən təsdiqlənməyə hazırdır!")
    st.write("Bu portal Azərbaycanın ən qabaqcıl süni intellekt sistemidir.")

elif page == "🎮 Oyunlar":
    st.header("🕹️ Məntiq Oyunları")
    st.info("Oyunlar bazası yenilənir... Bütün köhnə oyunlar bura yüklənəcək.")

elif page == "📚 Təhsil Portalı":
    st.header("📖 Sual-Cavab və Təhsil")
    st.write("Sualınızı bura yazın, AZ AI cavablandırsın.")
    st.text_input("Sual:")

elif page == "⚙️ Sultan Paneli":
    st.header("👑 Sultan Sahveren üçün Özəl Panel")
    st.warning("Bu bölməyə giriş yalnız admin üçündür.")
