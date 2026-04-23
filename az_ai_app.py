import streamlit as st
from groq import Groq
import random
import pandas as pd
import plotly.express as px

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="Akademiya AI | Sahveren Edition", page_icon="💎", layout="wide")

# Müasir Dizayn (İşıqlı/Qaranlıq rejim dəstəyi ilə)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 15px 25px; background: white; border-radius: 12px;
        font-weight: 600; border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] { background: #1e293b !important; color: white !important; }
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def ai_engine(prompt, difficulty="Professor"):
    if not active_keys: return "API açarı tapılmadı!"
    random.shuffle(active_keys)
    sys_msg = f"Sən {difficulty} səviyyəsində bir müəllimsən. Cavabların akademik, dərin və Azərbaycan dilində olmalıdır."
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
    return "Sistem hazırda yüklüdür, bir az sonra yenidən cəhd edin."

# 3. Yaddaş
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'score' not in st.session_state: st.session_state.score = 0

# --- GİRİŞ PANELİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🎓 Akademiya AI Giriş</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    u = c1.text_input("İstifadəçi adı:")
    p = c2.text_input("Şifrə:", type="password")
    if st.button("Daxil Ol 🚀"):
        if u == "admin" and p == "sahveren2026":
            st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
            st.rerun()
        elif u and p:
            st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
            st.rerun()
    st.stop()

# --- SIDEBAR (PARAMETRLƏR) ---
with st.sidebar:
    st.title("⚙️ Parametrlər")
    st.write(f"İstifadəçi: **{st.session_state.user}**")
    difficulty = st.select_slider("Dərs Səviyyəsi:", options=["Asan", "Orta", "Professor"])
    st.divider()
    subject = st.selectbox("Fənn seçin:", ["Tarix", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "İngilis dili", "Coğrafiya"])
    topic = st.text_input("Mövzu daxil edin:", value="Azərbaycan Tarixi")
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- SAHİB (ADMIN) PANELİ ---
if st.session_state.role == "admin":
    with st.expander("👑 Sahveren - İdarəetmə Paneli"):
        st.success(f"Sistem Aktivdir. Aktiv API Sayı: {len(active_keys)}")
        st.metric("Ümumi Platforma Xalı", f"{st.session_state.score} XP")

# --- TABLAR ---
t1, t2, t3, t4 = st.tabs(["📖 Öyrənmə", "📝 Sual Bankı", "🎮 Oyunlar", "📊 Statistika"])

with t1:
    if st.button("Dərsi Başlat 🚀"):
        with st.spinner("Professor məlumat hazırlayır..."):
            info = ai_engine(f"'{topic}' haqqında çox geniş, ən az 3000 sözlük akademik məlumat ver.", difficulty)
            st.session_state.last_info = info
            st.session_state.img = f"https://source.unsplash.com/800x400/?{topic.replace(' ', ',')}"
    
    if 'last_info' in st.session_state:
        st.image(st.session_state.img, use_container_width=True)
        st.markdown(f"<div class='card'><h2>{topic}</h2><br>{st.session_state.last_info}</div>", unsafe_allow_html=True)
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.last_info[:200]}&tl=tr&client=tw-ob")

with t2:
    def get_q():
        res = ai_engine(f"{subject} - {topic} mövzusunda test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            try:
                st.session_state.q = {
                    "s": res.split("SUAL:")[1].split("A)")[0].strip(),
                    "v": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                    "c": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                    "i": res.split("İZAH:")[1].strip()
                }
            except: st.write("Sual yaradılarkən xəta oldu, yenidən yoxlayın.")

    if st.button("Yeni Sual 🔄") or 'q' not in st.session_state: get_q()
    
    if 'q' in st.session_state:
        st.markdown(f"<div class='card'><b>{st.session_state.q['s']}</b></div>", unsafe_allow_html=True)
        ans = st.radio("Variant seçin:", st.session_state.q['v'], index=None)
        c1, c2 = st.columns(2)
        if c1.button("✅ Yoxla"):
            if ans and ans[0] == st.session_state.q['c']:
                st.success(f"Doğrudur! {st.session_state.q['i']}")
                st.session_state.score += 10
                st.balloons()
            else: st.error(f"Səhvdir! Doğru: {st.session_state.q['c']}")
        if c2.button("Növbəti Sual ➡️"): get_q(); st.rerun()

with t3:
    st.subheader("🎮 Təhsil Oyunları")
    mode = st.selectbox("Oyun növü:", ["Tarixi Roleplay", "Söz Tapmacası", "Məntiq Dueli"])
    if st.button("Oyunu Başlat 🕹️"):
        game = ai_engine(f"{topic} mövzusunda {mode} oyunu qur və şagirdlə interaktiv söhbətə başla.")
        st.markdown(f"<div class='card'>{game}</div>", unsafe_allow_html=True)

with t4:
    st.subheader("📊 Bilik Diaqramın")
    df = pd.DataFrame({"Fənn": ["Tarix", "Riyaziyyat", "Fizika", "Biologiya"], "XP": [random.randint(50, 100) for _ in range(4)]})
    fig = px.bar(df, x='Fənn', y='XP', color='Fənn', title="Fənlər üzrə Tərəqqi")
    st.plotly_chart(fig)
    st.metric("Ümumi XP", st.session_state.score)

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren Premium")
