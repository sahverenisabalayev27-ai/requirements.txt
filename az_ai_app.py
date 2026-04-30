import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- SULTAN AI: REGION-SHIELD VERSİYA ---
st.set_page_config(page_title="Sultan AI", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

API_KEY = "AIzaSyCd0w-fJTdofu0WO2de0Xf0N_SzCdGT6CI"

# CSS - Dizaynı stabil saxlayırıq
st.markdown("""<style> .stApp { background-color: #0e1117; color: white; } </style>""", unsafe_allow_html=True)

# Modelləri yoxlayan və ən uyğununu seçən funksiya
def init_model():
    try:
        genai.configure(api_key=API_KEY)
        # Ən bəsit və ən çox icazə verilən modeli seçirik
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except:
        return None

model = init_model()

st.sidebar.title("💎 SULTAN AI")
menu = st.sidebar.selectbox("Bölməni Seçin:", ["📢 Reklam Yazarı", "🛠️ Texniki Usta", "💼 QR Generator"])

if menu == "📢 Reklam Yazarı":
    st.header("📢 Reklam Mərkəzi")
    prod = st.text_input("Məhsul adı:")
    if st.button("Mətni Hazırla"):
        if model:
            try:
                # Sorğunu ən bəsit formada göndəririk (Region blokuna düşməmək üçün)
                response = model.generate_content(f"Yaz: {prod} haqqında maraqlı reklam.")
                st.success(response.text)
            except Exception as e:
                if "PermissionDenied" in str(e):
                    st.error("Xəta: Google bu açar üçün region məhdudiyyəti qoyub.")
                    st.info("Məsləhət: Google AI Studio-da yeni açar yaradanda 'Pay-as-you-go' deyil, 'Free' planını seçin.")
                else:
                    st.error(f"Xəta baş verdi: {e}")

elif menu == "🛠️ Texniki Usta":
    st.header("🛠️ Texniki Usta")
    prob = st.text_area("Problemi yazın:")
    if st.button("Həllini Tap"):
        try:
            res = model.generate_content(f"Usta kimi cavab ver: {prob}")
            st.write(res.text)
        except:
            st.error("Bağlantı kəsildi.")

elif menu == "💼 QR Generator":
    st.header("💼 QR Kod")
    link = st.text_input("Link:")
    if st.button("Yarat"):
        qr = qrcode.make(link)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf)
