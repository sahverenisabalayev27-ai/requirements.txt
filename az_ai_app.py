import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(
    page_title="Sultan AI | Universal Ekosistem",
    page_icon="💎",
    layout="wide"
)

# --- CSS İLƏ PREMİUM DİZAYN ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(45deg, #FF4B4B, #FF8E53);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255,75,75,0.4); }
    .sidebar .sidebar-content { background: #161b22; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- API KEY VƏ MODEL KONFİQURASİYASI ---
# Secrets-dən oxumağa çalışır, yoxdursa kənardan daxil etməyi təklif edir
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Sultan AI Key daxil edin:", type="password")

model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # Ən stabil model adını istifadə edirik
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"Sistemə qoşulmaq mümkün olmadı: {e}")

# --- SİDEBAR NAVİQASİYA ---
st.sidebar.title("💎 SULTAN Ə.İ. MƏRKƏZİ")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Bölməni Seçin:", [
    "🏠 Ana Səhifə", 
    "👁️ Vision AI (Universal Göz)", 
    "🎨 Dizayn & Loqo Studiyası", 
    "📢 Reklam & Marketinq", 
    "🏗️ Memarlıq & Milli Stil",
    "⚙️ Texniki Usta Dəstəyi",
    "💼 Biznes & QR Alətləri",
    "🏠 Gündəlik Həyat (Life)"
])

# --- FUNKSİONAL HİSSƏLƏR ---

if menu == "🏠 Ana Səhifə":
    st.title("Sultan AI: Milli Rəqəmsal İmperiya 🇦🇿")
    st.write("### Hər kəs üçün universal süni intellekt həlləri.")
    st.info("Bu platforma 'Zəka Core' tərəfindən hər kəsin işini asanlaşdırmaq üçün yaradılıb.")
    st.image("https://images.unsplash.com/photo-1620712943543-bcc4628c9759?auto=format&fit=crop&q=80&w=1000", caption="Zəka Təsvirləri Vizyonu")

elif menu == "👁️ Vision AI (Universal Göz)":
    st.header("👁️ Sultan Göz")
    st.write("Kameranı açın və ya şəkil yükləyin. AI hər şeyi analiz edəcək.")
    img_file = st.camera_input("Şəkil çək")
    if img_file and model:
        img = Image.open(img_file)
        with st.spinner("Analiz edilir..."):
            res = model.generate_content(["Bu şəkli peşəkar şəkildə analiz et. Problemdirsə həllini, əşyadırsa dəyərini və təsvirini ver.", img])
            st.success("Nəticə:")
            st.write(res.text)

elif menu == "🎨 Dizayn & Loqo Studiyası":
    st.header("🎨 AI Dizayn Atelyesi")
    idea = st.text_input("Dizayn ideyanız nədir? (Məs: Müasir bərbərxana loqosu)")
    if st.button("Dizayn Planı Yarat") and model:
        with st.spinner("Dizayn təlimatları hazırlanır..."):
            res = model.generate_content(f"'{idea}' üçün 3D hiper-realistik, professional brendinq dizaynı üçün detallı və cinematic prompt yaz.")
            st.code(res.text)

elif menu == "📢 Reklam & Marketinq":
    st.header("📢 Reklam Mərkəzi")
    prod = st.text_input("Məhsul/Xidmət adı:")
    target = st.text_input("Hədəf kütlə:")
    if st.button("Kampaniya Hazırla") and model:
        with st.spinner("Yaradıcı mətnlər hazırlanır..."):
            res = model.generate_content(f"{prod} üçün {target} kütləsinə uyğun cəlbedici Instagram reklamı və hashtaglar yaz.")
            st.write(res.text)

elif menu == "💼 Biznes & QR Alətləri":
    st.header("💼 Biznes və QR")
    qr_text = st.text_input("QR kod üçün link və ya yazı daxil edin:")
    if st.button("QR Kod Yaradın"):
        qr = qrcode.make(qr_text)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf, caption="Sizin Sultan QR Kodunuz")
        st.download_button("Şəkli Yüklə", buf.getvalue(), "sultan_qr.png")

elif menu == "⚙️ Texniki Usta Dəstəyi":
    st.header("⚙️ Rəqəmsal Usta")
    problem = st.text_area("Texniki problemi təsvir edin:")
    if st.button("Həll Yolunu Göstər") and model:
        res = model.generate_content(f"Peşəkar usta kimi bu problemi addım-addım həll et: {problem}")
        st.success(res.text)

elif menu == "🏠 Gündəlik Həyat (Life)":
    st.header("🏠 Sultan Life")
    quest = st.text_input("Sizi nə maraqlandırır? (Mətbəx, ləkə çıxarmaq, məsləhət...)")
    if st.button("Sultan AI Cavab Versin") and model:
        res = model.generate_content(f"Gündəlik həyat köməkçisi kimi səmimi və faydalı cavab ver: {quest}")
        st.info(res.text)

# Əgər API key yoxdursa xəbərdarlıq et
if not API_KEY:
    st.warning("⚠️ Diqqət: Sistemin işləməsi üçün sol tərəfdə Google AI Key daxil edilməlidir!")
