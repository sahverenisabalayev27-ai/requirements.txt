import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- ƏN SADƏ AYARLAR ---
st.set_page_config(page_title="Sultan AI", layout="centered")

# CSS - Ağ ekranın qarşısını almaq üçün minimal dizayn
st.markdown("""<style> .stApp { background-color: #0e1117; color: white; } </style>""", unsafe_allow_html=True)

st.title("💎 Sultan AI: Rəqəmsal Portal")

# --- API KEY (SADƏLƏŞDİRİLMİŞ) ---
# Əgər secrets işləmirsə, birbaşa sidebar-dan daxil etməyi tələb edirik
api_key = st.sidebar.text_input("Google AI Key daxil edin:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Ən stabil modeli birbaşa çağırırıq
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        menu = st.selectbox("Xidmət seçin:", ["Reklam Yazarı", "Texniki Usta", "QR Generator"])
        
        if menu == "Reklam Yazarı":
            text_in = st.text_input("Məhsul adı:")
            if st.button("Hazırla"):
                res = model.generate_content(f"{text_in} üçün qısa reklam mətni yaz.")
                st.write(res.text)
                
        elif menu == "Texniki Usta":
            prob_in = st.text_area("Problemi yazın:")
            if st.button("Həll tap"):
                res = model.generate_content(f"Usta kimi cavab ver: {prob_in}")
                st.write(res.text)
                
        elif menu == "QR Generator":
            link_in = st.text_input("Link daxil edin:")
            if st.button("QR Yarat"):
                img = qrcode.make(link_in)
                buf = BytesIO()
                img.save(buf)
                st.image(buf)
                
    except Exception as e:
        st.error(f"Bağlantı xətası: {e}")
else:
    st.warning("Zəhmət olmasa, sol tərəfdəki qutuya API Key yapışdırın.")
