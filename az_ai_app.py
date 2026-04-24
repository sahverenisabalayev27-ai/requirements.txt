import streamlit as st
from groq import Groq
import random
import pandas as pd
import time

# 1. AZ AI - Brendinq
st.set_page_config(page_title="AZ AI | Premium Təhsil", page_icon="🇦🇿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
    .premium-box { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
        color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: bold;
    }
    .stButton>button { border-radius: 10px; transition: 0.3s; }
    .admin-card { background: #1e1b4b; border: 2px solid #4338ca; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Engine
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def get_az_ai(prompt):
    if not active_keys: return "Sistem xətası."
    client = Groq(api_key=random.choice(active_keys))
    resp = client.chat.completions.create(
        messages=[{"role": "system", "content": "Sən AZ AI-san. Çox dərin və professional izahlar verirsən."},
                  {"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=4000
    )
    return resp.choices[0].message.content

# 3. Sessiya
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_premium' not in st.session_state: st.session_state.is_premium = False

# --- GİRİŞ ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🇦🇿 AZ AI Giriş</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("İstifadəçi:")
        p = st.text_input("Şifrə:", type="password")
        if st.button("Daxil Ol 🔓"):
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
    st.write(f"Salam, **{st.session_state.user}**")
    if st.session_state.is_premium:
        st.markdown("✨ **PREMIUM ÜZV**", unsafe_allow_html=True)
    
    menu = st.radio("Menyu:", ["📚 Dərslər", "🚩 Bayraq Oyunu", "💎 Premium Al", "⚙️ Ayarlar"])
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 📚 DƏRSLƏR ---
if menu == "📚 Dərslər":
    st.title("📖 Tədris Portalı")
    topic = st.text_input("Mövzu:", "Səfəvilər Dövləti")
    if st.button("Dərsi Hazırla 🚀"):
        with st.spinner("AZ AI yazır..."):
            res = get_az_ai(f"'{topic}' haqqında 4000 sözlük, mükəmməl akademik məqalə yaz.")
            st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

# --- 🚩 BAYRAQ OYUNU ---
elif menu == "🚩 Bayraq Oyunu":
    st.title("🌍 Bayraqları Tap")
    # Sadələşdirilmiş nümunə
    c_name = "Braziliya"
    st.image("https://flagcdn.com/w320/br.png")
    ans = st.text_input("Bu hansı ölkədir?")
    if st.button("Yoxla"):
        if ans.lower() == c_name.lower(): st.success("Doğru!")
        else: st.error("Səhv!")

# --- 💎 PREMIUM AL (ÖDƏNİŞ SİSTEMİ) ---
elif menu == "💎 Premium Al":
    st.title("✨ AZ AI Premium")
    st.markdown("""
    <div class='premium-box'>
        <h2>Aylıq cəmi 5 AZN</h2>
        <p>✅ Reklamsız təhsil</p>
        <p>✅ Limitsiz AI sualları</p>
        <p>✅ Şəxsi müəllim dəstəyi</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Ödəniş Üsulu")
    st.info("Hazırda ödənişlər test rejimindədir. Kart məlumatlarını daxil edin:")
    st.text_input("Kart nömrəsi (16 rəqəm):")
    col1, col2 = st.columns(2)
    col1.text_input("Tarix (MM/YY):")
    col2.text_input("CVV:")
    
    if st.button("Ödənişi Tamamla (5 AZN) 💳"):
        st.success("Təbriklər! Artıq Premium Üzvsünüz.")
        st.session_state.is_premium = True

# --- ⚙️ AYARLAR ---
elif menu == "⚙️ Ayarlar":
    st.title("⚙️ İstifadəçi Ayarları")
    st.write("Buradan profilinizi və dil seçimlərini tənzimləyə bilərsiniz.")
    st.selectbox("Sistem dili:", ["Azərbaycan", "English"])
    st.toggle("Gecə rejimi", value=True)
    
    # YALNIZ ADMIN ÜÇÜN GİZLİ BÖLMƏ
    if st.session_state.role == "admin":
        st.divider()
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.subheader("👑 SULTAN İDARƏETMƏ PANELİ")
        col_st1, col_st2 = st.columns(2)
        col_st1.metric("Ümumi İzləyici", "1,250 nəfər")
        col_st2.metric("Aylıq Qazanc", "425 AZN")
        
        st.write("🔍 **Son Ödənişlər:**")
        pay_data = pd.DataFrame({
            "İstifadəçi": ["User_12", "Ali_99", "Aysel_M"],
            "Məbləğ": ["5 AZN", "5 AZN", "5 AZN"],
            "Tarix": ["24.04.2026", "23.04.2026", "23.04.2026"]
        })
        st.table(pay_data)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 AZ AI | Sahveren Premium Edition")
