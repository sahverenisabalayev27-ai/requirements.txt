import streamlit as st
from groq import Groq
import random
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. AZ AI - Vizual Brendinq və Konfiqurasiya
st.set_page_config(page_title="AZ AI | Gələcəyin Təhsili", page_icon="🇦🇿", layout="wide")

# Müasir "Sahveren" Dizaynı
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e2e8f0; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1e293b, #0f172a); }
    .main-card { background: #1a1f2e; padding: 30px; border-radius: 25px; border: 1px solid #2d3748; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
    .admin-only { background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 20px; border-radius: 15px; border: 1px solid #3b82f6; }
    .stButton>button { 
        background: linear-gradient(90deg, #2563eb, #7c3aed); color: white; border: none; 
        border-radius: 10px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #3b82f6; }
    .game-box { background: #1e1b4b; border: 2px solid #4338ca; padding: 20px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AZ AI Mərkəzi Prosessor (AI Engine)
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def az_ai_brain(prompt, sys_msg="Sən AZ AI-san, Sahveren tərəfindən yaradılmış dahi Azərbaycanlı müəllimsən."):
    if not active_keys: return "Sistem Sahibi: API açarlarını yoxlayın!"
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=4000
            )
            return resp.choices[0].message.content
        except: continue
    return "Bağlantı kəsildi. AZ AI hazırda istirahət edir."

# 3. Giriş və Sessiya
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- GİRİŞ EKRANI ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🇦🇿 AZ AI - Təhsil Portalı</h1>", unsafe_allow_html=True)
    with st.container():
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            u = st.text_input("İstifadəçi ID:")
            p = st.text_input("Şifrə:", type="password")
            if st.button("Sistemə Giriş 🚀"):
                if u == "admin" and p == "sahveren2026":
                    st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                    st.rerun()
                elif u and p:
                    st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- SIDEBAR (NAVİQASİYA) ---
with st.sidebar:
    st.markdown(f"<h2 style='color: #60a5fa;'>🇦🇿 AZ AI</h2>", unsafe_allow_html=True)
    st.write(f"Xoş gəldin, **{st.session_state.user}**")
    st.metric("Toplanmış XP 🏆", f"{st.session_state.xp}")
    st.divider()
    
    menu = st.radio("Bölmələr:", ["📚 Öyrənmə Mərkəzi", "🎮 Yarışma və Oyunlar", "⚙️ Parametrlər (Admin)"])
    
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 📚 ÖYRƏNMƏ MƏRKƏZİ ---
if menu == "📚 Öyrənmə Mərkəzi":
    st.title("📖 Akademik İş Sahəsi")
    topic = st.text_input("Mövzu yazın (məs: Atabəylər dövləti):", "Azərbaycan mədəniyyəti")
    
    if st.button("Mövzunu Tədqiq Et 🧠"):
        with st.spinner("AZ AI məlumat toplayır..."):
            res = az_ai_brain(f"'{topic}' haqqında ən az 3000 sözlük, ensiklopedik, çox dərin məlumat yaz.")
            st.session_state.info = res
            st.session_state.img = f"https://loremflickr.com/1000/400/{topic.replace(' ', ',')}"
            
    if 'info' in st.session_state:
        st.image(st.session_state.img, use_container_width=True)
        st.markdown(f"<div class='main-card'>{st.session_state.info}</div>", unsafe_allow_html=True)
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.info[:200]}&tl=tr&client=tw-ob")

# --- 🎮 YARIŞMA VE OYUNLAR ---
elif menu == "🎮 Yarışma və Oyunlar":
    st.title("🎮 İntellektual Yarışma Meydanı")
    game_mode = st.selectbox("Oyun növü seçin:", ["⚔️ Tarixi Duel", "🧩 Söz Labirinti", "🔥 Məntiq Yarışı"])
    
    if st.button("Yarışmanı Başlat 🏁"):
        with st.spinner("AI rəqib hazırlanır..."):
            game_setup = az_ai_brain(f"{game_mode} növündə interaktiv, çox maraqlı bir oyun başlat. İstifadəçini sınağa çək.")
            st.session_state.current_game = game_setup
            
    if 'current_game' in st.session_state:
        st.markdown(f"<div class='game-box'>{st.session_state.current_game}</div>", unsafe_allow_html=True)
        user_reply = st.text_input("Cavabın və ya gedişin:")
        if st.button("Göndər 📤"):
            feedback = az_ai_brain(f"Oyun: {st.session_state.current_game}\nİstifadəçi cavabı: {user_reply}\nBunu qiymətləndir.")
            st.info(feedback)
            if "düzgün" in feedback.lower() or "əla" in feedback.lower():
                st.session_state.xp += 50
                st.balloons()

# --- ⚙️ PARAMETRLƏR (YALNIZ ADMIN) ---
elif menu == "⚙️ Parametrlər (Admin)":
    st.title("⚙️ AZ AI Sistem İdarəetməsi")
    
    if st.session_state.role != "admin":
        st.error("🚫 Bu bölməyə daxil olmaq üçün 'Sultan/Sahib' statusunuz olmalıdır!")
    else:
        st.markdown("<div class='admin-only'>", unsafe_allow_html=True)
        st.subheader("👑 Sahveren - İdarəetmə Paneli")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sistem Statusu", "Online")
        col2.metric("Aktiv API Sayı", len(active_keys))
        col3.metric("Platforma XP", st.session_state.xp)
        
        st.divider()
        st.write("📈 **İstifadəçi Aktivliyi Analizi**")
        stats_data = pd.DataFrame({
            "Bölmə": ["Öyrənmə", "Oyunlar", "Testlər", "Söhbət"],
            "İstifadə (%)": [40, 30, 20, 10]
        })
        fig = px.pie(stats_data, values='İstifadə (%)', names='Bölmə', hole=.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)
        
        st.subheader("🛠️ AZ AI Davranış Ayarları")
        st.select_slider("AI Yaradıcılıq Səviyyəsi (Temperature):", options=["Normal", "Yüksək", "Dahi"])
        st.checkbox("Sistem Loglarını Göstər", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"🇦🇿 AZ AI | Yaradıcı: Sahveren | Sistem Tarixi: {datetime.now().strftime('%d.%m.%Y')}")
