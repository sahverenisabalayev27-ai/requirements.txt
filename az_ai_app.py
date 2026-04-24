import streamlit as st
from groq import Groq
import random
import pandas as pd
import time

# 1. AZ AI Brendinq və Parametrlər
st.set_page_config(page_title="AZ AI | Universal Təhsil", page_icon="🇦🇿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .game-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #3b82f6; padding: 20px; border-radius: 20px; text-align: center; }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .admin-badge { background: #f85149; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Konfiqurasiyası
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_az_ai(prompt, sys_prompt="Sən AZ AI-san. Hər sahədə mütəxəssis olan mükəmməl müəllimsən."):
    if not active_keys: return "API Tapılmadı."
    random.shuffle(active_keys)
    client = Groq(api_key=active_keys[0])
    resp = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=3000
    )
    return resp.choices[0].message.content

# 3. Sessiya İdarəetməsi
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'current_q' not in st.session_state: st.session_state.current_q = None

# --- GİRİŞ SİSTEMİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI Giriş Portal</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("İstifadəçi:")
        p = st.text_input("Şifrə:", type="password")
        if st.button("Sistemə Qoşul 🔓"):
            if u == "admin" and p == "sahveren2026":
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif u and p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🇦🇿 AZ AI")
    if st.session_state.role == "admin":
        st.markdown("<span class='admin-badge'>👑 SULTAN STATUSU</span>", unsafe_allow_html=True)
    st.write(f"Xoş gəldin, **{st.session_state.user}**")
    st.metric("Sənin XP 🏆", st.session_state.xp)
    st.divider()
    menu = st.radio("Menyu:", ["📖 Dərs Mərkəzi", "🎮 Oyun Dünyası", "✍️ Sınaq İmtahanı", "⚙️ Sultan Paneli"])
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 📖 DƏRS MƏRKƏZİ ---
if menu == "📖 Dərs Mərkəzi":
    st.title("📚 Professional Tədris")
    subj = st.selectbox("Fənn:", ["Tarix", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "İngilis dili", "Rus dili"])
    topic = st.text_input("Mövzu daxil edin:", "Maddələr mübadiləsi")
    if st.button("Məlumatı Yüklə ⚡"):
        with st.spinner("AZ AI araşdırır..."):
            res = call_az_ai(f"{subj} fənnindən '{topic}' haqqında ən az 3000 sözlük geniş və akademik məlumat yaz.")
            st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            st.image(f"https://loremflickr.com/1000/400/{topic.replace(' ', ',')}")

# --- 🎮 OYUN DÜNYASI (ÇOXFƏNLİ) ---
elif menu == "🎮 Oyun Dünyası":
    st.title("🕹️ Mövzular Üzrə Yarışmalar")
    g_mode = st.selectbox("Oyun növü seçin:", [
        "🏴 Bayraqlar Yarışı", 
        "🔤 Dil Bilgini (İngilis/Rus)", 
        "🔢 Riyazi Duel", 
        "🧪 Elm Detektivi"
    ])

    if g_mode == "🏴 Bayraqlar Yarışı":
        clist = {"Azərbaycan": "az", "Türkiyə": "tr", "Almaniya": "de", "Yaponiya": "jp", "Braziliya": "br", "İtaliya": "it", "Fransa": "fr"}
        name, code = random.choice(list(clist.items()))
        st.image(f"https://flagcdn.com/w320/{code}.png", width=300)
        opts = random.sample(list(clist.keys()), 4)
        if name not in opts: opts[0] = name
        random.shuffle(opts)
        ans = st.radio("Bu hansı ölkədir?", opts)
        if st.button("Yoxla 🎯"):
            if ans == name:
                st.success("DOĞRU! +50 XP"); st.session_state.xp += 50; st.balloons()
            else: st.error(f"Səhv! Bu {name} idi.")

    elif g_mode == "🔤 Dil Bilgini (İngilis/Rus)":
        st.subheader("Sözün tərcüməsini tap!")
        lang_data = {"Apple": "Alma", "Success": "Uğur", "Freedom": "Azadlıq", "Book": "Kitab", "Sky": "Səma"}
        en, az = random.choice(list(lang_data.items()))
        st.info(f"Söz: **{en}**")
        opts = random.sample(list(lang_data.values()), 4)
        if az not in opts: opts[0] = az
        random.shuffle(opts)
        ans = st.selectbox("Tərcüməsi nədir?", opts)
        if st.button("Yoxla 🔍"):
            if ans == az:
                st.success("Əla! +30 XP"); st.session_state.xp += 30
            else: st.error(f"Səhv! Doğru cavab: {az}")

    elif g_mode == "🔢 Riyazi Duel":
        n1, n2 = random.randint(10, 99), random.randint(10, 99)
        op = random.choice(["+", "-", "*"])
        res = eval(f"{n1}{op}{n2}")
        st.subheader(f"Sürətli Hesabla: {n1} {op} {n2} = ?")
        user_res = st.number_input("Cavabın:", value=0)
        if st.button("Gedişi et ⚔️"):
            if user_res == res:
                st.success("Mükəmməl! +40 XP"); st.session_state.xp += 40
            else: st.error(f"Səhv! Doğru cavab: {res}")

# --- ✍️ SINAQ İMTAHANI (ARIDICIL) ---
elif menu == "✍️ Sınaq İmtahanı":
    st.title("📝 Sonsuz Test Rejimi")
    def next_q():
        res = call_az_ai("Hər hansı fəndən professional test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            st.session_state.current_q = {
                "s": res.split("SUAL:")[1].split("A)")[0].strip(),
                "v": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                "c": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                "i": res.split("İZAH:")[1].strip()
            }
    
    if st.button("Yeni Sual 🔄") or st.session_state.current_q is None:
        next_q(); st.rerun()
    
    if st.session_state.current_q:
        q = st.session_state.current_q
        st.markdown(f"<div class='card'><h3>{q['s']}</h3></div>", unsafe_allow_html=True)
        choice = st.radio("Variant seç:", q['v'], index=None)
        c1, c2 = st.columns(2)
        if c1.button("Cavabı Yoxla ✅"):
            if choice and choice[0] == q['c']:
                st.success(f"Düzdür! {q['i']}"); st.session_state.xp += 20; st.balloons()
            else: st.error(f"Səhv! Doğru variant: {q['c']}")
        if c2.button("Növbəti Sual ➡️"):
            next_q(); st.rerun()

# --- ⚙️ SULTAN PANELİ ---
elif menu == "⚙️ Sultan Paneli":
    if st.session_state.role != "admin":
        st.error("Giriş qadağandır! Yalnız Sahveren daxil ola bilər.")
    else:
        st.title("👑 Sultan İdarəetmə Paneli")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Global Statistika")
        st.metric("Sistem Yükü", "Stabil")
        st.metric("Aktiv API Açarları", len(active_keys))
        st.divider()
        st.write("🔧 **Admin Komandaları:**")
        if st.button("Sistemi Tam Sıfırla"): st.warning("Bütün sessiya məlumatları silindi.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 AZ AI | Sahveren Premium Edition")
