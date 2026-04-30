import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: MASTER KOD (SMART MODEL SELECTION) ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF4B4B, #822727); 
        color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; 
    }
    </style>
    """, unsafe_allow_html=True)

# Sənin yeni API açarın
API_KEY = "AIzaSyC7wDpM8DYAFzgGmMyoQxrmaC_Zk0KSOC8"

model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        # Yoxlanılacaq model adları siyahısı
        possible_models = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']
        
        # İlk işləyən modeli tapana qədər dövr edirik
        for model_name in possible_models:
            try:
                temp_model = genai.GenerativeModel(model_name)
                # Kiçik bir test sorğusu edirik
                temp_model.generate_content("hi", generation_config={"max_output_tokens": 1})
                model = temp_model
                break # İşləyən model tapıldısa, dövrdən çıxırıq
            except:
                continue
        
        if model is None:
            st.error("Xəta: Hazırda bu API Key üçün heç bir model (Flash və ya Pro) əlçatan deyil. Lütfən 10 dəqiqə sonra yenidən yoxlayın.")

    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")

if model:
    st.title("💎 Sultan AI: Rəqəmsal İmperiya")
    st.markdown("---")

    menu = st.selectbox("Bir xidmət seçin:", ["📢 Reklam Yazarı", "🛠️ Texniki Usta", "🖼️ Zəka Dizayn (Prompt)", "💼 QR Generator"])

    if menu == "📢 Reklam Yazarı":
        st.subheader("Reklam Mətni Hazırla")
        prod = st.text_input("Məhsul və ya xidmət adı (Məsələn: Quba Turu):")
        if st.button("Reklamı Yarat"):
            with st.spinner("Sultan AI düşünür..."):
                res = model.generate_content(f"{prod} üçün maraqlı reklam mətni yaz.")
                st.success("Hazırdır:")
                st.write(res.text)

    elif menu == "🛠️ Texniki Usta":
        st.subheader("Texniki Usta Dəstəyi")
        prob = st.text_area("Problemi yazın:")
        if st.button("Həll Yolunu Tap"):
            with st.spinner("Usta analiz edir..."):
                res = model.generate_content(f"Peşəkar usta kimi həll yaz: {prob}")
                st.info(res.text)

    elif menu == "🖼️ Zəka Dizayn (Prompt)":
        idea = st.text_input("Şəkil ideyanız:")
        if st.button("Promptu Hazırla"):
            res = model.generate_content(f"'{idea}' üçün 3D render promptu yaz.")
            st.code(res.text)

    elif menu == "💼 QR Generator":
        link = st.text_input("Link daxil edin:")
        if st.button("QR Kod Yaradın"):
            qr_img = qrcode.make(link)
            buf = BytesIO()
            qr_img.save(buf)
            st.image(buf)
