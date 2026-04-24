import streamlit as st
from groq import Groq
import random
import time

# 1. Professional Konfiqurasiya (Xətalar düzəldildi)
st.set_page_config(
    page_title="AZ AI | Giriş", 
    page_icon="🌐", 
    layout="wide"
)

# Modern Google Style CSS
st.markdown("""
    <style>
    .stApp { background-color: white !important; color: #202124 !important; }
    
    /* Login Kartı */
    .login-box {
        max-width: 450px;
        margin: auto;
        padding: 40px;
        border: 1px solid #dadce0;
        border-radius: 8px;
        text-align: center;
    }
    
    /* Google Rəngli Logo */
    .g-logo { font-size: 30px; font-weight: bold; margin-bottom: 10px; }
    .b { color: #4285F4; } .r { color: #EA4335; } 
    .y { color: #FBBC05; } .g { color: #34A853; }

    /* Düymələr */
    .stButton>button {
        border-radius: 4px !important;
        height: 45px !important;
        font-weight: 500 !important;
    }
    .main-btn > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
    }
    .google-btn > button {
        background-color: white !important;
        color: #3c4043 !important;
        border: 1px solid #dadce0 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6; }
    [data-testid="stSidebar"] * { color: #3c4043 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya Yaddaşı
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = None

# --- GİRİŞ EKRANI (GOOGLE STYLE) ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div class="login-box">
                <div class="g-logo">
                    <span class="b">A</span><span class="r">Z</span>
                    <span class="y">A</span><span class="g">I</span>
                </div>
                <h2 style="font-size: 24px; color: #202124;">Daxil olun</h2>
                <p style="color: #202124;">AZ AI ilə təhsilinizə davam edin</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            email_input = st.text_input("E-poçt", placeholder="admin")
            pass_input = st.text_input("Şifrə", type="password", placeholder="••••••••")
            
            st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
            if st.button("Növbəti"):
                if email_input == "admin" and pass_input == "sahveren2026":
                    st.session_state.auth = True
                    st.session_state.user = "Sahveren"
                    st.session_state.role = "admin"
                    st.rerun()
                elif email_input and pass_input:
                    st.session_state.auth = True
                    st.session_state.user = email_input
                    st.session_state.role = "user"
                    st.rerun()
                else:
                    st.warning("Məlumatları daxil edin")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<p style='text-align:center; margin:10px 0;'>və ya</p>", unsafe_allow_html=True)

            st.markdown("<div class='google-btn'>", unsafe_allow_html=True)
            if st.button("🔵 Google ilə davam et"):
                st.session_state.auth = True
                st.session_state.user = "Google User"
                st.session_state.role = "user"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- DAXİLİ SİSTEM ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user}")
    st.write(f"Vəzifə: **{st.session_state.role.upper()}**")
    st.divider()
    menu = st.radio("Menyu", ["🏠 Ana Səhifə", "📚 Dərslər", "⚙️ Ayarlar"])
    
    if st.button("🚪 Çıxış"):
        st.session_state.auth = False
        st.rerun()

if menu == "🏠 Ana Səhifə":
    st.title(f"Xoş gəldin, {st.session_state.user}!")
    st.write("AZ AI sənə özəl dərsləri hazırladı.")

elif menu == "📚 Dərslər":
    st.title("📖 AI Müəllim Paneli")
    st.chat_input("Nəyi öyrənmək istəyirsən?")

elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Parametrlər")
    if st.session_state.role == "admin":
        st.success("👑 Sultan Sahveren - Maliyyə Paneli Aktivdir")
        st.write("Aylıq qazanc: **520 AZN**")
    else:
        st.write("Profil ayarları tezliklə...")
