import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="Sultan AI | Universal Portal", page_icon="💎", layout="wide")

# --- CSS (PREMİUM GÖRÜNÜŞ) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #FF4B4B, #822727); color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- API VƏ MODEL (ZİREHLİ MƏNTİQ) ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Sultan AI Key daxil edin:", type="password")

model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        # Bütün mümkün model adlarını siyahıya alırıq
        model_names = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']
        
        # Hansı model işləsə, onu seçirik
        for name in model_names:
            try:
                test_model = genai.GenerativeModel(name)
                # Kiçik bir test sorğusu edirik
                test_model.generate_content("test", generation_config={"max_output_tokens": 1})
                model = test_model
                break # İşləyən modeli tapdıqsa dayanırıq
            except:
                continue
                
        if model is None:
            st.error("Xəta: Google heç bir modelə icazə vermir. API Key-i Google AI Studio-da yenidən yaradın.")
    except Exception as e:
        st.error(f"Sistem xətası: {e}")

# --- MENYU ---
st.sidebar.title("💎 SULTAN AI")
menu = st.sidebar.selectbox("Bölməni Seçin:", ["🏠 Ana Səhifə", "📢 Reklam Mərkəzi", "👁️ Vision AI", "💼 QR Generator", "⚙️ Usta Dəstəyi"])

# --- FUNKSİYALAR ---
if menu == "🏠 Ana Səhifə":
    st.title("Sultan AI: Rəqəmsal İmperiya 🇦🇿")
    st.info("Zəka Core vizyonu ilə hazırlanmış universal platforma.")
    st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995", caption="Zəka Təsvirləri")

elif menu == "📢 Reklam Mərkəzi":
    st.header("📢 Reklam Hazırla")
    prod = st.text_input("Məhsul adı:")
    target = st.text_input("Hədəf kütlə:")
    if st.button("Kampaniya Yaradın"):
        if model:
            try:
                res = model.generate_content(f"{prod} üçün {target} kütləsinə uyğun 3 maraqlı reklam mətni yaz.")
                st.success(res.text)
            except Exception as e:
                st.error(f"Model sorğunu cavablandırmadı: {e}")
        else:
            st.warning("Model aktiv deyil. Lütfən API Key-i yoxlayın.")

elif menu == "👁️ Vision AI":
    st.header("👁️ Universal Göz")
    file = st.camera_input("Şəkil çək")
    if file and model:
        img = Image.open(file)
        with st.spinner("Analiz edilir..."):
            try:
                res = model.generate_content(["Bu şəkli analiz et.", img])
                st.write(res.text)
            except:
                st.error("Bu model hazırda şəkil analizini dəstəkləmir.")

elif menu == "💼 QR Generator":
    st.header("💼 QR Kod")
    text = st.text_input("Link daxil edin:")
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
            res = model.generate_content(f"Peşəkar usta kimi bu problemi həll et: {prob}")
            st.write(res.text)
