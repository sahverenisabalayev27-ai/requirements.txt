import streamlit as st
from groq import Groq
import random
import pandas as pd

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="Akademiya AI - Sahveren Edition", page_icon="👑", layout="wide")

# Müasir və Premium CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 55px; background-color: white; border-radius: 12px;
        font-weight: bold; border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] { background-color: #1a237e !important; color: white !important; }
    .admin-card { background: #1a237e; color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .content-card { background: white; padding: 35px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt, system_prompt="Sən akademik bir müəllimsən."):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=4000
            )
            return resp.choices[0].message.content
        except: continue
    return "Limit dolub."

# 3. Yaddaş və İdarəetmə (Sessiya)
if 'score' not in st.session_state: st.session_state.score = 0
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = "user"
if 'db_users' not in st.session_state: st.session_state.db_users = [] # Admin üçün istifadəçi siyahısı

# --- GİRİŞ SİSTEMİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 Akademiya AI-ya xoş gəlmisiniz</h1>", unsafe_allow_html=True)
    l_col, r_col = st.columns(2)
    with l_col:
        user = st.text_input("İstifadəçi adı (Email/Tel):")
        pwd = st.text_input("Şifrə:", type="password")
        if st.button("Daxil Ol 🚀"):
            if user == "admin" and pwd == "sahveren2026": # Sənin xüsusi admin girişin
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.user_name = "Sahveren (Sahib)"
                st.rerun()
            elif user and pwd:
                st.session_state.logged_in = True
                st.session_state.user_role = "user"
                st.session_state.user_name = user
                st.session_state.db_users.append(user)
                st.rerun()
    st.stop()

# --- ADMIN PANELİ (Yalnız sənin üçün) ---
if st.session_state.user_role == "admin":
    with st.expander("🛠️ SAHİBİN İDARƏETMƏ PANELİ (ADMIN)"):
        st.markdown("<div class='admin-card'>Salam, Sahveren! Saytın bütün idarəçiliyi səndədir.</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Ümumi Giriş", len(st.session_state.db_users))
        c2.metric("Aktiv API Açarları", len(active_keys))
        c3.metric("Sistem Statusu", "Stabil")
        st.write("**İstifadəçi Siyahısı:**", st.session_state.db_users)

# --- ƏSAS PORTAL ---
with st.sidebar:
    st.title("🎓 Portal")
    st.write(f"👤 **İstifadəçi:** {st.session_state.user_name}")
    st.metric("Topladığın Xal 🏆", f"{st.session_state.score} XP")
    st.divider()
    subject = st.selectbox("Fənn seç:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "İngilis dili", "Rus dili"])
    topic = st.text_input("Mövzu:", value="Dədə Qorqud dastanı")
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

tab_info, tab_test, tab_game = st.tabs(["📖 Dərin Öyrənmə", "📝 Sual Bankı", "🎮 Təhsil Oyunları"])

# 📖 ÖYRƏNMƏ BÖLMƏSİ (Şəkilli və Səsli)
with tab_info:
    if st.button("Mövzunu Tam İzah Et 🚀"):
        with st.spinner("Ensiklopedik məlumatlar toplanır..."):
            res = call_ai(f"'{topic}' haqqında ən az 3000 sözlük, elmi, çox geniş məlumat ver.")
            st.session_state.info_text = res
            st.session_state.img_url = f"https://source.unsplash.com/800x400/?{topic.replace(' ', ',')}"
            st.rerun()
            
    if 'info_text' in st.session_state:
        st.image(st.session_state.img_url, use_container_width=True)
        st.markdown(f"<div class='content-card'>{st.session_state.info_text}</div>", unsafe_allow_html=True)
        # Səsli Oxuma (TTS)
        st.write("🎙️ **Dərsi Dinlə:**")
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.info_text[:250]}&tl=tr&client=tw-ob"
        st.audio(tts_url)

# 📝 SUAL BANKI (Test + Növbəti Düyməsi)
with tab_test:
    def get_new_q():
        res = call_ai(f"{subject} fənnindən {topic} haqqında çətin test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            st.session_state.q_data = {
                "text": res.split("SUAL:")[1].split("A)")[0].strip(),
                "opts": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                "ans": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                "expl": res.split("İZAH:")[1].strip()
            }

    if st.button("Yeni Sual Hazırla 🔄") or 'q_data' not in st.session_state:
        get_new_q()

    if 'q_data' in st.session_state:
        q = st.session_state.q_data
        st.info(f"**Sual:** {q['text']}")
        choice = st.radio("Variantını seç:", q['opts'], index=None)
        c1, c2 = st.columns(2)
        if c1.button("✅ Yoxla"):
            if choice and choice[0] == q['ans']:
                st.success(f"Düzdür! {q['expl']}")
                st.session_state.score += 10
                st.balloons()
            else: st.error(f"Səhvdir! Doğru: {q['ans']}. İzah: {q['expl']}")
        if c2.button("Növbəti Sual ➡️"):
            get_new_q()
            st.rerun()

# 🎮 OYUNLAR BÖLMƏSİ (Düzəldilmiş)
with tab_game:
    st.subheader("🎮 AI ilə İntellektual Oyun")
    game_mode = st.selectbox("Oyun növü:", ["Tarixi Personajla Söhbət", "Söz Tapmacası", "Məntiq Dueli"])
    if st.button("Oyuna Başla 🕹️"):
        with st.spinner("AI oyun mühitini qurur..."):
            game_res = call_ai(f"Mövzu {topic} üzrə {game_mode} oyunu başlat. Şagirdlə maraqlı şəkildə qarşılıqlı əlaqə qur.")
            st.markdown(f"<div class='content-card'>{game_res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren - Sistem Sahibi Paneli Aktivdir.")
