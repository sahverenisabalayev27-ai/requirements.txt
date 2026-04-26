import streamlit as st
import time

# --- SAYTIN KONFİQURASİYASI ---
st.set_page_config(page_title="Sultan Media AI", page_icon="🚀", layout="wide")

# --- CUSTOM CSS (PREMİUM GÖRÜNÜŞ) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #7c3aed;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #6d28d9; border: 1px solid white; }
    .biznes-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    h1, h2, h3 { color: #a78bfa !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (NAVİQASİYA) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6165/6165577.png", width=100)
    st.title("Sultan Media AI")
    st.markdown("---")
    choice = st.radio("Xidmətlər", ["📊 Dashboard", "✍️ AI Copywriter", "💰 Satış Artırımı", "📞 Dəstək"])
    st.markdown("---")
    st.info("Sultan Sahveren tərəfindən idarə olunur.")

# --- DASHBOARD ---
if choice == "📊 Dashboard":
    st.markdown("<h1 style='text-align: center;'>Xoş Gəldiniz, Sahveren! 🦾</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Biznesinizi AI ilə idarə etmək üçün mərkəzi panel.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="biznes-card"><h3>📈 Reytinq</h3><p>Aktiv istifadəçi: 0</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="biznes-card"><h3>💰 Qazanc</h3><p>Cəmi gəlir: 0 AZN</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="biznes-card"><h3>🤖 Status</h3><p>AI Model: Aktiv</p></div>', unsafe_allow_html=True)

    st.markdown("### 🛠️ Tez-tez istifadə olunanlar")
    if st.button("Yeni Kampaniya Başlat"):
        st.toast("Tezliklə aktiv olacaq!")

# --- AI COPYWRITER ---
elif choice == "✍️ AI Copywriter":
    st.title("✍️ AI Sosial Media Asistanı")
    st.write("Məhsul haqqında məlumat yazın, AI sizin üçün mükəmməl reklam mətni hazırlasın.")
    
    product_name = st.text_input("Məhsul və ya Xidmət adı:")
    features = st.text_area("Əsas özəlliklər (Məsələn: Pulsuz çatdırılma, 24/7 dəstək):")
    
    if st.button("Mətni Hazırla"):
        if product_name:
            with st.spinner("AI mətni hazırlayır..."):
                time.sleep(2)
                st.success("Mətn hazırdır!")
                st.code(f"🌟 {product_name.upper()} İLƏ TANIŞ OLUN! 🌟\n\n🎯 {features}\n\n✅ Keyfiyyət və Etibarın tək ünvanı.\n🚀 İndi sifariş verin, fürsəti qaçırmayın!\n\n📍 @sultan_media_ai\n#azərbaycan #biznes #ai #smm", language="markdown")
        else:
            st.error("Zəhmət olmasa məhsul adını qeyd edin.")

# --- SATIŞ ARTIRIMI ---
elif choice == "💰 Satış Artırımı":
    st.title("💰 Satış və Müştəri Psixologiyası")
    st.markdown("""
    Bu bölmədə AI sizə müştərilərlə necə danışmalı olduğunuzu öyrədir.
    1. Müştəri etirazlarını analiz edir.
    2. Qiymət təklifi strategiyası qurur.
    3. VIP müştəri profili yaradır.
    """)
    st.warning("Bu bölmə yalnız 'Premium' üzvlər üçündür.")
    if st.button("Premium Planı İndi Al (19 AZN)"):
        st.balloons()
        st.info("Ödəniş sistemi qoşulur...")

# --- DƏSTƏK ---
elif choice == "📞 Dəstək":
    st.title("📞 Əlaqə və Dəstək")
    st.write("Hər hansı bir sualınız və ya texniki probleminiz var?")
    with st.form("contact"):
        name = st.text_input("Adınız:")
        msg = st.text_area("Mesajınız:")
        if st.form_submit_button("Göndər"):
            st.success("Mesajınız Sahverenə göndərildi!")
