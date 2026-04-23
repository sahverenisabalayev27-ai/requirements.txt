import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI", page_icon="🎓", layout="wide")

# CSS - Dizaynı daha da gözəlləşdiririk
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background-color: #1a237e;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .test-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
def get_api_keys():
    return [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

active_keys = get_api_keys()

def call_ai(prompt):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=2000
            )
            return resp.choices[0].message.content
        except:
            continue
    return "Sistem yüklüdür, az sonra yenidən yoxlayın."

# 3. İnterfeys
st.markdown("<h1 style='text-align: center; color: #1a237e;'>🏫 Akademiya AI Portalı</h1>", unsafe_allow_html=True)
st.divider()

# Sidebar (Artıq texniki yazılar yoxdur)
st.sidebar.title("👤 Profilim")
st.sidebar.info("Xoş gəldiniz! Tezliklə burada xallarınız və nailiyyətləriniz görünəcək.")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📚 Dərs Paneli")
    subject = st.selectbox("Fənni seçin:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "Coğrafiya"])
    mode = st.radio("İş rejimi:", ["Dərin İzah (Ensiklopediya)", "İmtahan (Test)"])

with col2:
    st.subheader("✍️ Mövzu")
    topic = st.text_input("Mövzu adı daxil edin:", placeholder="Məsələn: Albaniya dövləti")
    
    if st.button("Dərsi Başlat 🚀"):
        if topic:
            if mode == "Dərin İzah (Ensiklopediya)":
                with st.spinner("Məlumat toplanır..."):
                    res = call_ai(f"{subject} fənnindən {topic} haqqında çox geniş, akademik məlumat ver.")
                    st.markdown(res)
            
            else: # İmtahan Rejimi
                with st.spinner("Sual hazırlanır..."):
                    # Botdan xüsusi formatda sual istəyirik
                    test_res = call_ai(f"{subject} fənnindən {topic} haqqında 1 ədəd çoxvariantlı test sualı hazırla. Format belə olsun: Sual mətni, sonra A, B, C, D variantları. Sonda 'DOĞRU_CAVAB: X' şəklində qeyd et.")
                    
                    # Cavabı ayırmaq üçün məntiq
                    if "DOĞRU_CAVAB:" in test_res:
                        parts = test_res.split("DOĞRU_CAVAB:")
                        question_text = parts[0]
                        correct_answer = parts[1].strip()
                        
                        st.session_state.current_question = question_text
                        st.session_state.correct_ans = correct_answer
                    else:
                        st.write(test_res)

    # Testi göstərmək və seçimi idarə etmək
    if mode == "İmtahan (Test)" and 'current_question' in st.session_state:
        st.markdown("---")
        st.markdown(f"### ❓ Sual:\n{st.session_state.current_question}")
        
        user_choice = st.radio("Düzgün variantı seçin:", ["A", "B", "C", "D", "E"])
        
        if st.button("Yoxla ✅"):
            if user_choice == st.session_state.correct_ans:
                st.success(f"Mükəmməl! Düzgün cavab: {st.session_state.correct_ans}")
                st.balloons()
            else:
                st.error(f"Təəssüf, səhvdir. Düzgün cavab: {st.session_state.correct_ans}")
                st.info("Mövzunu yenidən oxumağınız məsləhətdir.")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren")
