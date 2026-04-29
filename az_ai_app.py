import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Sultan AI | Universal Portal", page_icon="💎", layout="wide")

# --- API KEY OXUMA ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("API Key-i daxil edin:", type="password")

# --- MODELİ İŞƏ SALMA ---
model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.sidebar.error("API Bağlantı Xətası!")

# --- DİZAYN (MODERN DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF4B4B, #822727); 
        color: white; 
        border-radius: 10px; 
        border: none; 
        font-weight: bold; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- MENYU ---
st.sidebar.title("💎 SULTAN AI")
menu = st.sidebar.selectbox("Bölməni Seçin:", ["🏠 Ana Səhifə", "📢 Reklam Mərkəzi", "👁️ Vision AI", "💼 QR Generator", "⚙️ Usta Dəstəyi"])

if menu == "🏠 Ana Səhifə":
    st.title("Sultan AI: Milli Super-Portal 🇦🇿")
    st.info("Zəka Core tərəfindən idarə olunan universal rəqəmsal mərkəz.")
    st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995", caption="Gələcəyin Texnologiyası Sultan Media ilə")

elif menu == "📢 Reklam Mərkəzi":
    st.header("📢 Reklam Hazırla")
    prod = st.text_input("Məhsul adı (məs: Bərbərxana):")
    target = st.text_input("Hədəf kütlə (məs: Gənclər):")
    if st.button("Kampaniya Yaradın") and model:
        with st.spinner("Sultan AI hazırlayır..."):
            res = model.generate_content(f"{prod} üçün {target} kütləsinə uyğun cəlbedici reklam mətni və hashtaglar yaz.")
            st.success(res.text)

elif menu == "👁️ Vision AI":
    st.header("👁️ Universal Göz")
    file = st.camera_input("Şəkil çək")
    if file and model:
        img = Image.open(file)
        with st.spinner("Analiz edilir..."):
            res = model.generate_content(["Bu şəkli peşəkar analiz et və tövsiyələr ver.", img])
            st.write(res.text)

elif menu == "💼 QR Generator":
    st.header("💼 QR Kod Yarat")
    text = st.text_input("Link və ya yazı:")
    if st.button("Yarat"):
        qr = qrcode.make(text)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf, caption="Sizin QR Kodunuz")
        st.download_button("Yüklə", buf.getvalue(), "sultan_qr.png")

elif menu == "⚙️ Usta Dəstəyi":
    st.header("⚙️ Texniki Usta")
    prob = st.text_area("Problemi yazın:")
    if st.button("Həllini Tap") and model:
        res = model.generate_content(f"Peşəkar usta kimi bu problemi həll et: {prob}")
        st.write(res.text)
