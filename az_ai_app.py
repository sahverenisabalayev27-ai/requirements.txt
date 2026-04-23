import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI", page_icon="🎓", layout="wide")

# CSS Dizayn
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #1a237e; color: white !important; }
    .q-card { background: white; padding: 25px; border-radius: 15px; border-left: 8px solid #1a237e; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .ans-box { background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt, tokens=1500):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=tokens
            )
            return resp.choices[0].message.content
        except: continue
    return None

# 3. Sessiya İdarəetməsi (Qeydiyyat Simulyasiyası)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'score' not in st.session_state: st.session_state.score = 0

# --- QEYDİYYAT PƏNCƏRƏSİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 Akademiya AI - Giriş</h1>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        name = st.text_input("Adınız və Soyadınız:")
        email = st.text_input("Email ünvanınız:")
    with col_r:
        password = st.text_input("Şifrə:", type="password")
        if st.button("Qeydiyyatdan Keç 🚀"):
            if name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.success("Giriş uğurludur!")
                st.rerun()
    st.stop() # Giriş etməyibsə aşağıdakı kodu görməsin

# --- ƏSAS PORTAL ---
st.markdown(f"<h1 style='text-align: center;'>🎓 Xoş gəldin, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("👤 Profil")
    st.write(f"**İstifadəçi:** {st.session_state.user_name}")
    st.metric("Topladığın Xal 🏆", f"{st.session_state.score} XP")
    st.divider()
    subject = st.selectbox("Fənn seç:", ["Tarix", "Azərbaycan dili", "Biologiya", "Fizika", "Riyaziyyat"])
    topic = st.text_input("Mövzu yaz:", value="Səfəvilər")
    if st.button("Çıxış et"):
        st.session_state.logged_in = False
        st.rerun()

tab1, tab2, tab3 = st.tabs(["📖 Öyrən (Dərs)", "📝 Test Sınağı", "✍️ Açıq Sual (Yazılı)"])

# 1. ÖYRƏN BÖLMƏSİ
with tab1:
    if st.button(f"'{topic}' haqqında geniş məlumat al"):
        with st.spinner("Məlumat hazırlanır..."):
            lesson = call_ai(f"{subject} fənnindən {topic} haqqında çox geniş ensiklopedik məlumat yaz.")
            st.markdown(f"<div class='q-card'>{lesson}</div>", unsafe_allow_html=True)

# 2. TEST BÖLMƏSİ
with tab2:
    if st.button("Yeni Test Sualı Gətir 🔄"):
        with st.spinner("Sual hazırlanır..."):
            res = call_ai(f"{subject} fənnindən {topic} haqqında bir test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [Hərf]")
            st.session_state.test_q = res
    
    if 'test_q' in st.session_state:
        st.markdown(f"<div class='q-card'>{st.session_state.test_q}</div>", unsafe_allow_html=True)
        choice = st.radio("Variant seç:", ["A", "B", "C", "D"])
        if st.button("Testi Yoxla"):
            if choice in st.session_state.test_q: # Sadə yoxlama məntiqi
                st.success("Düzdür! +10 XP")
                st.session_state.score += 10
            else: st.error("Səhvdir!")

# 3. AÇIQ SUAL BÖLMƏSİ (YAZILI)
with tab3:
    if st.button("Mənə Açıq Sual Ver ❓"):
        with st.spinner("Sual hazırlanır..."):
            open_q = call_ai(f"{subject} fənnindən {topic} haqqında şagirdin özünün yazmalı olduğu 1 ədəd açıq sual hazırla. Variant olmasın.")
            st.session_state.open_q = open_q
    
    if 'open_q' in st.session_state:
        st.markdown(f"<div class='q-card'><h3>Sual:</h3>{st.session_state.open_q}</div>", unsafe_allow_html=True)
        user_answer = st.text_area("Cavabınızı bura yazın:")
        
        if st.button("Cavabımı Göndər 📤"):
            with st.spinner("Müəllim cavabınızı yoxlayır..."):
                evaluation = call_ai(f"Sual: {st.session_state.open_q}\nŞagirdin cavabı: {user_answer}\nBu cavabı yoxla. Düzdürsə 'DÜZDÜR' yaz və səbəbini izah et, səhvdirsə çatışmazlıqları yaz. Azərbaycan dilində.")
                st.markdown(f"<div class='ans-box'><b>Müəllim rəyi:</b><br>{evaluation}</div>", unsafe_allow_html=True)
                if "DÜZDÜR" in evaluation.upper():
                    st.session_state.score += 20
                    st.balloons()

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren")
