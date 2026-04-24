import streamlit as st
from groq import Groq
import random
import time

# 1. Professional Portal Konfiqurasiyası
st.set_page_config(page_title="AZ AI | Universal Təhsil Portalı", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    /* Google Style Design */
    .stApp { background-color: #ffffff; color: #202124; }
    .main-card { border: 1px solid #dadce0; padding: 30px; border-radius: 8px; max-width: 450px; margin: auto; text-align: center; }
    .nav-box { background: #f8f9fa; border-radius: 15px; padding: 20px; border: 1px solid #dee2e6; margin-bottom: 10px; }
    .premium-tag { background: linear-gradient(45deg, #f1c40f, #f39c12); color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .stButton>button { border-radius: 5px; font-weight: 500; }
    .sidebar-content { background: #f1f3f4; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI & Səs Funksiyası
def get_az_ai_pro(prompt, voice=False):
    keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
    client = Groq(api_key=random.choice(keys))
    # Kişi səsi tərzi üçün sistem təlimatı
    system_msg = "Sən professional kişisən, ciddi və səsli izah verirmiş kimi danışırsan." if voice else "Sən dahi AZ AI-san."
    resp = client.chat.completions.create(
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    return resp.choices[0].message.content

# 3. Sessiya
if 'auth' not in st.session_state: st.session_state.auth = False

# --- GOOGLE GİRİŞ SİSTEMİ ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
            <div class="main-card">
                <h1 style="color:#4285F4">G<span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span>g<span style="color:#34A853">l</span>e</h1>
                <h3>Hesab seçin</h3>
                <p>AZ AI tətbiqinə keçid üçün</p>
                <hr>
                <div style="text-align:left; padding:10px; border-bottom:1px solid #eee; cursor:pointer;">
                    <b>👤 Sahveren Balayev</b><br><small>sahveren@gmail.com</small>
                </div>
                <div style="text-align:left; padding:10px; color:#1a73e8; cursor:pointer;">
                     başka bir hesap kullan
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Sahveren olaraq davam et"):
                st.session_state.auth = True
                st.session_state.user = "Sahveren"
                st.rerun()
    st.stop()

# --- SİSTEMİN DAXİLİ ---
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.title("🌐 AZ AI PORTAL")
    st.write(f"Xoş gəldin, **{st.session_state.user}**")
    st.markdown("<span class='premium-tag'>PREMIUM V.I.P</span>", unsafe_allow_html=True)
    st.divider()
    menu = st.selectbox("Xana seçin:", ["🏠 Ana Səhifə", "🌎 Dil Mərkəzi", "🎮 Oyunlar & Yarışma", "📁 Fayl Analizi (PDF/IMG)", "⚙️ Sultan Ayarları"])
    st.markdown("</div>", unsafe_allow_html=True)

# --- 🌎 DİL MƏRKƏZİ (YENİ) ---
if menu == "🌎 Dil Mərkəzi":
    st.title("🗣️ Beynəlxalq Dil Öyrənmə")
    lang = st.selectbox("Dil seçin:", ["İngilis", "Rus", "Alman", "Fransız", "Ərəb", "Çin"])
    word = st.text_input(f"{lang} dilində öyrənmək istədiyiniz söz və ya cümlə:")
    
    col_a, col_b, col_c = st.columns(3)
    if col_a.button("📖 Yazılış və Oxunuş"):
        res = get_az_ai_pro(f"{word} sözünün {lang} dilində yazılışını, transkripsiyasını və oxunuş qaydasını yaz.")
        st.info(res)
    
    if col_b.button("🔄 Tərcümə Et"):
        res = get_az_ai_pro(f"{word} sözünü {lang} dilindən Azərbaycancaya tərcümə et və nümunə cümlə qur.")
        st.success(res)
        
    if col_c.button("🔊 Sesli Tercüme"):
        with st.spinner("AI Səsləndirir..."):
            res = get_az_ai_pro(f"Sən bir kişisən. Bu sözü səsli şəkildə izah edirmiş kimi tərcümə et: {word}", voice=True)
            st.markdown(f"**📢 [Sesli Tercüme]:** {res}")

# --- 🎮 OYUNLAR XANASI ---
elif menu == "🎮 Oyunlar & Yarışma":
    st.title("🕹️ Fənlər Üzrə Oyunlar")
    game = st.tabs(["🚩 Coğrafiya", "🔢 Riyaziyyat", "📚 Dil Oyunları"])
    
    with game[0]:
        st.subheader("Dünya Bayraqları")
        st.image("https://flagcdn.com/w320/tr.png")
        st.button("Bu hansı ölkədir?")
        
    with game[1]:
        st.subheader("Sürətli Hesablama")
        st.write("25 * 4 + 15 = ?")
        st.text_input("Cavabın:")
        
    with game[2]:
        st.subheader("Söz Tapmacası")
        st.write("A _ _ R B _ _ C _ N")
        st.button("Tap 🎯")

# --- 📁 FAYL ANALİZİ ---
elif menu == "📁 Fayl Analizi (PDF/IMG)":
    st.title("📄 Sənəd və Şəkil Oxuyucu")
    st.info("PDF, Şəkil və ya Konspektləri bura yükləyin, AZ AI onları analiz etsin.")
    up_file = st.file_uploader("Fayl seçin (PDF, JPG, PNG)", type=["pdf", "jpg", "png"])
    if up_file:
        st.success(f"{up_file.name} uğurla yükləndi. Analiz üçün abunəlik tələb olunur.")

# --- ⚙️ SULTAN AYARLARI ---
elif menu == "⚙️ Sultan Ayarları":
    st.title("👑 Sultan Paneli")
    st.metric("Ümumi Qazanc", "1,200 AZN")
    st.metric("İzləyici Sayı", "4,500 nəfər")
    st.divider()
    st.write("🛠️ **Sistem İdarəetməsi**")
    st.checkbox("Premium abunəliyi aktiv et", value=True)
    st.checkbox("Google Login tələb et", value=True)

st.markdown("---")
st.caption("© 2026 AZ AI Portal | Bütün hüquqlar Sahveren tərəfindən qorunur")
