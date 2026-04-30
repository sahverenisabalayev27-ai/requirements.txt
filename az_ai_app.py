import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: RƏQƏMSAL İMPERİYA ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="wide")

# Yeni API açarını bura daxil etdim
API_KEY = "AIzaSyCd0w-fJTdofu0WO2de0Xf0N_SzCdGT6CI"

# --- STİL VƏ DİZAYN ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF4B4B, #822727); 
        color: white; border-radius: 12px; border: none; font-weight: bold; width: 100%; height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); background: linear-gradient(45deg, #822727, #FF4B4B); }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL AKTİVASİYA FUNKSİYASI ---
@st.cache_resource
def load_sultan_model():
    try:
        genai.configure(api_key=API_KEY.strip())
        # Açarına uyğun işlək modelləri siyahıdan axtarırıq
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if available_models:
            # Əgər flash varsa onu, yoxdursa siyahıdakı ilk işlək modeli götür
            selected_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            return genai.GenerativeModel(selected_model), selected_model
    except Exception as e:
        return None, str(e)
    return None, "Heç bir model tapılmadı."

model, model_info = load_sultan_model()

# --- ƏSAS İNTERFEYS ---
st.sidebar.title("💎 SULTAN AI")
st.sidebar.markdown(f"**Status:** {'✅ Aktiv' if model else '❌ Deaktiv'}")
if model:
    st.sidebar.caption(f"Model: {model_info}")

menu = st.sidebar.selectbox("Bölməni Seçin:", ["🏠 Ana Səhifə", "📢 Reklam Yazarı", "🛠️ Texniki Usta", "💼 QR Generator"])

if not model:
    st.error(f"Sistemə qoşulmaq mümkün olmadı: {model_info}")
    st.info("Zəhmət olmasa, Google AI Studio-da açarın statusunu və ya regional icazələri yoxlayın.")
else:
    if menu == "🏠 Ana Səhifə":
        st.title("Sultan AI: Milli Portal 🇦🇿")
        st.info("Zəka Təsvirləri vizyonu ilə hazırlanmış universal süni zəka sistemi.")
        st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995", caption="Gələcəyi Sultan AI ilə qurun")

    elif menu == "📢 Reklam Yazarı":
        st.header("📢 Reklam Mərkəzi")
        prod = st.text_input("Məhsulun adı:")
        target = st.text_input("Kimin üçün? (Hədəf kütlə):")
        if st.button("Kampaniya Yaradın"):
            with st.spinner("AI reklam mətni hazırlayır..."):
                res = model.generate_content(f"{prod} məhsulu üçün {target} kütləsinə uyğun kreativ reklam yaz.")
                st.success(res.text)

    elif menu == "🛠️ Texniki Usta":
        st.header("🛠️ Texniki Usta Dəstəyi")
        prob = st.text_area("Problemi yazın (məs: kombi radiatoru isinmir):")
        if st.button("Həllini Tap"):
            with st.spinner("Usta məsləhəti hazırlanır..."):
                res = model.generate_content(f"Peşəkar usta kimi bu problemi həll et: {prob}")
                st.write(res.text)

    elif menu == "💼 QR Generator":
        st.header("💼 QR Kod Generator")
        link = st.text_input("Link və ya yazı daxil edin:")
        if st.button("QR Kod Yaradın"):
            qr_img = qrcode.make(link)
            buf = BytesIO()
            qr_img.save(buf)
            st.image(buf, caption="Sizin Sultan QR Kodunuz")
