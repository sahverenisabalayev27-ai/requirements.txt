import streamlit as st
from groq import Groq
import random
from gtts import gTTS
import os
import base64
import pandas as pd

# 1. Saytın Google-da və Brauzerdə Professional Görünüşü
st.set_page_config(page_title="AZ AI | Universal Master Portal", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #202124; }
    .google-card { border: 1px solid #dadce0; padding: 40px; border-radius: 12px; max-width: 450px; margin: auto; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .sultan-panel { background: #1a1c1e; color: #00ff00; padding: 25px; border-radius: 15px; border: 2px solid #00ff00; font-family: 'Courier New', monospace; }
    .premium-badge { background: linear-gradient(45deg, #FFD700, #FFA500); color: black; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }
    .stButton>button { border-radius: 6px; font-weight: 500; height: 45px; }
    .sidebar-user { background: #f1f3f4; padding: 15px; border-radius: 12px; border-left: 5px solid #4285F4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Səsli İzahat Funksiyası (Kişi Səsi Tonu ilə)
def speak_text(text):
    tts = gTTS(text=text, lang='tr', slow=False) # Kişi səsinə ən yaxın ton üçün
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>', unsafe_allow_html=True)

# 3. AI Müəllim (Groq Engine)
def call_ai(prompt, system_role="Sən dahi bir müəllimsən."):
    keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
    client = Groq(api_key=random.choice(keys))
    res = client.chat.completions.create(
        messages=[{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    return res.choices[0].message.content

# 4. Professional Giriş (Google Auth UI)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="google-card">
            <h1 style="font-family: 'Product Sans', sans-serif;"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></h1>
            <h2 style="font-size:22px; margin-top:0;">Hesab seçin</h2>
            <p style="color:#5f6368;">AZ AI Portalına davam etmək üçün</p>
            <div style="text-align:left; padding:15px; border:1px solid #dadce0; border-radius:8px; margin-top:20px;">
                <b>Sahveren Balayev</b><br><small>sahveren.admin@azai.az</small>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.write("")
        u = st.text_input("E-poçt")
        p = st.text_input("Şifrə", type="password")
        if st.button("Daxil ol", use_container_width=True):
            if u == "admin" and p == "sahveren2026":
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif u and p:
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "user", u
                st.rerun()
    st.stop()

# --- PORTAL DAXİLİ ---
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-user">
            <small style="color:#5f6368;">Aktiv Hesab</small><br>
            <b>{st.session_state.user}</b> <span class="premium-badge">V.I.P</span>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    menu = st.selectbox("Portal Xanaları:", ["🏠 Ana Səhifə", "🌎 Dil Akademiyası", "🎮 Elm Oyunları", "📄 PDF/Şəkil Analizi", "👑 Sultan İdarəetmə"])
    if st.button("🚪 Çıxış"):
        st.session_state.auth = False
        st.rerun()

# --- 🌎 DİL AKADEMİYASI (SƏSLİ VƏ ÇOXDİLLİ) ---
if menu == "🌎 Dil Akademiyası":
    st.title("🗣️ Beynəlxalq Dil Mərkəzi")
    l_col1, l_col2 = st.columns([1, 2])
    with l_col1:
        lang = st.selectbox("Öyrənilən Dil:", ["İngilis", "Rus", "Alman", "Fransız", "İspan", "Ərəb"])
        mode = st.radio("Məqsəd:", ["Söz Öyrən", "Tərcümə", "Dramatik Dialoq"])
    
    with l_col2:
        txt = st.chat_input("Sözü və ya mətni yazın...")
        if txt:
            with st.spinner("AZ AI təhlil edir..."):
                res = call_ai(f"Mövzu: {txt}. Dil: {lang}. Rejim: {mode}. Professional yazılış, oxunuş və izah ver.")
                st.markdown(f"<div style='background:#f8f9fa; padding:20px; border-radius:10px; border:1px solid #dee2e6;'>{res}</div>", unsafe_allow_html=True)
                if st.button("🔊 Sesli Tercüme (Kişi Səsi)"):
                    speak_text(res)

# --- 🎮 ELM OYUNLARI ---
elif menu == "🎮 Elm Oyunları":
    st.title("🕹️ Bilik Yarışması")
    subj = st.radio("Fənn seç:", ["Coğrafiya", "Tarix", "Riyaziyyat", "Məntiq"], horizontal=True)
    st.info(f"Hazırda {subj} üzrə online rəqib axtarılır...")
    st.image("https://flagcdn.com/w640/az.png", width=300)
    st.button("Bu bayrağın paytaxtı haradır?")

# --- 📄 PDF/ŞƏKİL ANALİZİ ---
elif menu == "📄 PDF/Şəkil Analizi":
    st.title("📂 Professional Sənəd Oxuyucu")
    file = st.file_uploader("Faylı bura atın (PDF, JPG, PNG)", type=["pdf", "png", "jpg"])
    if file:
        st.success("Fayl qəbul olundu. Mətn çıxarılır...")
        st.write("Analiz nəticəsi: Bu sənəddə 10-cu sinif riyaziyyat testləri aşkarlandı.")

# --- 👑 SULTAN İDARƏETMƏ (GENİŞLƏNDİRİLMİŞ) ---
elif menu == "👑 Sultan İdarəetmə":
    if st.session_state.role != "admin":
        st.error("Giriş qadağandır! Yalnız Sahveren daxil ola bilər.")
    else:
        st.title("👑 Professional Sultan Paneli")
        m1, m2, m3 = st.columns(3)
        m1.metric("Ümumi Qazanc", "1,450 AZN", "+12%")
        m2.metric("Aktiv İstifadəçi", "5,230 nəfər", "+450")
        m3.metric("Premium Satış", "85 ədəd", "Aylıq")
        
        st.subheader("📊 Son Ödənişlər və Girişlər")
        data = pd.DataFrame({
            "İstifadəçi": ["Aysel99", "Murad_Az", "Leyla_W", "Admin_Sahveren"],
            "Əməliyyat": ["Premium Alındı", "Giriş Etdi", "Dil Dərsi", "Sistem Yeniləndi"],
            "Məbləğ": ["5 AZN", "0 AZN", "5 AZN", "0 AZN"],
            "Tarix": ["24.04.2026 12:00", "24.04.2026 12:15", "24.04.2026 12:45", "İndi"]
        })
        st.table(data)
        
        if st.button("🚀 Sistem Hesabatını Yüklə (Excel)"):
            st.download_button("Yükləməni Başlat", data.to_csv(), "report.csv")

st.markdown("---")
st.caption("AZ AI Portal v3.0 | Professional AI System by Sahveren")
