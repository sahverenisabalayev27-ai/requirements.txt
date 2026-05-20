import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: MEMARLIQ VƏ 3D VİZUALİZASİYA PLATFORMASI ---
st.set_page_config(page_title="Sultan AI: Memar", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

# Sənin işlək API açarın
API_KEY = "AIzaSyCOBiUabMs9t4K6TFfAK-4_cBH2XnbKHoA"

# Professional İnşaat və Memarlıq Mövzusu
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

try:
    genai.configure(api_key=API_KEY.strip())
    # 2026-cı ilin standart və ən stabil modelinə keçid etdik: gemini-2.0-flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
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
            st.subheader("🛏️ Daxili Bölmələr Və Həyət")
            rooms = st.text_input("Otaqların təxmini ölçüləri:", value="Qonaq otağı 5x6, Yataq otağı 4x4, Mətbəx 3x4")
            yard_features = st.text_area("Həyətdə nə olacaq?:", value="4x8 metr hovuz, qazon, daş döşəməli besedka")

        st.markdown("---")
        ext_inter_desc = st.text_area("Əlavə xarici və daxili görünüş istəkləri:", value="Evin fasadı təbii Ağlay daşı olsun. Daxildə epoksid döşəmə istifadə edilsin.")

        if st.button("🏗️ Memarlıq Konsepsiyasını Yarat"):
            with st.spinner("Sultan AI memarlıq planını hesablayır..."):
                try:
                    prompt = f"Bir memar kimi bu evi analiz et və Azərbaycanca geniş cavab ver. Üslub: {style}, Mərtəbə: {floors}, Sahə: {total_area}m2, Otaqlar: {rooms}, Həyət: {yard_features}, İstəklər: {ext_inter_desc}. Cavabda Memarlıq təhlili, Sahə bölgüsü, Ekstryer və İnteryer məsləhətləri bölmələri olsun."
                    res = model.generate_content(prompt)
                    st.success("Layihə Konsepsiyası Hazırdır!")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Xəta: {e}")

    elif menu == "📐 Çertyoj Analizi":
        st.title("📐 Mətn Əsaslı Çertyoj və Plan Sxemi")
        st.write("Daxil etdiyiniz ölçülərə əsasən otaqların divar və qapı düzülüşünü vizual mətn sxemi şəklində simulyasiya edirik.")
        
        dimensions = st.text_area("Evin divar və otaq koordinatlarını yazın:", value="Ev 10x12 metr düzbucaqlı. Giriş koridoru 2x4. Sağda qonaq otağı 5x6, solda mətbəx 4x4.")
        
        if st.button("Çertyoj Strukturunu Hesabla"):
            with st.spinner("Ölçülər analiz edilir..."):
                try:
                    prompt = f"Aşağıdakı ölçülərə əsasən divar qalınlığı və qapı yerləşməsi üçün mühəndis çertyoj tövsiyəsi hazırlayın: {dimensions}"
                    res = model.generate_content(prompt)
                    st.info("Mühəndislik Qeydləri:")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Xəta: {e}")

    elif menu == "🎨 3D Render Prompt Generator":
        st.title("🎨 AI Renderləri üçün Professional Prompt Generator")
        st.write("Burada hazırlanan promptları Midjourney və ya Flux-a yapışdıraraq birbaşa şəkillər ala bilərsiniz.")
        
        render_idea = st.text_input("Evin hansı hissəsinin şəklini yaratmaq istəyirsiniz?", value="Lahıc daş üslubunda, hovuzlu, modern iki mərtəbəli villa")
        
        if st.button("Professional Prompt İstehsal Et"):
            with st.spinner("Prompt hazırlanır..."):
                try:
                    prompt = f"Write 2 professional English prompts for Midjourney and Stable Diffusion based on this idea: {render_idea}. Style: photorealistic, 8k, architectural photography."
                    res = model.generate_content(prompt)
                    st.subheader("Hazır İngiliscə Promptlar:")
                    st.code(res.text)
                except Exception as e:
                    st.error(f"Xəta: {e}")

except Exception as e:
    st.error(f"Sistem xətası: {e}")
