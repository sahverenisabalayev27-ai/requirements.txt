import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="wide")

API_KEY = "AIzaSyCd0w-fJTdofu0WO2de0Xf0N_SzCdGT6CI"

# CSS
st.markdown("""<style> .stApp { background-color: #0e1117; color: white; } </style>""", unsafe_allow_html=True)

@st.cache_resource
def get_best_model():
    try:
        genai.configure(api_key=API_KEY)
        # Sistemdə olan bütün modelləri siyahıya alırıq
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if models:
            # Ən yeni modeli seçməyə çalışırıq
            for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
                if target in models:
                    return genai.GenerativeModel(target)
            return genai.GenerativeModel(models[0])
    except Exception as e:
        return str(e)
    return None

model_engine = get_best_model()

st.title("💎 Sultan AI: Rəqəmsal Portal")

if isinstance(model_engine, str):
    st.error(f"Sistem xətası: {model_engine}")
elif model_engine is None:
    st.warning("Google modelləri ilə əlaqə qurula bilmir. Bir az gözləyin...")
else:
    menu = st.sidebar.selectbox("Bölməni Seçin:", ["📢 Reklam Yazarı", "🛠️ Texniki Usta", "💼 QR Generator"])
    
    if menu == "📢 Reklam Yazarı":
        prod = st.text_input("Məhsul adı:")
        if st.button("Mətni Hazırla"):
            try:
                # Ən bəsit sorğu
                res = model_engine.generate_content(f"Write a short ad for: {prod}")
                st.success(res.text)
            except Exception as e:
                st.error(f"Bağlantı kəsildi: {e}")

    elif menu == "🛠️ Texniki Usta":
        prob = st.text_area("Problemi yazın:")
        if st.button("Həllini Tap"):
            try:
                res = model_engine.generate_content(f"Usta məsləhəti: {prob}")
                st.write(res.text)
            except Exception as e:
                st.error(f"Xəta: {e}")
