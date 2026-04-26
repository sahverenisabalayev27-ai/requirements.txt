import streamlit as st
import time
import random

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Sultan Media AI | Omni-Channel", page_icon="🌐", layout="wide")

# --- CUSTOM CSS (ULTRA MODERN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background: #05070a; color: white; }
    .main-header {
        font-family: 'Orbitron', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px;
        text-align: center;
        font-weight: bold;
    }
    .platform-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
        text-align: center;
    }
    .platform-card:hover {
        background: rgba(124, 58, 237, 0.1);
        border-color: #7c3aed;
        transform: scale(1.02);
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background: linear-gradient(90deg, #7c3aed 0%, #f472b6 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>SULTAN AI</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.selectbox("🎯 PLATFORMA SEÇİN", [
        "🏠 Ana Səhifə",
        "📸 Instagram & TikTok",
        "🎥 YouTube (Shorts & Long)",
        "💼 LinkedIn & Facebook",
        "✈️ Telegram Kanal İdarəçisi",
        "💎 Sultan Premium"
    ])
    st.write("---")
    st.success("Sistem: 100% Aktiv")

# --- ANA SƏHİFƏ ---
if menu == "🏠 Ana Səhifə":
    st.markdown('<p class="main-header">SULTAN MEDIA AI</p>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Bütün Sosial Media Platformalarını Tək Mərkəzdən İdarə Edin</h3>", unsafe_allow_html=True)
    
    st.write("##")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="platform-card"><h1>📱</h1><h4>Instagram</h4><p>Reels və Postlar</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="platform-card"><h1>🎬</h1><h4>TikTok</h4><p>Viral Trendlər</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="platform-card"><h1>📺</h1><h4>YouTube</h4><p>SEO və Skriptlər</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="platform-card"><h1>💼</h1><h4>Business</h4><p>Facebook & Ads</p></div>', unsafe_allow_html=True)

# --- INSTAGRAM & TIKTOK ---
elif menu == "📸 Instagram & TikTok":
    st.title("📸 Qısa Video (Reels/TikTok) Generatoru")
    topic = st.text_input("Videonun mövzusu:")
    duration = st.slider("Video müddəti (saniyə):", 15, 60, 30)
    
    if st.button("Viral Ssenari Yarat"):
        with st.spinner("Alqoritm analiz edilir..."):
            time.sleep(2)
            st.subheader("🔥 Sizin Viral Planınız:")
            st.info(f"**Hook:** '{topic}' haqqında bunu bilsəniz şok olarsınız!")
            st.write("**Görüntü:** Sürətli keçidlər, alt yazı mərkəzdə.")
            st.code(f"Hashtaglar: #sultanai #{topic.replace(' ','')} #trend #azərbaycan")

# --- YOUTUBE ---
elif menu == "🎥 YouTube (Shorts & Long)":
    st.title("🎥 YouTube SEO & Content Generator")
    video_type = st.radio("Video növü:", ["Shorts (Qısa)", "Long Form (Uzun video)"])
    title_req = st.text_input("Mövzu başlığı yazın:")
    
    if st.button("YouTube Planını Hazırla"):
        st.write("### ✅ AI Təklifləri:")
        st.write(f"**Başlıq:** {title_req} - Heç Kimin Bilmədiyi 5 Sirr!")
        st.write("**Açıqlama:** Bu videoda biz {title_req} mövzusunu dərindən araşdırırıq...")
        st.warning("Yüksək Click-Through Rate (CTR) üçün parlaq rəngli thumbnail istifadə edin!")

# --- TELEGRAM ---
elif menu == "✈️ Telegram Kanal İdarəçisi":
    st.title("✈️ Telegram Kanal Avtomatlaşdırması")
    channel_type = st.selectbox("Kanalın növü:", ["Xəbər", "Eğlence", "Biznes/Motivasiya"])
    
    if st.button("Həftəlik Post Planı Yarat"):
        days = ["Bazar ertəsi", "Çərşənbə", "Cümə"]
        for day in days:
            st.markdown(f"""
            **{day}:**
            - Saat 10:00: {channel_type} haqqında maraqlı fakt.
            - Saat 18:00: İnteraktiv sorğu (Poll).
            """)

# --- PREMIUM ---
elif menu == "💎 Sultan Premium":
    st.markdown("<h1 style='text-align: center; color: #f472b6;'>💎 SULTAN PRO MEMBERSHIP</h1>", unsafe_allow_html=True)
    st.write("### Niyə Pro-ya keçməlisiniz?")
    st.write("- 🚀 Bütün platformalar üçün limitsiz AI sorğuları")
    st.write("- 📊 Rəqib analizi (Rəqibləriniz nə paylaşır?)")
    st.write("- 📞 24/7 Sultan Dəstək Xətti")
    
    st.write("---")
    st.button("İNDİ ABUNƏ OL (Cəmi 19.99 AZN)")
