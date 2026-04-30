import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: YENİLƏNMİŞ MASTER KOD ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# Sənin yeni API açarın bura yerləşdirildi
API_KEY = "AIzaSyD0_EWzOr1ZAQj3JXkdsJCfVQbom_n6Qm0"

# Stil tənzimləmələri
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF4B4B, #822727); 
        color: white; border-radius: 12px; border: none; font-weight: bold; width: 100%; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

try:
    # Google AI aktivasiyası
    genai.configure(api_key=API_KEY.strip())
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.sidebar.title("💎 SULTAN AI")
    st.sidebar.success("Sistem Aktivdir")
    
    menu = st.sidebar.selectbox("Bölməni Seçin:", ["🏠 Ana Səhifə", "📢 Reklam Yazarı", "🛠️ Texniki Usta", "💼 QR Generator"])

    if menu == "🏠 Ana Səhifə":
        st.title("Sultan AI: Milli Portal 🇦🇿")
        st.info("Zəka Təsvirləri vizyonu ilə hazırlanmış universal süni zəka sistemi.")
        st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995", caption="Gələcəyi Sultan AI ilə qurun")

    elif menu == "📢 Reklam Yazarı":
        st.header("📢 Reklam Mərkəzi")
        prod = st.text_input("Məhsul və ya xidmət adı:")
        if st.button("Reklamı Hazırla"):
            with st.spinner("AI reklam yazır..."):
                res = model.generate_content(f"{prod} üçün cəlbedici reklam mətni yaz.")
                st.success("Nəticə:")
                st.write(res.text)

    elif menu == "🛠️ Texniki Usta":
        st.header("🛠️ Texniki Usta")
        prob = st.text_area("Problemi təsvir edin:")
        if st.button("Həll Yolunu Tap"):
            with st.spinner("Usta düşünür..."):
                res = model.generate_content(f"Peşəkar usta kimi bu problemi həll et: {prob}")
                st.info(res.text)

    elif menu == "💼 QR Generator":
        st.header("💼 QR Kod")
        link = st.text_input("Link daxil edin:")
        if st.button("QR Yarat"):
            qr_img = qrcode.make(link)
            buf = BytesIO()
            qr_img.save(buf)
            st.image(buf, caption="Sizin QR Kodunuz")

except Exception as e:
    st.error(f"Sistem xətası: {e}")
    st.info("Zəhmət olmasa, tətbiqi 'Reboot' edin və ya yeni açarı yoxlayın.")
