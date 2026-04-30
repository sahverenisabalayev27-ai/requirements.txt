import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: MASTER KOD (STABİL VERSİYA) ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="centered")

# CSS - Səliqəli dizayn
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF4B4B, #822727); 
        color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; 
    }
    </style>
    """, unsafe_allow_html=True)

# Sənin yeni API açarın birbaşa kodun daxilindədir
API_KEY = "AIzaSyC7wDpM8DYAFzgGmMyoQxrmaC_Zk0KSOC8"

try:
    # Google AI konfiqurasiyası
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("💎 Sultan AI: Rəqəmsal İmperiya")
    st.markdown("---")

    # Əsas Menyu
    menu = st.selectbox("Bir xidmət seçin:", ["📢 Reklam Yazarı", "🛠️ Texniki Usta", "🖼️ Zəka Dizayn (Prompt)", "💼 QR Generator"])

    if menu == "📢 Reklam Yazarı":
        st.subheader("Reklam Mətni Hazırla")
        prod = st.text_input("Məhsul və ya xidmət adı:")
        if st.button("Reklamı Yarat"):
            with st.spinner("Sultan AI düşünür..."):
                res = model.generate_content(f"{prod} üçün cəlbedici Instagram reklam mətni və hashtaglar yaz.")
                st.success("Hazırdır:")
                st.write(res.text)

    elif menu == "🛠️ Texniki Usta":
        st.subheader("Texniki Usta Dəstəyi")
        prob = st.text_area("Problemi təsvir edin (məs: kombi işləmir):")
        if st.button("Həll Yolunu Tap"):
            with st.spinner("Usta analiz edir..."):
                res = model.generate_content(f"Peşəkar usta kimi bu problemi addım-addım həll et: {prob}")
                st.info(res.text)

    elif menu == "🖼️ Zəka Dizayn (Prompt)":
        st.subheader("AI Şəkil üçün Professional Prompt")
        idea = st.text_input("Şəkil ideyanız nədir?")
        if st.button("Promptu Hazırla"):
            with st.spinner("Dizayn təlimatı hazırlanır..."):
                res = model.generate_content(f"'{idea}' üçün 3D hiper-realistik, cinematic və detallı AI image promptu yaz.")
                st.code(res.text)

    elif menu == "💼 QR Generator":
        st.subheader("Sürətli QR Kod")
        link = st.text_input("Link və ya mətn daxil edin:")
        if st.button("QR Kod Yaradın"):
            qr_img = qrcode.make(link)
            buf = BytesIO()
            qr_img.save(buf)
            st.image(buf, caption="Sizin QR Kodunuz")

except Exception as e:
    st.error(f"Sistemdə kiçik bir problem yarandı: {e}")
    st.info("Zəhmət olmasa, tətbiqi 'Reboot' edin.")
