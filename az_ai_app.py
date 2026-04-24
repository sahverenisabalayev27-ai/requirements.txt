import streamlit as st
from groq import Groq
import pandas as pd
import random
from gtts import gTTS
import base64

# 1. Professional Portal Ayarları
st.set_page_config(page_title="AZ AI | Universal Language Academy", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #202124; }
    .book-page { 
        background: #fdfdfd; 
        padding: 40px; 
        border: 1px solid #e0e0e0; 
        border-radius: 5px; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        font-family: 'Georgia', serif;
    }
    .alphabet-box { 
        display: grid; 
        grid-template-columns: repeat(auto-fill, minmax(60px, 1fr)); 
        gap: 10px; 
        margin: 20px 0;
    }
    .letter-card { 
        border: 1px solid #ddd; 
        text-align: center; 
        padding: 10px; 
        border-radius: 4px;
        background: #f8f9fa;
    }
    .sultan-panel { background: #000; color: #0f0; padding: 20px; border-radius: 10px; border: 1px solid #0f0; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI & Səs Mühərriki
def get_ai_lesson(prompt):
    try:
        keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
        client = Groq(api_key=random.choice(keys))
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən dünya dilləri üzrə dahi bir dilçisən. Məlumatları cədvəl və kitab formatında ver."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return resp.choices[0].message.content
    except: return "Hazırda server yüklüdür, zəhmət olmasa təkrar yoxlayın."

# 3. Giriş Sistemi
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><h1 style='text-align:center; color:#4285F4;'>AZ AI Portal</h1>", unsafe_allow_html=True)
        email = st.text_input("E-poçt")
        password = st.text_input("Şifrə", type="password")
        if st.button("Daxil ol", use_container_width=True):
            if email == "admin" and password == "sahveren2026":
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif "@" in email:
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "user", email.split("@")[0]
                st.rerun()
    st.stop()

# --- PORTAL MENYUSU ---
with st.sidebar:
    st.title("🌐 AZ AI GLOBAL")
    st.write(f"Profil: **{st.session_state.user}**")
    menu = st.radio("Bölmələr:", ["📖 Dil Ensiklopediyası", "🎮 Bilik Yarışması", "⚙️ Ayarlar"])
    if st.button("Çıxış"):
        st.session_state.auth = False
        st.rerun()

# --- 📖 DİL ENSİKLOPEDİYASI ---
if menu == "📖 Dil Ensiklopediyası":
    st.title("📚 Beynəlxalq Dil Tədrisi (Kitab Formatı)")
    
    # Bütün dünya dillərini seçmək üçün
    all_languages = ["İngilis", "Rus", "Alman", "Fransız", "İspan", "İtalyan", "Çin", "Yapon", "Koreya", "Ərəb", "Türk", "Fars", "Portuqal", "Yunan", "Hind", "Vyetnam"]
    lang = st.selectbox("Öyrənmək istədiyiniz dili seçin:", all_languages)
    
    st.markdown(f"<div class='book-page'>", unsafe_allow_html=True)
    st.header(f"📗 {lang} Dilinin Tədris Kitabı")
    
    tab1, tab2, tab3 = st.tabs(["🔤 Əlifba və Hərflər", "🗣️ Oxunuş Qaydaları", "📊 Söz Cədvəli"])
    
    with tab1:
        st.subheader("Əlifba Siyahısı")
        if st.button(f"{lang} əlifbasını gətir"):
            res = get_ai_lesson(f"{lang} dilinin bütün hərflərini və onların oxunuşunu siyahı halında yaz.")
            st.write(res)

    with tab2:
        st.subheader("Fonetika və Tələffüz")
        st.write("Bu dildə xüsusi səs birləşmələri və oxunuş sirrləri:")
        if st.button(f"{lang} fonetikasını öyrət"):
            res = get_ai_lesson(f"{lang} dilində sözlərin necə oxunması haqqında 5 qızıl qayda yaz.")
            st.info(res)

    with tab3:
        st.subheader("Mövzu üzrə Lüğət Cədvəli")
        topic = st.selectbox("Mövzu:", ["Salamlaşma", "Ailə", "Rəqəmlər", "Mətbəx", "Texnologiya"])
        if st.button("Cədvəli Yarat"):
            res = get_ai_lesson(f"{lang} dilində {topic} mövzusunda 10 sözlük cədvəl qur: Söz - Yazılış - Oxunuş - Tərcümə.")
            st.markdown(res)
            
            # Səsli Oxunuş
            if st.button("🔊 Bu dərsi səsli dinlə"):
                tts = gTTS(text=f"{lang} dili dərsi hazırlandı.", lang='tr')
                tts.save("v.mp3")
                st.audio("v.mp3")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⚙️ AYARLAR ---
elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Tənzimləmələr")
    st.subheader("İstifadəçi Ayarları")
    st.selectbox("Səhifə Modu:", ["Aydın", "Qaranlıq", "Sultan"])
    
    if st.session_state.role == "admin":
        st.markdown("<div class='sultan-panel'>", unsafe_allow_html=True)
        st.subheader("👑 SULTAN İŞ KABİNETİ")
        c1, c2, c3 = st.columns(3)
        c1.metric("İzləyici Sayı", "18,400", "+500")
        c2.metric("Aylıq Qazanc", "3,200 AZN", "+15%")
        c3.metric("Ödənişlər", "240 ədəd", "Uğurlu")
        
        st.write("📋 **İstifadəçi Giriş Siyahısı:**")
        logs = pd.DataFrame({
            "İstifadəçi": ["Aysel88", "Ali_Az", "Leyla_W", "User_01"],
            "Ölkə/Dil": ["İngilis", "Rus", "Yapon", "Alman"],
            "Status": ["Premium", "Pulsuz", "Premium", "Pulsuz"]
        })
        st.table(logs)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 AZ AI Portal | Sahveren Edition")
