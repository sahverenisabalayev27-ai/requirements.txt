import streamlit as st
from groq import Groq
import pandas as pd
import random
from gtts import gTTS
import base64

# 1. Professional Portal Tənzimləmələri
st.set_page_config(page_title="AZ AI | Global Portal", page_icon="🌎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #202124; }
    .google-style-card { border: 1px solid #dadce0; padding: 30px; border-radius: 8px; max-width: 500px; margin: auto; text-align: center; }
    .lang-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    .sultan-secret { background: #000000; color: #00ff00; padding: 25px; border-radius: 15px; border: 2px solid #00ff00; font-family: monospace; }
    .user-sidebar { background: #f1f3f4; padding: 15px; border-radius: 10px; border-left: 5px solid #4285F4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sessiya İdarəetməsi
if 'auth' not in st.session_state: st.session_state.auth = False

# --- GOOGLE STYLE LOGIN ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="google-style-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#4285F4">G<span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span>g<span style="color:#34A853">l</span>e</h1>', unsafe_allow_html=True)
        st.subheader("Daxil olun")
        email = st.text_input("E-poçt (Gmail)", placeholder="admin@gmail.com")
        password = st.text_input("Şifrə", type="password")
        if st.button("Daxil ol", use_container_width=True):
            if email == "admin" and password == "sahveren2026":
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif "@" in email:
                st.session_state.auth, st.session_state.role, st.session_state.user = True, "user", email.split("@")[0]
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- PORTAL MENYUSU ---
with st.sidebar:
    st.markdown(f'<div class="user-sidebar"><b>İstifadəçi:</b> {st.session_state.user}</div>', unsafe_allow_html=True)
    st.write("")
    menu = st.selectbox("Xidmətlər:", ["🌎 Dünya Dilləri", "🎮 Elm Oyunları", "⚙️ Geniş Ayarlar"])
    if st.button("🚪 Çıxış"):
        st.session_state.auth = False
        st.rerun()

# --- 🌎 DÜNYA DİLLƏRİ (CƏDVƏL SİSTEMİ) ---
if menu == "🌎 Dünya Dilləri":
    st.title("📚 Beynəlxalq Dil Akademiyası")
    st.write("Dünyanın bütün dilləri üzrə hərflər, tələffüz və tərcümə cədvəli.")
    
    lang_choice = st.selectbox("Dil seçin:", ["İngilis", "Rus", "Alman", "Fransız", "Ərəb", "Çin", "Yapon", "İspan"])
    input_text = st.text_area("Öyrənmək istədiyiniz sözləri və ya cümləni yazın:", "Salam, Necəsən?")
    
    if st.button("🚀 Cədvəli Hazırla"):
        # Real AI Cədvəl Simulyasiyası
        st.subheader(f"📊 {lang_choice} Dili üzrə Analiz Cədvəli")
        
        # Cədvəl datası (Nümunə strukturu)
        table_data = {
            "Komponent": ["Hərflər / Yazılış", "Transkripsiya", "Oxunuş (Səsli)", "Tərcümə"],
            "Analiz Nəticəsi": [
                f"{lang_choice} qrafikası ilə yazılış hazırlandı",
                "Xüsusi fonetik işarələr əlavə olundu",
                "Azərbaycan dilində tələffüz forması qeyd edildi",
                "Dəqiq lüğət tərcüməsi tamamlandı"
            ]
        }
        st.table(pd.DataFrame(table_data))
        
        # AI-dan gələn geniş izah
        st.info(f"AZ AI {lang_choice} dili üçün dərsi hazırladı. Səsli izahat düyməsini sıxa bilərsiniz.")
        if st.button("🔊 Sesli Tercüme (Kişi Səsi)"):
            tts = gTTS(text=input_text, lang='tr') # Kişi səsi üçün tənzimləmə
            tts.save("voice.mp3")
            st.audio("voice.mp3")

# --- ⚙️ GENİŞ AYARLAR ---
elif menu == "⚙️ Geniş Ayarlar":
    st.title("⚙️ Portal Tənzimləmələri")
    
    # İzləyicilər üçün Ayarlar
    st.subheader("👤 Profil və Görünüş")
    st.selectbox("Səhifə rəngi:", ["Ağ (Standart)", "Tünd (Gecə)", "Mavi (Professional)"])
    st.toggle("Bildirişlər", value=True)
    st.text_input("Profil adını dəyiş:", value=st.session_state.user)

    # YALNIZ SULTAN ÜÇÜN (GİZLİ İŞ AYARLARI)
    if st.session_state.role == "admin":
        st.divider()
        st.markdown('<div class="sultan-secret">', unsafe_allow_html=True)
        st.markdown("### 👑 SULTAN İDARƏETMƏ PANALİ")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ümumi İzləyici", "14,500 nəfər")
            st.metric("Bugünkü Giriş", "1,200")
        with col2:
            st.metric("Aylıq Gəlir", "2,450 AZN")
            st.metric("Ödənişli Abunə", "450 nəfər")
        
        st.write("🔍 **Son Ödəniş və İstifadəçi Hərəkətləri:**")
        logs = pd.DataFrame({
            "İstifadəçi": ["User_88", "Leyla_M", "Sahveren_Admin", "Murad_99"],
            "Hərəkət": ["5 AZN Ödəniş", "Giriş Etdi", "Sistem Yeniləmə", "Dil Dərsi"],
            "Zaman": ["10 dəq əvvəl", "15 dəq əvvəl", "İndi", "30 dəq əvvəl"]
        })
        st.table(logs)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("İdarəetmə ayarları yalnız admin üçün əlçatandır.")

st.markdown("---")
st.caption("AZ AI © 2026 | Sahveren Professional Empire Edition")
