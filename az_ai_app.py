import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: MEMARLIQ VƏ 3D VİZUALİZASİYA PLATFORMASI ---
st.set_page_config(page_title="Sultan AI: Memar", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

# Sənin yeni və işlək API açarın
API_KEY = "AIzaSyCOBiUabMs9t4K6TFfAK-4_cBH2XnbKHoA"

# Professional İnşaat və Memarlıq Mövzusu (Tünd Gold və Tikinti çalarları)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e6ed; }
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #aa7c11); 
        color: black; border-radius: 8px; border: none; font-weight: bold; width: 100%; height: 3.5em;
    }
    .stButton>button:hover { background: linear-gradient(45deg, #aa7c11, #d4af37); color: white; }
    h1, h2, h3 { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# Modellərin ilkin tənzimlənməsi funksiyası
def init_sultan_model():
    try:
        genai.configure(api_key=API_KEY.strip())
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Sistem qoşulma xətası: {e}")
        return None

model = init_sultan_model()

# İndi isə menyu və əsas interfeys məntiqini başladırıq
if model:
    st.sidebar.title("🏛️ SULTAN MEMARLIQ")
    st.sidebar.success("AI Memarlıq Modulu Aktivdir")
    
    menu = st.sidebar.selectbox("Layihə Alətləri:", ["📋 Yeni Ev Layihəsi", "📐 Çertyoj Analizi", "🎨 3D Render Prompt Generator"])

    if menu == "📋 Yeni Ev Layihəsi":
        st.title("🏠 Süni Zəka ilə Ev İnşası və Planlaşdırılması")
        st.write("Evinizin xəyalınızdakı parametrlərini daxil edin, AI sizin üçün ilkin memarlıq konsepsiyasını qursun.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧱 Əsas Parametrlər")
            style = st.selectbox("Memarlıq Üslubu:", ["Modern / Minimalist", "Klassik", "Xay-Tek (High-Tech)", "Ənənəvi Azərbaycan Memarlığı (Lahıc/Xınalıq daş üslubu)", "Kənd evi / Loft"])
            floors = st.slider("Mərtəbə sayı:", 1, 3, 1)
            total_area = st.number_input("Ümumi sahə (kvadrat metr ilə):", min_value=30, max_value=1000, value=120)
            
        with col2:
            st.subheader("🛏️ Daxili Bölgülər Və Həyət")
            rooms = st.text_input("Otaqların təxmini ölçüləri:", placeholder="Məs: Qonaq otağı 5x6, Yataq otağı 4x4, Mətbəx 3x4")
            yard_features = st.text_area("Həyətdə nə olacaq?:", placeholder="Məs: 4x8 metr hovuz, qazon, daş döşəməli besedka, dekorativ ağaclar")

        st.markdown("---")
        ext_inter_desc = st.text_area("Əlavə xarici və daxili görünüş istəkləri:", placeholder="Məsələn: Evin fasadı təbii Ağlay daşı və şüşə panellərdən olsun. Daxildə epoksid döşəmə və gizli işıqlandırma istifadə edilsin.")

        if st.button("🏗️ Memarlıq Konsepsiyasını və 3D Təsviri Yarat"):
            with st.spinner("Sultan AI memarlıq planını hesablayır və vizual təsviri hazırlayır..."):
                try:
                    prompt = f"""
                    Bir memar və 3D vizualizator kimi aşağıdakı ev layihəsinin tam memarlıq konsepsiy
