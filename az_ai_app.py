import streamlit as st
import pandas as pd

# --- XƏTANI HƏLL EDƏN HİSSƏ ---
st.set_page_config(
    page_title="AZ AI | Official Portal",
    page_icon="🇦🇿",
    layout="wide"  # "tight" yazma, yoxsa yenə qırmızı xəta verəcək!
)

# Google Təsdiqləmə sahəsi (Kodu bura qoyacağıq)
st.markdown("""
    <head>
        </head>
""", unsafe_allow_html=True)

# --- GİRİŞ SİSTEMİ (Qadağanı aradan qaldıran hissə) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🌐 AZ AI - Giriş")
    user = st.text_input("İstifadəçi adı")
    pw = st.text_input("Şifrə", type="password")
    if st.button("Daxil ol"):
        if user == "admin" and pw == "sahveren2026":
            st.session_state.auth = True
            st.session_state.role = "admin"
            st.rerun()
        else:
            st.error("Məlumatlar yanlışdır!")
    st.stop()

# --- ƏSAS SAYT ---
st.success(f"Xoş gəldin, Sahveren! Sistem artıq xətasız işləyir.")
st.write("İndi Google Search Console-dan HTML teqini gözləyirik.")
