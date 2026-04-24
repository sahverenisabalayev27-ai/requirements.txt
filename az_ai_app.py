import streamlit as st
from groq import Groq
import random
import pandas as pd

# 1. GOOGLE ÜÇÜN SEO VƏ SAYT AYARLARI (İndi hər şey bir yerdə)
st.set_page_config(
    page_title="AZ AI | Azərbaycanın Süni İntellekt Təhsil Portalı", 
    page_icon="🇦🇿", 
    layout="wide"
)

# Google Botları üçün Meta Tag-lar (SEO üçün bu vacibdir)
st.markdown("""
    <head>
        <meta name="description" content="AZ AI - Azərbaycanın süni intellekt əsaslı təhsil platforması.">
        <meta name="keywords" content="AZ AI, Sahveren, Süni İntellekt Azərbaycan, Bayraq oyunu, Onlayn təhsil">
    </head>
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .premium-box { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
        color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: bold;
    }
    .admin-card { background: #1e1b4b; border: 2px solid #4338ca; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Engine Konfiqurasiyası
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def get_az_ai(prompt):
    if not active_keys: return "Sistem xətası: API açarları yoxdur."
    try:
        client = Groq(api_key=random.choice(active_keys))
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən AZ AI-san. Çox dərin və professional izahlar verirsən."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=4000
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Xəta baş verdi: {e}"

# 3. Sessiya (Yaddaş)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_premium' not in st.session_state: st.session_state.is_premium = False
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- GİRİŞ PORTALI ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI Giriş</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("İstifadəçi adı:")
        p = st.text_input("Şifrə:", type="password")
        if st.button("Sistemə Qoşul 🔓"):
            if u == "admin" and p == "sahveren2026":
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", "Sahveren"
                st.rerun()
            elif u and p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "user", u
                st.rerun()
    st.stop()

# --- SIDEBAR NAVİQASİYA ---
with st.sidebar:
    st.title("🇦🇿 AZ AI")
    st.write(f"Salam, **{st.session_state.user}**")
    if st.session_state.is_premium:
        st.success("✨ PREMIUM ÜZV")
    st.divider()
    menu = st.radio("Bölmələr:", ["📚 Tədris", "🚩 Bayraq Oyunu", "💎 Premium", "⚙️ Ayarlar"])
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 📚 TƏDRİS BÖLMƏSİ ---
if menu == "📚 Tədris":
    st.title("📖 Tədris Portalı")
    topic = st.text_input("Hansı mövzunu öyrənmək istəyirsən?", "Dədə Qorqud dastanı")
    if st.button("Dərsi Hazırla 🚀"):
        with st.spinner("AZ AI araşdırır..."):
            res = get_az_ai(f"'{topic}' haqqında geniş akademik məlumat ver.")
            st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

# --- 🚩 OYUNLAR ---
elif menu == "🚩 Bayraq Oyunu":
    st.title("🌍 Bayraqları Tanı")
    st.write("XP-ni artırmaq üçün ölkələri tap!")
    st.image("https://flagcdn.com/w320/az.png") # Nümunə olaraq Azərbaycan
    ans = st.text_input("Bu hansı ölkədir?")
    if st.button("Yoxla"):
        if ans.lower() == "azərbaycan":
            st.success("DOĞRU! +20 XP")
            st.session_state.xp += 20
        else: st.error("Səhvdir!")

# --- 💎 PREMIUM (ÖDƏNİŞ) ---
elif menu == "💎 Premium":
    st.title("✨ AZ AI Premium")
    st.markdown("""
    <div class='premium-box'>
        <h2>Aylıq cəmi 5 AZN</h2>
        <p>Limitsiz AI sualları və xüsusi dərslər!</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("Kart məlumatlarını daxil edərək abunə ola bilərsiniz (Simulyasiya):")
    st.text_input("Kart Nömrəsi:")
    if st.button("Ödənişi Tamamla ✨"):
        st.session_state.is_premium = True
        st.success("Təbriklər, Premium aktiv edildi!")

# --- ⚙️ AYARLAR VƏ ADMIN PANEL ---
elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Ayarlar")
    st.write("Dil və interfeys seçimlərini buradan edin.")
    st.selectbox("Sistem dili:", ["Azərbaycan", "English"])
    
    # YALNIZ SƏNİN ÜÇÜN (ADMIN)
    if st.session_state.role == "admin":
        st.divider()
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.subheader("👑 SULTAN İDARƏETMƏ")
        st.write(f"Toplanmış XP (Ümumi): {st.session_state.xp}")
        st.write("📊 **Statistika:**")
        st.table(pd.DataFrame({"İzləyici": [1250], "Qazanc": ["425 AZN"]}))
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"© 2026 AZ AI | Sahveren Premium Edition")
