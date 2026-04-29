import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="Sultan AI | Universal Portal", page_icon="💎", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #FF4B4B, #822727); color: white; border-radius: 10px; border: none; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- API VƏ MODEL TAPILMASI (DİNAMİK YOXlama) ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Sultan AI Key daxil edin:", type="password")

model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        # Mövcud ola biləcək bütün model adlarını siyahıya alırıq
        available_models = ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']
        
        # İlk işləyən modeli tapana qədər yoxlayırıq
        for m_name in available_models:
            try:
                temp_model = genai.GenerativeModel(m_name)
                # Kiçik bir test sorğusu göndəririk ki, həqiqətən işlədiyini bilək
                temp_model.generate_content("test", generation_config={"max_output_tokens": 1})
                model = temp_model
                st.sidebar.success(f"Aktiv Model: {m_name}")
                break
            except:
                continue
                
        if model is None:
            st.error("Xəta: Heç bir modelə qoşulmaq mümkün olmadı. API Key-inizi yoxlayın.")
            
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
                try:
                    res = model.generate_content(f"{prod} üçün {target} kütləsinə uyğun 3 maraqlı reklam mətni yaz.")
                    st.success(res.text)
                except Exception as e:
                    st.error(f"Sorğu zamanı xəta yarandı: {e}")
        else:
            st.error("API Key daxil edilməyib və ya model aktiv deyil.")

elif menu == "👁️ Vision AI":
    st.header("👁️ Universal Göz")
    file = st.camera_input("Şəkil çək")
    if file and model:
        img = Image.open(file)
        with st.spinner("Analiz edilir..."):
            try:
                # Vision üçün xüsusi model adını birbaşa çağırırıq əgər ana model dəstəkləmirsə
                vision_model = genai.GenerativeModel('gemini-1.5-flash')
                res = vision_model.generate_content(["Bu şəkli analiz et və təsvir ver.", img])
                st.write(res.text)
            except Exception as e:
                st.error(f"Vision xətası: {e}. Bu model şəkli dəstəkləmir.")

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
