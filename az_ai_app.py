import streamlit as st
from groq import Groq
import random
import pandas as pd
import time

# 1. AZ AI - Brendinq və Üslub
st.set_page_config(page_title="AZ AI - Mega Portal", page_icon="🇦🇿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    .stSidebar { background-color: #0f172a !important; border-right: 1px solid #1e293b; }
    .card { background: #111827; padding: 25px; border-radius: 20px; border: 1px solid #374151; margin-bottom: 15px; }
    .stButton>button { 
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; 
        border-radius: 12px; font-weight: 600; border: none; padding: 10px 20px;
    }
    .flag-img { border-radius: 10px; border: 2px solid #374151; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    .admin-status { color: #10b981; font-weight: bold; background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Konfiqurasiyası
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def get_az_ai(prompt, difficulty="Professor"):
    if not active_keys: return "API Xətası."
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Sən AZ AI-san. {difficulty} səviyyəsində, mükəmməl izahlar verən müəllimsən."},
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=4000
            )
            return resp.choices[0].message.content
        except: continue
    return "Bağlantı kəsildi."

# 3. Yaddaş və Giriş Sistemi
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_test' not in st.session_state: st.session_state.current_test = None

# --- LOGİN SİSTEMİ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI PORTAL</h1>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        u = st.text_input("Giriş ID (və ya Email):")
        p = st.text_input("Şifrə:", type="password")
        if st.button("Daxil Ol ✨"):
            if u == "admin" and p == "sahveren2026":
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif u and p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                st.rerun()
    st.stop()

# --- SIDEBAR NAVİQASİYA ---
with st.sidebar:
    st.markdown("### 🇦🇿 AZ AI MENU")
    st.write(f"Səviyyə: **{st.session_state.user}**")
    if st.session_state.role == "admin":
        st.markdown("<div class='admin-status'>👑 SULTAN STATUSU AKTİVDİR</div>", unsafe_allow_html=True)
    
    st.metric("Toplanmış XP", st.session_state.xp if 'xp' in st.session_state else 0)
    st.divider()
    
    choice = st.selectbox("Haraya gedirik?", ["📚 Tədris Mərkəzi", "🧪 Sınaq Otağı", "🎮 Oyun & Yarışma", "⚙️ Admin Ayarları"])
    
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 📚 TƏDRİS MƏRKƏZİ ---
if choice == "📚 Tədris Mərkəzi":
    st.title("📖 Akademik Bilik Bazası")
    topic = st.text_input("Hansı mövzunu öyrənmək istəyirsən?", "Böyük İpək Yolu")
    if st.button("Dərsi Başlat 🚀"):
        with st.spinner("AZ AI araşdırır..."):
            lesson = get_az_ai(f"'{topic}' haqqında ən az 3500 sözlük, başlıqlarla və maraqlı faktlarla dolu bir külliyyat yaz.")
            st.markdown(f"<div class='card'>{lesson}</div>", unsafe_allow_html=True)
            st.image(f"https://loremflickr.com/800/400/{topic.replace(' ', ',')}")

# --- 🧪 SINAQ OTAĞI (NÖVBƏTİ DÜYMƏSİ İLƏ) ---
elif choice == "🧪 Sınaq Otağı":
    st.title("📝 Ardıcıl Test Sistemi")
    
    def generate_new_question():
        res = get_az_ai("Tarix, Riyaziyyat və ya Coğrafiyadan çətin bir test sualı hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]")
        if "DOĞRU:" in res:
            try:
                st.session_state.current_test = {
                    "s": res.split("SUAL:")[1].split("A)")[0].strip(),
                    "v": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                    "c": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                    "i": res.split("İZAH:")[1].strip()
                }
            except: pass

    if st.button("Yeni Sual 🔄") or st.session_state.current_test is None:
        generate_new_question()

    if st.session_state.current_test:
        q = st.session_state.current_test
        st.markdown(f"<div class='card'><h4>{q['s']}</h4></div>", unsafe_allow_html=True)
        ans = st.radio("Variant seç:", q['v'], index=None)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Yoxla"):
            if ans and ans[0] == q['c']:
                st.success(f"Mükəmməl! {q['i']}")
                st.balloons()
            else: st.error(f"Səhv! Doğru cavab: {q['c']}. {q['i']}")
        
        if c2.button("Növbəti Sual ➡️"):
            generate_new_question()
            st.rerun()

# --- 🎮 OYUN & YARIŞMA (COĞRAFİYA VƏ BAYRAQLAR) ---
elif choice == "🎮 Oyun & Yarışma":
    st.title("🎲 AZ AI Yarışma Meydanı")
    game_type = st.radio("Oyun növü:", ["🚩 Bayraqları Tanı", "🏙️ Paytaxt Dueli", "🤝 Online Yarışma (Simulyasiya)"], horizontal=True)
    
    if game_type == "🚩 Bayraqları Tanı":
        countries = ["Azerbaijan", "Turkey", "Germany", "Japan", "Brazil", "Norway", "Canada", "Egypt"]
        target = random.choice(countries)
        st.subheader("Bu hansı ölkənin bayrağıdır?")
        st.image(f"https://flagcdn.com/w640/{target[:2].lower() if target != 'Azerbaijan' else 'az'}.png", width=300)
        
        options = random.sample(countries, 4)
        if target not in options: options[0] = target
        random.shuffle(options)
        
        user_choice = st.selectbox("Ölkəni seç:", options)
        if st.button("Təsdiqlə 🎯"):
            if user_choice == target:
                st.success("DOĞRUDUR! +50 XP")
            else: st.error(f"SƏHV! Bu {target} bayrağı idi.")

    elif game_type == "🤝 Online Yarışma (Simulyasiya)":
        st.warning("Canlı rəqib axtarılır...")
        time.sleep(2)
        st.info("Rəqib tapıldı: User_99 (Level 5)")
        st.write("**Sual:** Dünyanın ən böyük adası hansıdır?")
        st.text_input("Cavabın:")
        st.button("Rəqibi Qabaqla! ⚡")

# --- ⚙️ ADMIN AYARLARI (YALNIZ SAHİB ÜÇÜN) ---
elif choice == "⚙️ Admin Ayarları":
    if st.session_state.role != "admin":
        st.error("Giriş rədd edildi! Bu bölmə yalnız Sultan/Sahib üçündür.")
    else:
        st.title("👑 Sahibin İdarəetmə Paneli")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Sistem Statistikası")
        st.write(f"Aktiv API: {len(active_keys)}")
        st.write(f"İstifadəçi: {st.session_state.user}")
        
        st.divider()
        st.write("🔧 **Sistem Parametrləri**")
        st.toggle("AI-nın yaradıcılığını artır", value=True)
        st.toggle("Bütün şagirdlərə bildiriş göndər")
        if st.button("Bütün Keşləri Təmizlə"): st.success("Sistem təmizləndi!")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("🇦🇿 AZ AI | Bütün hüquqlar Sahveren tərəfindən qorunur 2026")
