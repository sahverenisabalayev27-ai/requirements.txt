import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="Sultan AI | Universal Portal", page_icon="💎", layout="wide")

# --- CSS (MÜKƏMMƏL GÖRÜNÜŞ) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #FF4B4B, #822727); color: white; border-radius: 10px; border: none; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- API VƏ MODEL (XƏTASIZ VERSİYA) ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Sultan AI Key daxil edin:", type="password")

model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # ƏN STABİL MODEL ADLARI SİYAHISI
        # Əgər biri tapılmazsa, digərini yoxlayır
        for m_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(m_name)
                # Test sorğusu
                model.generate_content("hi")
                break
            except:
                continue
    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")

# --- MENYU ---
st.sidebar.title("💎 SULTAN AI")
menu = st.sidebar.selectbox("Bölməni Seçin:", ["🏠 Ana Səhifə", "📢 Reklam Mərkəzi", "👁️ Vision AI", "💼 QR Alətləri", "⚙️ Usta Dəstəyi"])

# --- FUNKSİYALAR ---
if menu == "🏠 Ana Səhifə":
    st.title("Sultan AI: Rəqəmsal İmperiya 🇦🇿")
    st.write("### Zəka Core vizyonu ilə hazırlanmış universal platforma.")
    st.info("İstədiyiniz bölməni soldan seçərək işinizi saniyələr içində həll edin.")

elif menu == "📢 Reklam Mərkəzi":
    st.header("📢 Reklam Hazırla")
    prod = st.text_input("Məhsulun adı:")
    target = st.text_input("Kimin üçün? (Hədəf kütlə):")
    if st.button("Kampaniya Yaradın"):
        if model:
            with st.spinner("Sultan AI hazırlayır..."):
                res = model.generate_content(f"{prod} üçün {target} kütləsinə uyğun 3 maraqlı reklam mətni yaz.")
                st.success(res.text)
        else:
            st.error("API Key daxil edilməyib və ya model tapılmadı.")

elif menu == "👁️ Vision AI":
    st.header("👁️ Universal Göz")
    file = st.camera_input("Şəkil çək")
    if file and model:
        img = Image.open(file)
        with st.spinner("Analiz edilir..."):
            res = model.generate_content(["Bu şəkli analiz et və təsvir ver.", img])
            st.write(res.text)

elif menu == "💼 QR Alətləri":
    st.header("💼 QR Generator")
    text = st.text_input("QR üçün məlumat:")
    if st.button("Yarat"):
        qr = qrcode.make(text)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf)

elif menu == "⚙️ Usta Dəstəyi":
    st.header("⚙️ Texniki Usta")
    prob = st.text_area("Problemi yazın:")
    if st.button("Həllini Tap"):
        if model:
            res = model.generate_content(f"Usta kimi bu problemi həll et: {prob}")
            st.write(res.text)
