import streamlit as st
from groq import Groq
import random
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Ultra Modern Səhifə Ayarları
st.set_page_config(page_title="Gemini Pro - Sahveren Edition", page_icon="🧠", layout="wide")

# Müasir "AI Workspace" Dizaynı
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stSidebar { background-color: #1e293b !important; }
    .card { 
        background: #1e293b; padding: 25px; border-radius: 20px; 
        border: 1px solid #334155; margin-bottom: 20px; 
    }
    .user-msg { background: #334155; padding: 15px; border-radius: 15px; margin: 10px 0; }
    .ai-msg { background: #1e40af; padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #60a5fa; }
    .stButton>button { 
        border-radius: 12px; width: 100%; height: 3em; 
        background: linear-gradient(90deg, #3b82f6, #2563eb); color: white; border: none;
    }
    h1, h2, h3 { color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# 2. API və Beyin Funksiyası
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def brain(prompt, system_instruction="Sən mükəmməl bir süni intellektsən."):
    if not active_keys: return "Sistem xətası: API açarları daxil edilməyib."
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=4000
            )
            return resp.choices[0].message.content
        except: continue
    return "Bağlantı kəsildi. Yenidən yoxlayın."

# 3. Sessiya İdarəetməsi (Chat Tarixçəsi)
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'score' not in st.session_state: st.session_state.score = 0

# --- GİRİŞ PORTALI (PRO DİZAYN) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🧠 Gemini Pro Təhsil Portalı</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            u = st.text_input("Giriş ID:")
            p = st.text_input("Şifrə:", type="password")
            if st.button("Sistemə Qoşul 🔓"):
                if u == "admin" and p == "sahveren2026":
                    st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                    st.rerun()
                elif u and p:
                    st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- SIDEBAR (SİSTEM PARAMETRLƏRİ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=100)
    st.title("⚙️ AI Panel")
    st.info(f"İstifadəçi: **{st.session_state.user}**")
    
    mode = st.radio("Sistem Rejimi:", ["Öyrənmə", "Sınaq", "Canlı Söhbət", "Parametrlər"])
    st.divider()
    
    if st.session_state.role == "admin":
        st.warning("👑 Admin Rejimi Aktivdir")
        st.write(f"Sistem Saatı: {datetime.now().strftime('%H:%M')}")
    
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- ƏSAS EKRAN (DİNAMİK TABLAR) ---
if mode == "Öyrənmə":
    st.title("📖 Akademik Öyrənmə Sahəsi")
    topic = st.text_input("Mövzu seçin:", "Kvant Fizikası")
    if st.button("Məlumatı Generasiya Et ⚡"):
        with st.spinner("AI analiz edir..."):
            res = brain(f"'{topic}' haqqında akademik, detallı və şəkillərlə canlandırıla bilən geniş məlumat yaz.")
            st.session_state.last_lesson = res
            st.session_state.img = f"https://loremflickr.com/1200/500/{topic.replace(' ', ',')}"
            
    if 'last_lesson' in st.session_state:
        st.image(st.session_state.img, use_container_width=True)
        st.markdown(f"<div class='card'>{st.session_state.last_lesson}</div>", unsafe_allow_html=True)

elif mode == "Sınaq":
    st.title("📝 Süni İntellekt Sınaqları")
    if st.button("Yeni Səviyyə Sualı 🔄"):
        res = brain("İstənilən fəndən çətin bir test sualı hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            st.session_state.q_active = res
            
    if 'q_active' in st.session_state:
        st.markdown(f"<div class='card'>{st.session_state.q_active}</div>", unsafe_allow_html=True)
        user_ans = st.radio("Variant seç:", ["A", "B", "C", "D"], key="exam_radio")
        if st.button("Yoxla"):
            if user_ans in st.session_state.q_active:
                st.success("Təbriklər! Doğru tapdınız. +20 XP")
                st.session_state.score += 20
                st.balloons()
            else: st.error("Təəssüf, cavab yanlışdır.")

elif mode == "Canlı Söhbət":
    st.title("💬 AI Asistentlə Söhbət")
    chat_container = st.container()
    user_input = st.chat_input("Nəyi öyrənmək istəyirsən?")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Düşünürəm..."):
            ai_res = brain(user_input)
            st.session_state.chat_history.append({"role": "ai", "content": ai_res})

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div class='user-msg'>👤 **Sən:** {chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-msg'>🤖 **AI:** {chat['content']}</div>", unsafe_allow_html=True)

elif mode == "Parametrlər":
    st.title("🛠️ Sistem Parametrləri")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.slider("AI Cavab Sürəti:", 0.1, 1.0, 0.8)
    st.checkbox("Səsli Cavab Aktiv Olsun", value=True)
    st.selectbox("Sistem Dili:", ["Azərbaycan", "English", "Russian"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.role == "admin":
        st.subheader("📊 İstifadəçi Analitikası")
        chart_data = pd.DataFrame({"Gün": ["B.e", "Ç.a", "Ç", "C.a", "C"], "Giriş": [12, 45, 23, 67, 34]})
        st.plotly_chart(px.bar(chart_data, x="Gün", y="Giriş", title="Sistem Yükü"))

st.markdown("---")
st.caption(f"© 2026 Gemini-Sahveren AI Engine | XP: {st.session_state.score}")
