import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI - Sonsuz Sual Bankı", page_icon="🎓", layout="wide")

# CSS - Daha peşəkar görünüş
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .question-box { background: white; padding: 25px; border-radius: 15px; border: 2px solid #1a237e; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=1000
            )
            return resp.choices[0].message.content
        except:
            continue
    return None

# 3. İnterfeys
st.markdown("<h1 style='text-align: center; color: #1a237e;'>🏫 Sonsuz Sual Bankı AI</h1>", unsafe_allow_html=True)
st.divider()

st.sidebar.title("👤 Profilim")
st.sidebar.metric("Düzgün Cavablar 🏆", st.session_state.get('correct_count', 0))
st.sidebar.info("Hər mövzu üzrə minlərlə fərqli sual sistemi aktivdir.")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📚 Mövzu Seç")
    subject = st.selectbox("Fənni seçin:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "Coğrafiya"])
    topic = st.text_input("Mövzunu daxil edin:", placeholder="Məsələn: Səfəvilər")
    
    if st.button("Yeni Sual Hazırla 🔄"):
        if topic:
            with st.spinner("Yeni sual hazırlanır..."):
                # Botdan fərqli sual istəyirik
                prompt = f"""
                {subject} fənnindən {topic} mövzusunda təsadüfi bir test sualı hazırla. 
                Əvvəlki suallardan fərqli olsun. 
                Format: 
                Sual mətni
                A) variant
                B) variant
                C) variant
                D) variant
                E) variant
                DOĞRU_CAVAB: X
                """
                res = call_ai(prompt)
                if res and "DOĞRU_CAVAB:" in res:
                    parts = res.split("DOĞRU_CAVAB:")
                    st.session_state.q_text = parts[0]
                    st.session_state.c_ans = parts[1].strip()
                    st.session_state.answered = False # Cavab verilməyib rejimine kec
        else:
            st.warning("Mövzu daxil edin.")

with col2:
    if 'q_text' in st.session_state:
        st.markdown(f"<div class='question-box'><h3>Sual:</h3>{st.session_state.q_text}</div>", unsafe_allow_html=True)
        
        user_choice = st.radio("Variantı seçin:", ["A", "B", "C", "D", "E"], key="user_radio")
        
        if st.button("Yoxla ✅"):
            st.session_state.answered = True
            if user_choice == st.session_state.c_ans:
                st.success(f"Düzdür! Cavab: {st.session_state.c_ans}")
                st.session_state.correct_count = st.session_state.get('correct_count', 0) + 1
                st.balloons()
            else:
                st.error(f"Səhvdir. Düzgün cavab: {st.session_state.c_ans}")
    else:
        st.info("Sol tərəfdən mövzu seçib 'Yeni Sual Hazırla' düyməsinə basaraq imtahana başlayın.")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sonsuz Öyrənmə Sistemi")
