import streamlit as st
import pandas as pd

# --- XƏTANI DÜZƏLDƏN KONFİQURASİYA ---
st.set_page_config(
    page_title="AZ AI | Official Portal",
    page_icon="🇦🇿",
    layout="wide"  # "tight" yazma, qırmızı xətanın səbəbi budur!
)

# Google Təsdiqləmə (Kod gələndə bura qoyacağıq)
st.markdown("""<head></head>""", unsafe_allow_html=True)

# --- GİRİŞ SİSTEMİ ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🌐 AZ AI - Giriş Portalı")
    st.info("Sistem rəsmi qeydiyyatdan keçir, zəhmət olmasa daxil olun.")
    user = st.text_input("İstifadəçi adı (admin)")
    pw = st.text_input("Şifrə", type="password")
    if st.button("Sistemə Gir"):
        if user == "admin" and pw == "sahveren2026":
            st.session_state.auth = True
            st.session_state.role = "admin"
            st.rerun()
        else:
            st.error("Məlumatlar yanlışdır!")
    st.stop()

# --- ƏSAS PANEL ---
st.balloons()
st.success(f"Təbriklər, Sahveren! Artıq qırmızı xətalar yoxdur.")
st.write("İndi Google Search Console-da o göy düyməyə basıb kodu götürə bilərsən.")
