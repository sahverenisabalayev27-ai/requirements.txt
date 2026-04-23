import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI", page_icon="🎓", layout="wide")

# CSS Dizaynı
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1a237e;
        color: white;
        font-weight: bold;
    }
    .status-card {
        padding: 15px;
        border-radius: 10px;
        background-color: white;
        border-left: 5px solid #1a237e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Açar Sistemi
def get_keys():
    return [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

active_keys = get_keys()

def generate_ai_response(subject, topic, mode):
    if not active_keys:
        return "⚠️ Secrets hissəsində API açarı tapılmadı!"
    
    random.shuffle(active_keys)
    
    if mode == "Dərin İzah (Ensiklopediya)":
        prompt = f"Sən Azərbaycanlı professorsan. {subject} fənnindən '{topic}' mövzusunu ən az 1500 sözlə, çox ətraflı və elmi şəkildə izah et. Dil: Azərbaycan dili."
    else:
        prompt = f"Şagird üçün {subject} fənnindən '{topic}' mövzusunda 1 ədəd çətin test sualı hazırla. Düzgün cavabı sonda qeyd et."

    for key in active_keys:
        try:
            client = Groq(api_key=key)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=4000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                continue
            else:
                return f"❌ Xəta: {str(e)}"
    return "😴 Bütün açarların limiti dolub, 1 dəqiqə gözləyin."

# 3. İnterfeys
st.markdown("<h1 style='text-align: center;'>🎓 Akademiya AI Portalı</h1>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.sidebar.markdown("## ⚙️ Sistem Paneli")
    st.sidebar.markdown(f"<div class='status-card'>✅ <b>Server:</b> Aktiv<br>🔑 <b>Açar Sayı:</b> {len(active_keys)}</div>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Seçimlər")
    # BURADA DƏQİQ OLUN: Dırnaqların bağlandığından əmin olun
    subject = st.selectbox("Fənni seçin:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "Coğrafiya"])
    mode = st.radio("İş rejimi:", ["Dərin İzah (Ensiklopediya)", "İmtahan Rejimi (Test)"])

with col2:
    st.markdown("### ✍️ Mövzu Daxil Et")
    topic = st.text_input("Mövzu adı:", placeholder="Məsələn: Səfəvilər dövləti")
    
    if st.button("Dərsi Başlat 🚀"):
        if topic:
            with st.spinner("Məlumatlar hazırlanır..."):
                response = generate_ai_response(subject, topic, mode)
                st.markdown(response)
                st.balloons()
        else:
            st.warning("Mövzu adını yazın.")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren")
