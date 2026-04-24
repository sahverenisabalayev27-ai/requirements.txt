import streamlit as st
from groq import Groq
import random
import pandas as pd
from gtts import gTTS
import base64

# 1. Professional Konfiqurasiya
st.set_page_config(page_title="AZ AI | Professional Workspace", page_icon="🧠", layout="wide")

# Google Style Dizayn
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #202124; }
    .google-card { border: 1px solid #dadce0; padding: 40px; border-radius: 12px; max-width: 450px; margin: auto; text-align: center; }
    .sultan-dashboard { background: #000000; color: #00ff00; padding: 20px; border-radius: 10px; border: 1px solid #00ff00; font-family: monospace; }
    .stButton>button { border-radius: 5px; font-weight: bold; height: 45px; }
    .user-section { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #4285F4; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Funksiyası
def get_ai_response(prompt, role="Sən dahi bir müəllimsən."):
    try:
        keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
        client = Groq(api_key=random.choice(keys))
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except: return "Sistem hazırda məşğuldur. Bir az sonra yoxlayın."

# 3. Giriş Sistemi (Daha Professional)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
            <div class="google-card">
                <h1 style="color:#4285F4">G<span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span>g<span style="color:#34A853">l</span>e</h1>
                <h3>Giriş edin</h3>
                <p>AZ AI Portalına davam etmək üçün</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1.5,1])
        with col2:
            email = st.text_input("E-poçt və ya telefon", placeholder="Məs: admin@azai.az")
            password = st.text_input("Şifrə", type="password", placeholder="••••••••")
            
            if st.button("Növbəti", use_container_width=True):
                if email == "admin" and password == "sahveren2026":
                    st.session_state.auth, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                    st.rerun()
                elif "@" in email and len(password) > 5:
                    st.session_state.auth, st.session_state.role, st.session_state.user = True, "user", email.split("@")[0]
                    st.rerun()
                else:
                    st.error("E-poçt düzgün deyil və ya şifrə çox qısadır.")
    st.stop()

# --- SİSTEM DAXİLİ ---
with st.sidebar:
    st.markdown(f"""
        <div class="user-section">
            <small>Aktiv Profil</small><br>
            <b>{st.session_state.user}</b> {'👑' if st.session_state.role == 'admin' else '🎓'}
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.selectbox("Bölmələr:", ["🏠 Ana Səhifə", "🌎 Dil Öyrənmə", "🎮 Oyunlar", "⚙️ Ayarlar"])
    
    if st.button("🚪 Sistemdən çıx"):
        st.session_state.auth = False
        st.rerun()

# --- 🏠 ANA SƏHİFƏ ---
if menu == "🏠 Ana Səhifə":
    st.title(f"Xoş gəldin, {st.session_state.user}!")
    st.markdown("### Gündəlik Planın")
    st.info("Bugün İngilis dili və Riyaziyyat üzrə 2 yeni dərsin var.")

# --- 🌎 DİL ÖYRƏNMƏ ---
elif menu == "🌎 Dil Öyrənmə":
    st.title("🗣️ Beynəlxalq Dil Akademiyası")
    lang = st.selectbox("Öyrənmək istədiyiniz dil:", ["İngilis", "Rus", "Alman", "Fransız"])
    q = st.chat_input("Sözü və ya mövzunu yazın...")
    if q:
        res = get_ai_response(f"{q} mövzusunu {lang} dilində izah et, tərcümə və tələffüzünü yaz.")
        st.write(res)
        if st.button("🔊 Sesli Tercüme"):
            tts = gTTS(text=res[:100], lang='tr') # Nümunə səs
            tts.save("s.mp3")
            st.audio("s.mp3")

# --- 🎮 OYUNLAR ---
elif menu == "🎮 Oyunlar":
    st.title("🕹️ Elm və Əyləncə")
    st.write("Tezliklə: Online rəqabət sistemi aktiv ediləcək.")

# --- ⚙️ AYARLAR (HƏMİ ÜÇÜN AÇIQ, AMMA ADMİNƏ ÖZƏL HİSSƏ İLƏ) ---
elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Tənzimləmələr")
    
    # 1. Hamı üçün görünən ayarlar
    st.subheader("Profil Ayarları")
    st.text_input("Görünən ad:", value=st.session_state.user)
    st.selectbox("Sistem dili:", ["Azərbaycan", "Türk", "English"])
    st.checkbox("Bildirişləri aktiv et", value=True)
    
    # 2. Yalnız Sənə (Sultana) görünən əsas iş ayarları
    if st.session_state.role == "admin":
        st.markdown("---")
        st.markdown("<h2 style='color:#4285F4;'>👑 SULTAN İŞ PANALİ (Gizli)</h2>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
                <div class="sultan-dashboard">
                    <h3>📊 Statistika</h3>
                    <p>Ümumi Gəlir: 1,450 AZN</p>
                    <p>Yeni İstifadəçilər: +120 bugün</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown("### 💳 Son Ödənişlər")
            st.table(pd.DataFrame({
                "Ad": ["Aysel", "Elvin", "Leyla"],
                "Məbləğ": ["5 AZN", "5 AZN", "5 AZN"],
                "Status": ["Uğurlu", "Uğurlu", "Gözləmədə"]
            }))
            
        if st.button("🚀 Bütün sistem məlumatlarını Excel-ə çıxar"):
            st.success("Hesabat hazırlandı!")

st.markdown("---")
st.caption("AZ AI © 2026 | Sahveren Pro Edition")
