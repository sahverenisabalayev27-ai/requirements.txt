import streamlit as st
import pandas as pd
from groq import Groq
import random

# --- 1. GOOGLE TƏSDİQLƏMƏ VƏ SEO AYARLARI ---
st.set_page_config(
    page_title="AZ AI | Gələcəyin Süni İntellekt Portalı",
    page_icon="🤖",
    layout="wide"  # Qırmızı xətaları silən əsas sətir
)

# Sənin göndərdiyin Google kodu bura yerləşdirildi
st.markdown(f"""
    <head>
        <meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />
        <meta name="description" content="AZ AI - Azərbaycanın ən qabaqcıl dil və təhsil portalı.">
    </head>
""", unsafe_allow_html=True)

# --- 2. GİRİŞ SİSTEMİ (Qadağanı Aradan Qaldıran) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#4285F4;'>🤖 AZ AI PORTAL</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        st.info("Sistem rəsmi Google qeydiyyatından keçdi. Giriş edin:")
        user = st.text_input("İstifadəçi adı (Email)")
        pw = st.text_input("Şifrə", type="password")
        if st.button("Daxil ol", use_container_width=True):
            if user == "admin" and pw == "sahveren2026":
                st.session_state.auth = True
                st.session_state.role = "admin"
                st.session_state.user = "AZ AI Rəhbəri"
                st.rerun()
            elif "@" in user and len(pw) > 5:
                st.session_state.auth = True
                st.session_state.role = "user"
                st.session_state.user = user.split("@")[0]
                st.rerun()
            else:
                st.error("Məlumatlar yanlışdır və ya çatışmır!")
    st.stop()

# --- 3. ANA PANEL (Sahveren üçün Özəl) ---
with st.sidebar:
    st.title("🤖 AZ AI GLOBAL")
    st.write(f"Səlahiyyət: **{st.session_state.user}**")
    menu = st.selectbox("Menyu", ["🏠 Ana Səhifə", "📚 Dil Akademiyası", "⚙️ Sultan Paneli"])
    if st.button("Çıxış"):
        st.session_state.auth = False
        st.rerun()

if menu == "🏠 Ana Səhifə":
    st.title("🤖 AZ AI Dünyasına Xoş Gəldiniz!")
    st.success("Sistem rəsmi olaraq təsdiqləndi və xətalar təmizləndi.")
    st.write("Artıq saytımız Google axtarış sistemlərində indekslənir.")

elif menu == "📚 Dil Akademiyası":
    st.title("🌍 Dünya Dilləri Ensiklopediyası")
    st.info("Burada bütün dillərin hərfləri, oxunuşları və cədvəlləri yer alacaq.")
    # AI funksiyalarını bura əlavə edə bilərsən

elif menu == "⚙️ Sultan Paneli":
    if st.session_state.role == "admin":
        st.markdown("<h2 style='color:#00ff00;'>👑 AZ AI Üst İdarəetmə Paneli</h2>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        col_a.metric("İzləyici Sayı", "18,400", "+1.2k")
        col_b.metric("Sistem Statusu", "Aktiv", "Google Verified")
        
        st.write("📋 **İstifadəçi Qeydləri:**")
        st.table(pd.DataFrame({
            "İstifadəçi": ["Yeni_İzləyici_1", "Sahveren_Admin"],
            "Zaman": ["İndi", "Aktiv"],
            "Məkan": ["Baku", "HQ"]
        }))
    else:
        st.error("Bu bölmə yalnız AZ AI rəhbərliyi üçündür!")

st.markdown("---")
st.caption("AZ AI © 2026 | Professional Language System")
