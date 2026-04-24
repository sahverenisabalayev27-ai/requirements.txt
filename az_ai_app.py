import streamlit as st
from groq import Groq
import random
import pandas as pd

# 1. Professional Konfiqurasiya
st.set_page_config(
    page_title="AZ AI | Professional Workspace", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI Dizayn (Mənim sistemimə bənzər)
st.markdown("""
    <style>
    .stApp { background-color: #0e1113; color: #e1e1e1; }
    .login-card {
        background: #1c1f23;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
    }
    .stTextInput>div>div>input {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(45deg, #1f6feb, #238636);
        margin: 0 auto 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        background: #238636 !important;
        border: none !important;
        font-weight: bold;
    }
    .sidebar-user {
        padding: 15px;
        background: #161b22;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Beyni (Groq Cloud)
def get_ai_response(prompt):
    active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
    if not active_keys: return "Sistem Sahibi: API Key-ləri əlavə edin!"
    try:
        client = Groq(api_key=random.choice(active_keys))
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən AZ AI-san. Sahveren tərəfindən yaradılmış dahi assistentsən."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except: return "Sistem hazırda yüklüdür."

# 3. Professional Giriş Məntiqi (Session State)
if 'auth_status' not in st.session_state: st.session_state.auth_status = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_role' not in st.session_state: st.session_state.user_role = "guest"

def login_user(username, password):
    if username == "admin" and password == "sahveren2026":
        st.session_state.auth_status = True
        st.session_state.user_name = "Sahveren"
        st.session_state.user_role = "admin"
        return True
    elif username and password: # Digər hər kəs üçün sadə giriş
        st.session_state.auth_status = True
        st.session_state.user_name = username
        st.session_state.user_role = "user"
        return True
    return False

# --- EKRAN 1: GİRİŞ PƏNCƏRƏSİ ---
if not st.session_state.auth_status:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div class='login-card'>
                <div class='user-avatar'>AZ</div>
                <h2 style='margin-bottom:5px;'>Xoş gəlmisiniz</h2>
                <p style='color: #8b949e;'>AZ AI hesabınızla davam edin</p>
            </div>
        """, unsafe_allow_html=True)
        
        user_input = st.text_input("İstifadəçi adı və ya Email", placeholder="Məs: admin")
        pass_input = st.text_input("Şifrə", type="password", placeholder="••••••••")
        
        if st.button("Daxil ol"):
            if login_user(user_input, pass_input):
                st.success("Giriş uğurludur! Yönləndirilir...")
                time_sleep = 1
                st.rerun()
            else:
                st.error("İstifadəçi adı və ya şifrə yanlışdır.")
    st.stop()

# --- EKRAN 2: ƏSAS İŞ SAHƏSİ (Sidebarsız görünməz) ---
with st.sidebar:
    # Profil hissəsi (Eynilə məndə olduğu kimi)
    st.markdown(f"""
        <div class='sidebar-user'>
            <small style='color: #8b949e;'>Aktiv Profil</small><br>
            <b>{st.session_state.user_name}</b> 
            <br><small>{'👑 Sultan' if st.session_state.user_role == 'admin' else '🎓 Tələbə'}</small>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Naviqasiya", ["🏠 Ana Səhifə", "📚 Dərslər", "🎮 Yarışmalar", "⚙️ Ayarlar"])
    
    st.spacer = st.markdown("<br>"*10, unsafe_allow_html=True)
    if st.button("🚪 Sistemdən çıx"):
        st.session_state.auth_status = False
        st.rerun()

# --- BÖLMƏLƏR ---
if menu == "🏠 Ana Səhifə":
    st.title(f"Salam, {st.session_state.user_name}! 👋")
    st.write("Bu gün nə öyrənmək istəyirsən? AZ AI sənin üçün hazırdır.")
    
    # Tez-tez verilən suallar (Mənim ana səhifəm kimi)
    cols = st.columns(3)
    with cols[0]:
        if st.button("🌍 Coğrafiya testi et"): pass
    with cols[1]:
        if st.button("📜 Tarixi araşdır"): pass
    with cols[2]:
        if st.button("💡 Məntiq sualı ver"): pass

elif menu == "📚 Dərslər":
    st.title("📖 Tədris Mərkəzi")
    topic = st.chat_input("Mövzu daxil edin...")
    if topic:
        with st.chat_message("assistant"):
            response = get_ai_response(f"{topic} haqqında ətraflı məlumat ver.")
            st.markdown(response)

elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    # Sənin istədiyin Sultan bölməsi
    if st.session_state.user_role == "admin":
        st.info("👑 Sən hazırda Sultan statusundasan.")
        tab1, tab2 = st.tabs(["Statistika", "Maliyyə"])
        with tab1:
            st.write("Aktiv İzləyicilər: **1,450**")
        with tab2:
            st.write("Cari ayın qazancı: **520 AZN**")
    else:
        st.write("Profil ayarları və dil seçimləri tezliklə əlavə olunacaq.")

elif menu == "🎮 Yarışmalar":
    st.title("🎮 Online Yarışma")
    st.warning("Tezliklə: Digər tələbələrlə canlı yarış!")
