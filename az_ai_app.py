import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont

# --- SAYTIN AYARLARI ---
st.set_page_config(page_title="Sultan Business AI", layout="wide", page_icon="💎")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    .card {
        background: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #a78bfa !important; }
    .stButton>button {
        background: linear-gradient(90deg, #7c3aed, #db2777);
        color: white; border: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (SULTAN MENU) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=80)
    st.title("Sultan AI Hub")
    menu = st.selectbox("Xidmət Seçin:", [
        "🏢 Biznes Dashboard",
        "💈 Reklam & Brendinq (Logo)",
        "📸 Sosial Media Generatoru",
        "🧠 Müştəri Analizi"
    ])

# --- 1. BİZNES DASHBOARD ---
if menu == "🏢 Biznes Dashboard":
    st.title("🏢 Müəssisənin İdarəetmə Paneli")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gəlir Hədəfi", "3,500 AZN")
    col2.metric("Aktiv Müştəri", "85")
    col3.metric("Reklam Effekti", "88%")
    
    st.write("### 📈 Satış Analitikası")
    df = pd.DataFrame({'Həftə': ['1', '2', '3', '4'], 'Qazanc': [400, 700, 600, 950]})
    fig = px.bar(df, x='Həftə', y='Qazanc', template="plotly_dark", color_discrete_sequence=['#7c3aed'])
    st.plotly_chart(fig, use_container_width=True)

# --- 2. REKLAM & BRENDİNQ (LOGO) ---
elif menu == "💈 Reklam & Brendinq (Logo)":
    st.title("💈 Biznesin Üçün Reklam Yaradıcı")
    st.write("Məsələn: Bərbər, Kafe və ya Sürücü üçün avtomatik dizayn.")
    
    biz_type = st.selectbox("Sizin Biznesiniz:", ["Bərbərxana", "Restoran", "Gözəllik Salonu", "Mağaza"])
    biz_name = st.text_input("Müəssisənin Adı:", "Sultan Style")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🖼️ Avtomatik Logo")
        if st.button("Loqonu Hazırla"):
            # Sadə Loqo Simulyasiyası
            img = Image.new('RGB', (400, 200), color = (22, 27, 34))
            d = ImageDraw.Draw(img)
            d.rectangle([20, 20, 380, 180], outline="#7c3aed", width=5)
            d.text((100, 80), biz_name.upper(), fill=(255, 255, 255))
            st.image(img, caption="Sizin Yeni Loqonuz (Konsept)")
            st.success("Dizayn AI tərəfindən hazırlandı!")

    with col2:
        st.subheader("📢 Reklam Banneri")
        slogan = st.text_input("Şüarınız:", "Keyfiyyətin tək ünvanı!")
        if st.button("Banner Mətni Yarat"):
            st.info(f"📍 Məkan: {biz_name}\n✂️ Xidmət: {biz_type}\n🔥 {slogan}\n📞 Sifariş üçün: 055-XXX-XX-XX")

# --- 3. SOSİAL MEDİA GENERATORU ---
elif menu == "📸 Sosial Media Generatoru":
    st.title("📸 Omni-Channel Media AI")
    platform = st.multiselect("Platformaları seçin:", ["Instagram", "TikTok", "YouTube", "Facebook"])
    topic = st.text_input("Postun mövzusu:", "Böyük Endirim Başladı!")
    
    if st.button("Postları və Hashtagları Yarat"):
        st.divider()
        for p in platform:
            st.subheader(f"✅ {p} üçün təklif:")
            if p == "Instagram":
                st.write(f"📸 **Post:** {topic}. Şəkil: Parlaq və yüksək keyfiyyətli. #azərbaycan #biznes #baku")
            elif p == "TikTok":
                st.write(f"🎥 **Video:** {topic} ssenarisi: 5 saniyəlik 'Hook' ilə başlayın. #trend #viral")
            elif p == "YouTube":
                st.write(f"📺 **Shorts:** SEO Başlıq: {topic} (Sirlər açıqlanır!)")

# --- 4. MÜŞTƏRİ ANALİZİ ---
elif menu == "🧠 Müştəri Analizi":
    st.title("🧠 Satış Psixologiyası Modulu")
    msg = st.text_area("Müştərinin mesajını bura qoyun:")
    if st.button("Mesajı Analiz Et"):
        if "qiymət" in msg.lower():
            st.error("⚠️ Müştəri qiymətdən narazıdır. Ona hədiyyə və ya xidmət müddətini vurğulayın.")
        else:
            st.success("✅ Müştəri maraqlıdır. Ona dərhal rezervasiya təklif edin!")
