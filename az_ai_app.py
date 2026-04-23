import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI - Ardıcıl Test", page_icon="🎓", layout="wide")

# CSS - Daha axıcı dizayn
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stRadio > label { font-size: 1.2rem; font-weight: bold; color: #1a237e; }
    .question-container {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 5px solid #1a237e;
    }
    .next-btn {
        background-color: #4CAF50 !important;
        color: white !important;
    }
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

# 3. Sessiya Yaddaşı (Sualı yadda saxlamaq üçün)
if 'question_data' not in st.session_state:
    st.session_state.question_data = None
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

def get_new_question(subject, topic):
    prompt = f"""
    {subject} fənnindən {topic} mövzusunda 1 ədəd maraqlı test sualı hazırla. 
    Variantlar: A, B, C, D, E. 
    Format mütləq belə olsun:
    SUAL: [Sual bura]
    A) [Variant]
    B) [Variant]
    C) [Variant]
    D) [Variant]
    E) [Variant]
    DOĞRU_CAVAB: [Səhv düşməmək üçün yalnız hərfi yaz, məs: A]
    İZAH: [Qısa izah]
    """
    res = call_ai(prompt)
    if res and "DOĞRU_CAVAB:" in res:
        try:
            q_part = res.split("SUAL:")[1].split("A)")[0].strip()
            a_part = "A) " + res.split("A)")[1].split("B)")[0].strip()
            b_part = "B) " + res.split("B)")[1].split("C)")[0].strip()
            c_part = "C) " + res.split("C)")[1].split("D)")[0].strip()
            d_part = "D) " + res.split("D)")[1].split("E)")[0].strip()
            e_part = "E) " + res.split("E)")[1].split("DOĞRU_CAVAB:")[0].strip()
            correct = res.split("DOĞRU_CAVAB:")[1].split("İZAH:")[0].strip()
            explain = res.split("İZAH:")[1].strip()
            
            return {
                "question": q_part,
                "options": [a_part, b_part, c_part, d_part, e_part],
                "answer": correct,
                "explanation": explain
            }
        except:
            return None
    return None

# 4. İnterfeys
st.markdown("<h1 style='text-align: center;'>🎓 İnteraktiv Sual Paneli</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("⚙️ Tənzimləmə")
    subject = st.selectbox("Fənn:", ["Tarix", "Biologiya", "Riyaziyyat", "Fizika", "Kimya", "Coğrafiya"])
    topic = st.text_input("Mövzu:", value="Səfəvilər")
    
    if st.button("🚀 İmtahanı Başlat / Yenilə"):
        st.session_state.question_data = get_new_question(subject, topic)
        st.session_state.show_explanation = False
        st.rerun()

    st.divider()
    st.metric("Topladığın Xal 🏆", f"{st.session_state.correct_count * 10} XP")

with col2:
    if st.session_state.question_data:
        q = st.session_state.question_data
        
        st.markdown(f"""<div class='question-container'>
            <h3>Sual:</h3>
            <p style='font-size: 1.3rem;'>{q['question']}</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("")
        choice = st.radio("Variantlardan birini seçin:", q['options'], index=None)
        
        col_check, col_next = st.columns(2)
        
        with col_check:
            if st.button("✅ Cavabı Yoxla"):
                if choice:
                    st.session_state.show_explanation = True
                    user_letter = choice[0] # Variantın ilk hərfi (A, B, C...)
                    if user_letter == q['answer']:
                        st.success("Təbriklər! Doğru cavabdır.")
                        st.session_state.correct_count += 1
                        st.balloons()
                    else:
                        st.error(f"Səhvdir! Doğru cavab: {q['answer']}")
                else:
                    st.warning("Zəhmət olmasa variant seçin.")
        
        with col_next:
            if st.button("Növbəti Sual ➡️"):
                st.session_state.question_data = get_new_question(subject, topic)
                st.session_state.show_explanation = False
                st.rerun()

        if st.session_state.show_explanation:
            st.info(f"**İzah:** {q['explanation']}")
    else:
        st.info("Sol tərəfdən mövzu yazıb 'İmtahanı Başlat' düyməsinə basaraq başlayın.")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren - Dinamik Öyrənmə Platforması")
