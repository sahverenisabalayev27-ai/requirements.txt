import streamlit as st
from groq import Groq
import random
import pandas as pd
import plotly.express as px

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="Akademiya AI | Sahveren Edition", page_icon="💎", layout="wide")

# Premium CSS Dizayn
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] {
        padding: 15px 25px; background: white; border-radius: 12px 12px 0 0;
        font-weight: 600; color: #64748b;
    }
    .stTabs [aria-selected="true"] { background: #1e293b !important; color: white !important; }
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f1f5f9; }
    .admin-box { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sistem Məntiqi (API)
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def ai_engine(prompt, difficulty="Professor"):
    random.shuffle(active_keys)
    sys_msg = f"Sən {difficulty} səviyyəsində bir müəllimsən. Məlumatı çox ətraflı, akademik və Azərbaycan dilində təqdim et."
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
    return "Xəta: Sistem yüklüdür."

# 3. Yaddaş və Parametrlər
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'difficulty' not in st.session_state: st.session_state.difficulty = "Professor"
if 'theme' not in st.session_state: st.session_state.theme = "Light"

# --- GİRİŞ PANELİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🏫 Akademiya AI Giriş</h1>", unsafe_allow_html=True)
    with st.container():
        c1, c2 = st.columns(2)
        u = c1.text_input("İstifadəçi adı:")
        p = c2.text_input("Şifrə:", type="password")
        if st.button("Giriş 🚀"):
            if u == "admin" and p == "sahveren2026":
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif u and p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                st.rerun()
    st.stop()

# --- SAHİB (ADMIN) GÖSTƏRİCİLƏRİ ---
if st.session_state.role == "admin":
    with st.sidebar:
        st.markdown("<div class='admin-box'>👑 <b>Sahib Paneli</b><br>Sistem Tam Aktivdir</div>", unsafe_allow_html=True)
        st.write(f"🔑 API Açarları: {len(active_keys)}")
        if st.button("Sistemi Yenilə 🔄"): st.rerun()

# --- PARAMETRLƏR VƏ PROFİL (SIDEBAR) ---
with st.sidebar:
    st.title("👤 Profilim")
    st.write(f"Xoş gəldin, **{st.session_state.user}**")
    st.divider()
    st.subheader("⚙️ Parametrlər")
    st.session_state.difficulty = st.select_slider("Dərs Çətinliyi:", options=["Asan", "Orta", "Professor"])
    st.session_state.theme = st.selectbox("Görünüş:", ["İşıqlı", "Qaranlıq (Dark Mode)"])
    
    st.divider()
    subject = st.selectbox("Fənn:", ["Tarix", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "İngilis dili", "Coğrafiya"])
    topic = st.text_input("Mövzu:", "Azərbaycanın Müasir Tarixi")
    
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- ƏSAS İNTERFEYS ---
t1, t2, t3, t4 = st.tabs(["📖 Öyrənmə Mərkəzi", "📝 Sual Bankı", "🎮 Oyunlar", "📊 Statistikam"])

# 1. ÖYRƏNMƏ (PARAMETRƏ UYĞUN)
with t1:
    if st.button("Dərsi Başlat 🚀"):
        with st.spinner("Məlumatlar analiz edilir..."):
            info = ai_engine(f"'{topic}' haqqında {st.session_state.difficulty} səviyyəsində geniş məlumat ver.", st.session_state.difficulty)
            st.session_state.last_info = info
            st.session_state.img = f"https://source.unsplash.com/800x400/?{topic.replace(' ', ',')}"
    
    if 'last_info' in st.session_state:
        st.image(st.session_state.img, use_container_width=True)
        st.markdown(f"<div class='card'><h2>{topic}</h2><br>{st.session_state.last_info}</div>", unsafe_allow_html=True)
        # Səs
        st.write("🎙️ **Səsli İzahat:**")
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.last_info[:200]}&tl=tr&client=tw-ob")

# 2. SUAL BANKI (ARIDICIL SİSTEM)
with t2:
    def load_q():
        res = ai_engine(f"{subject} - {topic} mövzusunda çətin bir test sualı hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            st.session_state.q = {
                "s": res.split("SUAL:")[1].split("A)")[0].strip(),
                "v": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                "c": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                "i": res.split("İZAH:")[1].strip()
            }

    if st.button("Yeni Sual 🔄") or 'q' not in st.session_state: load_q()
    
    if 'q' in st.session_state:
        st.markdown(f"<div class='card'><h4>{st.session_state.q['s']}</h4></div>", unsafe_allow_html=True)
        ans = st.radio("Seçiminiz:", st.session_state.q['v'], index=None)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Cavabı Yoxla"):
            if ans and ans[0] == st.session_state.q['c']:
                st.success(f"Mükəmməl! {st.session_state.q['i']}")
                st.session_state.score += 10
                st.balloons()
            else: st.error(f"Səhv! Doğru variant: {st.session_state.q['c']}")
        
        if c2.button("Növbəti Sual ➡️"):
            load_q()
            st.rerun()

# 3. OYUNLAR (DİNAMİK ROLEPLAY)
with t3:
    st.subheader("🎮 İntellektual Ssenarilər")
    g_type = st.selectbox("Oyun növü:", ["Tarixi Debat", "Sirli Tapmaca", "Gələcəkdən Məktub"])
    if st.button("Oyuna Gir 🕹️"):
        game_content = ai_engine(f"{topic} haqqında {g_type} formatında interaktiv oyun başlat.")
        st.markdown(f"<div class='card'>{game_content}</div>", unsafe_allow_html=True)

# 4. STATİSTİKA (PARAMETR ANALİZİ)
with t4:
    st.subheader("📊 Sənin Tərəqqi Qrafikin")
    data = pd.DataFrame({
        "Fənn": ["Tarix", "Riyaziyyat", "Fizika", "Biologiya"],
        "Bilik Səviyyəsi": [random.randint(40, 100) for _ in range(4)]
    })
    fig = px.line_polar(data, r='Bilik Səviyyəsi', theta='Fənn', line_close=True)
    st.plotly_chart(fig)
    st.metric("Ümumi Toplanmış Xal", f"{st.session_state.score} XP")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren Premium")
