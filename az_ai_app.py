import streamlit as st

# --- 1. GOOGLE DOĞRULAMA (İLK SIRADA) ---
# Google bu kodu HTML-in 'head' hissəsində görməlidir.
st.set_page_config(page_title="Sultan Media AI", layout="wide")

st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />
    </head>
    """,
    unsafe_allow_html=True
)

# --- 2. GOOGLE ÜÇÜN ALTERNATİV GİRİŞ (BEKEND) ---
# Əgər Google botu birbaşa fayl kimi axtarsa, bu hissə cavab verəcək.
q_params = st.query_params
if "google-site-verification" in q_params or "verify" in q_params:
    st.write("google-site-verification: fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY")
    st.stop()

# --- 3. SULTAN MEDIA AI - REAL BİZNES PANELİ ---
st.markdown("<h1 style='text-align: center; color: #a78bfa;'>🚀 Sultan Media AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Biznesinizi Süni İntellektlə növbəti səviyyəyə daşıyın</p>", unsafe_allow_html=True)
st.write("---")

# Dashboard Elementləri
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="background-color: #161821; padding: 20px; border-radius: 10px; border: 1px solid #2d2f3b;">
            <h3 style="color: #7c3aed;">📢 SMM AI</h3>
            <p>Instagram postlarını və trend başlıqları saniyələr içində yaradın.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color: #161821; padding: 20px; border-radius: 10px; border: 1px solid #2d2f3b;">
            <h3 style="color: #7c3aed;">💰 Satış Botu</h3>
            <p>Müştəri rəylərini analiz edin və satış strategiyanızı qurun.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background-color: #161821; padding: 20px; border-radius: 10px; border: 1px solid #2d2f3b;">
            <h3 style="color: #7c3aed;">💎 Premium</h3>
            <p>Aylıq abunəlik sistemi ilə limitsiz AI xidmətlərinə giriş əldə edin.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.info("✅ Google Təsdiqləmə Modulu daxil edildi. İndi Google Console-da 'Verify' düyməsini basın.")
