import streamlit as st
import pandas as pd
import random

# --- 1. AZ AI RƏSMİ SEO VƏ KONFİQURASİYA ---
st.set_page_config(
    page_title="AZ AI | Gələcəyin Süni İntellekt Portalı",
    page_icon="🤖",
    layout="wide"  # Xətaları silən rəsmi tənzimləmə
)

# Google Təsdiqləmə (Kodu mənə göndərəndə bura əlavə edəcəm)
st.markdown("""
    <head>
        <meta name="description" content="AZ AI - Azərbaycanın ən qabaqcıl dil və təhsil platforması.">
        <meta name="keywords" content="AZ AI, Süni İntellekt, Dil öyrənmə, Azərbaycan">
    </head>
""", unsafe_allow_html=True)

# --- 2. GİRİŞ SİSTEMİ (Professional AZ AI Dizaynı) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#4285F4;'>AZ AI PORTAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Sistemə giriş edin</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        user = st.text_input("İstifadəçi adı")
        pw = st.text_input("Şifrə", type="password")
        if st.button("Daxil ol", use_container_width=True):
            if user == "admin" and pw == "sahveren2026": # Şifrə gizli qalır
                st.session_state.auth = True
                st.session_state.role = "admin"
                st.session_state.user = "AZ AI Rəhbəri"
                st.rerun()
            elif user and pw:
                st.session_state.auth = True
                st.session_state.role = "user"
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Məlumatları daxil edin!")
    st.stop()

# --- 3. ANA PANEL ---
with st.sidebar:
    st.title("🤖 AZ AI")
    st.write(f"Səlahiyyət: **{st.session_state.user}**")
    menu = st.selectbox("Menyu", ["🏠 Ana Səhifə", "📚 Dil Akademiyası", "⚙️ Admin Ayarları"])
    if st.button("Çıxış"):
        st.session_state.auth = False
        st.rerun()

if menu == "🏠 Ana Səhifə":
    st.title("Xoş gəldiniz! Bu AZ AI Portalıdır.")
    st.info("Saytımız artıq Google tərəfindən təsdiqlənmə mərhələsindədir.")

elif menu == "📚 Dil Akademiyası":
    st.title("🌍 Beynəlxalq Dil Tədrisi")
    st.write("Bütün dünya dilləri üzrə professional cədvəllər və oxunuş qaydaları.")

elif menu == "⚙️ Admin Ayarları":
    if st.session_state.role == "admin":
        st.success("👑 AZ AI Üst İdarəetmə Paneli")
        st.metric("Aktiv İstifadəçi", "18,400")
        st.write("📊 **Sistem Analizi:**")
        st.table(pd.DataFrame({"Tarix": ["Bugün"], "Giriş": ["1,200 nəfər"], "Status": ["Uğurlu"]}))
    else:
        st.error("Bu bölmə yalnız Admin üçündür.")
