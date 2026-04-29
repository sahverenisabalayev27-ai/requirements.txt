import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(
    page_title="Sultan AI | Universal Ekosistem",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS İLƏ MÜKƏMMƏL GÖRÜNÜŞ ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); }
    </style>
    """, unsafe_allow_html=True)

# --- API KEY TƏHLÜKƏSİZLİYİ ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Sultan AI Key daxil edin:", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- SİDEBAR NAVİQASİYA ---
st.sidebar.image("https://via.placeholder.com/150x150.png?text=SULTAN+AI", width=150) # Bura öz loqonu qoyarsan
st.sidebar.title("💎 SULTAN AI PORTAL")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Mərkəzi Seçin:", [
    "🏠 Ana Səhifə", 
    "👁️ Vision AI (Hər Şeyi Tanıyan Göz)", 
    "🎨 Dizayn & Loqo Studiyası", 
    "📢 Reklam & Marketinq Mərkəzi", 
    "🏗️ Memarlıq & İnşaat (Milli)",
    "⚙️ Texniki Problemlər & Usta",
    "💼 Biznes & QR Generator",
    "🩺 Sağlamlıq & Gündəlik Həyat"
])

# --- FUNKSİYALAR ---

if menu == "🏠 Ana Səhifə":
    st.title("Sultan AI: Milli Rəqəmsal İnqilab 🇦🇿")
    st.write("### 'Zəka Core' tərəfindən idarə olunan universal həllər platforması.")
    col1, col2, col3 = st.columns(3)
    col1.metric("İstifadəçi Sahəsi", "Bütün Sahələr")
    col2.metric("Süni İntellekt", "Gemini 1.5 Pro")
    col3.metric("Status", "Aktiv")
    st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995", caption="Gələcəyin Texnologiyası Sultan Media ilə")

elif menu == "👁️ Vision AI (Hər Şeyi Tanıyan Göz)":
    st.header("👁️ Universal Göz")
    st.info("Nəyin şəklini çəksəniz, AI onu saniyələr içində analiz edəcək.")
    img_file = st.camera_input("Kameranı aç")
    if img_file and API_KEY:
        img = Image.open(img_file)
        with st.spinner("Analiz edilir..."):
            res = model.generate_content(["Bu nədir? Ətraflı izah et və mənə bununla bağlı faydalı məsləhətlər ver.", img])
            st.write(res.text)

elif menu == "🎨 Dizayn & Loqo Studiyası":
    st.header("🎨 AI Dizayn Mərkəzi")
    idea = st.text_input("Loqo və ya Dizayn ideyanızı yazın:")
    if st.button("Dizayn Promptu Yarat"):
        res = model.generate_content(f"'{idea}' ideyası üçün 3D hiper-realistik, professional loqo və ya brendinq dizaynı üçün detallı DALL-E/Midjourney promptu yaz.")
        st.code(res.text)
        st.info("Bu promptu kopyalayıb şəkli yarada bilərsiniz.")

elif menu == "📢 Reklam & Marketinq Mərkəzi":
    st.header("📢 Professional Reklam Yazarı")
    product = st.text_input("Məhsul və ya xidmət adı:")
    target = st.text_input("Hədəf kütlə (məs: Gənclər, Ev xanımları):")
    if st.button("Kampaniya Hazırla"):
        res = model.generate_content(f"{product} üçün {target} hədəf kütləsinə uyğun, psixoloji təsirli 3 fərqli Instagram reklam mətni və 5 hashtag yaz.")
        st.write(res.text)

elif menu == "🏗️ Memarlıq & İnşaat (Milli)":
    st.header("🏗️ Milli İnşaat Planlayıcısı")
    st.write("Eskiz və ya otaq şəklini analiz edib material hesablayaq.")
    # Vision AI inteqrasiyası bura gələcək

elif menu == "⚙️ Texniki Problemlər & Usta":
    st.header("⚙️ Rəqəmsal Usta")
    prob = st.text_area("Problemi təsvir edin (və ya yuxarıdan şəklini çəkin):")
    if st.button("Həll Yolunu Tap"):
        res = model.generate_content(f"Texniki usta kimi bu problemi həll et: {prob}")
        st.success(res.text)

elif menu == "💼 Biznes & QR Generator":
    st.header("💼 Biznes Alətləri")
    data = st.text_input("QR Koda gedəcək link və ya məlumat:")
    if st.button("QR Kod Yarat"):
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf)
        st.download_button("QR Kodu Yüklə", buf.getvalue(), "sultan_qr.png")

elif menu == "🩺 Sağlamlıq & Gündəlik Həyat":
    st.header("🩺 Sultan Life Köməkçisi")
    q = st.text_input("Sualınız (Sağlamlıq, Mətbəx, Həyat tərzi):")
    if st.button("Məsləhət Al"):
        res = model.generate_content(f"Gündəlik həyat köməkçisi kimi cavab ver: {q}")
        st.write(res.text)
