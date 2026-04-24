import streamlit as st
from groq import Groq
import random
import time

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="AZ AI - Giriş", page_icon="🌐", layout="tight")

# Professional Google Style CSS
st.markdown("""
    <style>
    /* Ümumi fon */
    .stApp { background-color: white !important; color: #202124 !important; }
    
    /* Giriş Kartı */
    .login-container {
        max-width: 450px;
        margin: auto;
        padding: 40px;
        border: 1px solid #dadce0;
        border-radius: 8px;
        text-align: center;
        font-family: 'Google Sans',arial,sans-serif;
    }
    
    /* Google Logosu */
    .google-logo {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .g-blue { color: #4285F4; } .g-red { color: #EA4335; } 
    .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

    /* Giriş Düymələri */
    .stButton>button {
        border-radius: 4px !important;
        height: 40px !important;
        font-weight: 500 !important;
        text-transform: none !important;
    }
    .google-btn > button {
        background-color: white !important;
        color: #3c4043 !important;
        border: 1px solid #dadce0 !important;
    }
    .next-btn > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Sidebar rəngi */
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6; }
    [data-testid="stSidebar"] * { color: #3c4043 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya İdarəetməsi
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = None

# --- GİRİŞ EKRANI (GOOGLE STYLE) ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Mərkəzi Giriş Qutusu
    with st.container():
        st.markdown("""
            <div class="login-container">
                <div class="google-logo">
                    <span class="g-blue">A</span><span class="g-red">Z</span>
                    <span class="g-yellow">A</span><span class="g-green">I</span>
                </div>
                <h2 style="font-size: 24px; margin-bottom: 8px; color: #202124;">Daxil olun</h2>
                <p style="font-size: 16px; margin-bottom: 24px; color: #202124;">AZ AI hesabınızla davam edin</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Email və Şifrə sahələri
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            email = st.text_input("E-poçt və ya telefon", placeholder="Məs: admin@azai.az")
            password = st.text_input("Şifrənizi daxil edin", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Google Düyməsi Simulyasiyası
            st.markdown("<div class='google-btn'>", unsafe_allow_html=True)
            if st.button("🔴 🟡 🔵 Google ilə daxil olun"):
                st.info("Google hesabı ilə əlaqə qurulur...")
                time.sleep(1)
                st.session_state.auth = True
                st.session_state.user = "Google İstifadəçisi"
                st.session_state.role = "user"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            # Növbəti Düyməsi (Real Giriş)
            st.markdown("<div class='next-btn'>", unsafe_allow_html=True)
            if st.button("Növbəti"):
                if email == "admin" and password == "sahveren2026":
                    st.session_state.auth = True
                    st.session_state.user = "Sahveren"
                    st.session_state.role = "admin"
                    st.rerun()
                elif email and password:
                    st.session_state.auth = True
                    st.session_state.user = email.split("@")[0]
                    st.session_state.role = "user"
                    st.rerun()
                else:
                    st.error("Məlumatları daxil edin")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<p style='text-align:left; color:#1a73e8; font-size:14px; font-weight:500; cursor:pointer;'>Hesab yaradın</p>", unsafe_allow_html=True)
    st.stop()

# --- SİSTEMİN DAXİLİ (Daxil olduqdan sonra) ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user}")
    st.write(f"Status: **{st.session_state.role.upper()}**")
    st.divider()
    menu = st.radio("Menyu", ["🌐 Ana Səhifə", "📚 Dərslər", "⚙️ Ayarlar"])
    
    if st.button("Çıxış et"):
        st.session_state.auth = False
        st.rerun()

# --- ƏSAS KONTENT ---
if menu == "🌐 Ana Səhifə":
    st.title(f"Xoş gəldin, {st.session_state.user}!")
    st.markdown("<div style='background-color:#f1f3f4; padding:20px; border-radius:10px; color:black;'>Gündəlik təhsil planın hazırdır. Başlamaq üçün dərslər bölməsinə keç.</div>", unsafe_allow_html=True)

elif menu == "📚 Dərslər":
    st.title("📖 AZ AI Təlimat")
    q = st.chat_input("Sualınızı buraya yazın...")
    if q:
        st.write(f"**Sən:** {q}")
        st.write("**AZ AI:** Bu mövzu üzərində işləyirəm...")

elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Parametrlər")
    if st.session_state.role == "admin":
        st.success("👑 Sultan Paneli Aktivdir")
        st.write("Aylıq Qazanc: **500 AZN**")
        st.write("İzləyici: **1200**")
    else:
        st.write("Profil tənzimləmələri tezliklə aktiv olacaq.")
