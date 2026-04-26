import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- SAYTIN AYARLARI ---
st.set_page_config(page_title="Sultan Business AI", layout="wide", page_icon="💎")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .biznes-qutu { border: 2px solid #7c3aed; padding: 20px; border-radius: 15px; background: #0d1117; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (BİZNES MENYU) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=80)
    st.title("Sultan AI Hub")
    choice = st.radio("İdarəetmə Paneli:", [
        "🏢 Biznes Dashboard", 
        "🧠 Satış Analizi (Beyin)", 
        "📊 Maliyyə Planlayıcı", 
        "📝 Reklam Generatoru"
    ])

# --- 1. BİZNES DASHBOARD (Göstəricilər) ---
if choice == "🏢 Biznes Dashboard":
    st.markdown("<h1>🏢 Biznes İdarəetmə Mərkəzi</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aylıq Hədəf", "5,000 AZN", "+12%")
    col2.metric("Müştəri Sayı", "142", "yeni")
    col3.metric("Reklam Xərci", "450 AZN", "-5%")
    col4.metric("Xalis Mənfəət", "2,100 AZN", "稳定")

    st.write("### 📈 Satışın Artım Dinamikası")
    chart_data = pd.DataFrame({
        'Ay': ['Yanvar', 'Fevral', 'Mart', 'Aprel'],
        'Satış': [1200, 1800, 1500, 2100]
    })
    fig = px.line(chart_data, x='Ay', y='Satış', markers=True, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 2. SATIŞ ANALİZİ (ƏSL BEYİN) ---
elif choice == "🧠 Satış Analizi (Beyin)":
    st.title("🧠 AI Müştəri Analizatoru")
    st.write("Müştərinin mesajını yazın, AI onun psixologiyasını analiz etsin.")
    
    user_text = st.text_area("Müştəri nə yazır?", placeholder="Məsələn: Qiymət çox bahadır, endirim mümkündür?")
    
    if st.button("Analiz Et"):
        if user_text:
            with st.spinner("Beyin analiz aparır..."):
                # Real məntiq:
                text_lower = user_text.lower()
                if "bahadır" in text_lower or "qiymət" in text_lower:
                    st.error("⚠️ ETİRAZ: Müştəri qiymətə ilişib.")
                    st.info("💡 MƏSLƏHƏT: Qiyməti deyil, məhsulun ona qazandıracağı vaxtı və keyfiyyəti vurğulayın.")
                elif "zəmanət" in text_lower or "güvən" in text_lower:
                    st.warning("⚠️ ŞÜBHƏ: Müştəri güvən istəyir.")
                    st.info("💡 MƏSLƏHƏT: Ona əvvəlki müştəri rəylərini və geri qaytarma şərtlərini göndərin.")
                else:
                    st.success("✅ MARAQ: Müştəri məhsulla maraqlanır.")
                    st.info("💡 MƏSLƏHƏT: Onu tələsdirmək üçün 'Məhdud sayda qaldı' taktikasını işlədin.")
        else:
            st.error("Zəhmət olmasa mətn daxil edin.")

# --- 3. MALİYYƏ PLANLAYICI ---
elif choice == "📊 Maliyyə Planlayıcı":
    st.title("📊 Gəlir və Xərc Hesablayıcı")
    
    with st.container():
        st.write("Aylıq xərclərinizi daxil edin:")
        office = st.number_input("Ofis/Server xərci:", value=50)
        ads = st.number_input("Reklam büdcəsi:", value=200)
        other = st.number_input("Digər xərclər:", value=100)
        
        total_cost = office + ads + other
        target_income = st.slider("Hədəf Gəlir (AZN):", 500, 10000, 2000)
        
        if st.button("Hesabla"):
            net_profit = target_income - total_cost
            st.markdown(f"<div class='biznes-qutu'><h2>Xalis Mənfəət: {net_profit} AZN</h2></div>", unsafe_allow_html=True)
            if net_profit > 1000:
                st.balloons()

# --- 4. REKLAM GENERATORU ---
elif choice == "📝 Reklam Generatoru":
    st.title("📝 Universal Reklam Yazarı")
    biz_name = st.text_input("Biznesin adı:")
    offer = st.text_input("Kampaniya (Məsələn: 20% Endirim):")
    
    if st.button("Reklam Mətnləri Yarat"):
        st.subheader("🚀 Instagram/Facebook Üçün:")
        st.code(f"🔥 ŞOK KAMPANİYA! {biz_name} təqdim edir: {offer}!\n🎯 Keyfiyyətli seçim, münasib qiymət.\n📦 Sifariş üçün DM!")
        
        st.subheader("✈️ Telegram/WhatsApp Üçün:")
        st.code(f"📢 DİQQƏT: {biz_name}-da {offer} başladı! Məhdud zaman, qaçırmayın! 🏃💨")
