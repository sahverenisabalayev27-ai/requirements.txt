import streamlit as st
from groq import Groq
import random
import os

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI - Tam Versiya", page_icon="🏫", layout="wide")

# CSS - Müasir dizayn
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [aria-selected="true"] { background-color: #1a237e !important; color: white !important; }
    .stButton>button { border-radius: 12px; font-weight: bold; }
    .audio-player { margin-top: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt, tokens=2000):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=tokens
            )
            return resp.choices[0].message.content
        except: continue
    return "Xəta baş verdi."

# 3. Sessiya İdarəetməsi
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_test' not in st.session_state: st.session_state.current_test = None

# 4. İnterfeys (Sidebar)
with st.sidebar:
    st.title("🏫 İdarə Paneli")
    subject_list = [
        "Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", 
        "Coğrafiya", "İnformatika", "İngilis dili", "Rus dili", "Alman dili", "Fransız dili"
    ]
    subject = st.selectbox("Fənn seçin:", subject_list)
    topic = st.text_input("Mövzu:", value="Ümumi")
    st.divider()
    st.metric("Sənin Xalın 🏆", f"{st.session_state.score} XP")
    
    # 🎤 Səs funksiyası üçün placeholder (Sadələşdirilmiş versiya)
    st.write("🔊 Səsli Cavab: **Aktiv (Oğlan səsi)**")

# --- ƏSAS EKRAN ---
tab1, tab2, tab3 = st.tabs(["📚 Ensiklopediya & Səs", "📝 Sonsuz Sual Bankı", "📁 Fayl/Şəkil Analizi"])

# 📚 TAB 1: ÖYRƏN VƏ SƏS
with tab1:
    if st.button("Mövzunu İzah Et 📖"):
        with st.spinner("AI müəllim hazırlayır..."):
            explanation = call_ai(f"{subject} fənnindən {topic} haqqında dərin məlumat ver.")
            st.markdown(explanation)
            # Səsli oxuma simulyasiyası (Google TTS api lazım ola bilər, hələlik placeholder qoyuruq)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Nümunə səs

# 📝 TAB 2: SONSUZ SUAL (NÖVBƏTİ DÜYMƏSİ İLƏ)
with tab2:
    def load_new_test():
        res = call_ai(f"{subject} fənnindən {topic} haqqında test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [Hərf] İZAH: [..]")
        if "DOĞRU:" in res:
            try:
                st.session_state.current_test = {
                    "q": res.split("SUAL:")[1].split("A)")[0].strip(),
                    "opts": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                    "ans": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                    "expl": res.split("İZAH:")[1].strip()
                }
            except: pass

    if st.button("Sınağa Başla 🚀") or st.session_state.current_test is None:
        load_new_test()

    if st.session_state.current_test:
        t = st.session_state.current_test
        st.info(f"**Sual:** {t['q']}")
        user_choice = st.radio("Variant seç:", ["A", "B", "C", "D"], key="test_radio")
        
        col_c, col_n = st.columns(2)
        with col_c:
            if st.button("✅ Yoxla"):
                if user_choice == t['ans']:
                    st.success(f"Düzdür! {t['expl']}")
                    st.session_state.score += 10
                    st.balloons()
                else:
                    st.error(f"Səhvdir! Doğru cavab: {t['ans']}. İzah: {t['expl']}")
        
        with col_n:
            if st.button("Növbəti Sual ➡️"):
                load_new_test()
                st.rerun()

# 📁 TAB 3: FAYL ANALİZİ
with tab3:
    st.subheader("🖼️ Şəkil və ya PDF-dən Sual İzahı")
    uploaded_file = st.file_uploader("Testin şəklini və ya PDF-i bura atın", type=["jpg", "png", "pdf"])
    
    if uploaded_file is not None:
        st.success("Fayl yükləndi. Analiz edilir...")
        if st.button("Faylı İzah Et 🧠"):
            # Real OCR üçün kitabxanalar lazımdır, hələlik AI-ya müraciət simulyasiyası:
            st.info("Bu hissədə AI faylı oxuyur (Tezliklə tam inteqrasiya olunacaq)...")
            izah = call_ai(f"Mənə bir test şəkli göndərilib, mövzusu {subject}. Onu necə həll edə bilərəm?")
            st.write(izah)

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren")
