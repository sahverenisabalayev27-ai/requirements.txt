import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: AVTOMATİK MODEL SEÇİCİ ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

API_KEY = "AIzaSyD0_EWzOr1ZAQj3JXkdsJCfVQbom_n6Qm0"

# Stil
st.markdown("""<style> .stApp { background-color: #0e1117; color: white; } </style>""", unsafe_allow_html=True)

@st.cache_resource
def get_sultan_model():
    try:
        genai.configure(api_key=API_KEY.strip())
        # Açara icazə verilən bütün modelləri çəkirik
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if models:
            # Əgər Flash varsa onu, yoxdursa siyahıdakı birinci (adətən Pro) modeli seç
            best_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
            return genai.GenerativeModel(best_model), best_model
    except Exception as e:
        return None, str(e)
    return None, "Heç bir model tapılmadı."

model, model_name = get_sultan_model()

st.sidebar.title("💎 SULTAN AI")
if model:
    st.sidebar.success(f"✅ Aktiv: {model_name.split('/')[-1]}")
else:
    st.sidebar.error("❌ Model Tapılmadı")

menu = st.sidebar.selectbox("Bölməni Seçin:", ["📢 Reklam Yazarı", "🛠️ Texniki Usta", "💼 QR Generator"])

if model:
    if menu == "📢 Reklam Yazarı":
        st.header("📢 Reklam Mərkəzi")
        prod = st.text_input("Məhsul adı:")
        if st.button("Reklamı Hazırla"):
            try:
                with st.spinner("Hazırlanır..."):
                    res = model.generate_content(f"{prod} üçün maraqlı reklam yaz.")
                    st.success(res.text)
            except Exception as e:
                st.error(f"Bağlantı xətası: {e}")

    elif menu == "🛠️ Texniki Usta":
        st.header("🛠️ Texniki Usta")
        prob = st.text_area("Problemi yazın:")
        if st.button("Həll Yolunu Tap"):
            try:
                res = model.generate_content(f"Usta kimi cavab ver: {prob}")
                st.write(res.text)
            except Exception as e:
                st.error(f"Xəta: {e}")

    elif menu == "💼 QR Generator":
        st.header("💼 QR Kod")
        link = st.text_input("Link:")
        if st.button("QR Yarat"):
            qr = qrcode.make(link)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf)
else:
    st.error(f"Sistem xətası: {model_name}")
    st.info("Zəhmət olmasa, 5 dəqiqə gözləyin, Google yeni açarı sistemdə aktivləşdirir.")
