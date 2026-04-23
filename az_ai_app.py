import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI - Sonsuz Sual Bankı", page_icon="🎓", layout="wide")

# CSS - Vizual olaraq daha cəlbedici dizayn
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stRadio > label { font-size: 1.1rem; color: #0d47a1; font-weight: 600; }
    .question-card {
        background: white; 
        padding: 2rem; 
        border-radius: 20px; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 10px solid #1a237e;
    }
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment (Çoxlu Açar Sistemi)
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt):
    random.shuffle(active_keys)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                max_tokens=1500
            )
            return resp.choices[0].message.content
        except:
            continue
    return None

# 3. Sual Yaratma Funksiyası (Dinamik Diversifikasiya)
def get_dynamic_question(subject, topic):
    # Bu təlimat botun hər dəfə tam fərqli sual verməsini təmin edir
    aspects = ["tarixi tarixlər", "əsas şəxsiyyətlər", "səbəb-nəticə əlaqələri", "coğrafi mövqe", "mədəni nailiyyətlər", "terminologiya", "az tanınan faktlar"]
    selected_aspect = random.choice(aspects)
    
    prompt = f"""
    Sən peşəkar bir imtahan hazırlayan mütəxəssissən.
    Fənn: {subject}
    Mövzu: {topic}
    İstiqamət: Xüsusilə '{selected_aspect}' üzərində fokuslanaraq unikal bir sual hazırla.
    
    Qaydalar:
    - Sual əvvəlki standart suallardan tamamilə fərqli və düşündürücü olsun.
    - Format mütləq belə olmalıdır:
    SUAL: [Sual bura]
    A) [Variant]
    B) [Variant]
    C) [Variant]
    D) [Variant]
    E) [Variant]
    DOĞRU_CAVAB: [Yalnız hərfi yaz]
    İZAH: [Şagirdin mövzunu tam anlaması üçün geniş akademik izah]
    """
    return call_ai(prompt)

# 4. Sessiya İdarəetməsi
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'checked' not in st.session_state:
    st.session_state.checked = False

# 5. İnterfeys
st.markdown("<h1 style='text-align: center; color: #1a237e;'>🏫 Milli Sonsuz Sual Platforması</h1>", unsafe_allow_html=True)

col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.markdown("### 🛠️ Parametrlər")
    subject = st.selectbox("Fənn:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "Coğrafiya"])
    topic = st.text_input("Mövzu daxil et:", value="Azərbaycan Tarixi")
    
    if st.button("🆕 Yeni Sınağa Başla"):
        raw_res = get_dynamic_question(subject, topic)
        if raw_res and "DOĞRU_CAVAB:" in raw_res:
            try:
                st.session_state.current_q = {
                    "question": raw_res.split("SUAL:")[1].split("A)")[0].strip(),
                    "options": [
                        "A) " + raw_res.split("A)")[1].split("B)")[0].strip(),
                        "B) " + raw_res.split("B)")[1].split("C)")[0].strip(),
                        "C) " + raw_res.split("C)")[1].split("D)")[0].strip(),
                        "D) " + raw_res.split("D)")[1].split("E)")[0].strip(),
                        "E) " + raw_res.split("E)")[1].split("DOĞRU_CAVAB:")[0].strip()
                    ],
                    "correct": raw_res.split("DOĞRU_CAVAB:")[1].split("İZAH:")[0].strip(),
                    "explanation": raw_res.split("İZAH:")[1].strip()
                }
                st.session_state.checked = False
                st.rerun()
            except:
                st.error("Sual emal edilərkən xəta oldu, yenidən yoxlayın.")

    st.divider()
    st.markdown(f"### 🏆 Sənin Xalın: **{st.session_state.score * 10} XP**")

with col_main:
    if st.session_state.current_q:
        q = st.session_state.current_q
        
        st.markdown(f"""<div class='question-card'>
            <h4 style='color: #1565c0;'>Sual:</h4>
            <p style='font-size: 1.25rem;'>{q['question']}</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("")
        user_choice = st.radio("Düzgün variantı seçin:", q['options'], index=None)
        
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            if st.button("✅ Cavabı Yoxla"):
                if user_choice:
                    st.session_state.checked = True
                    if user_choice[0] == q['correct']:
                        st.success(f"Düzgün! Variant {q['correct']}")
                        st.session_state.score += 1
                        st.balloons()
                    else:
                        st.error(f"Səhvdir! Doğru cavab: {q['correct']}")
                else:
                    st.warning("Zəhmət olmasa seçim edin.")
        
        with col_act2:
            if st.button("Növbəti Sual ➡️"):
                raw_res = get_dynamic_question(subject, topic)
                if raw_res and "DOĞRU_CAVAB:" in raw_res:
                    st.session_state.current_q = {
                        "question": raw_res.split("SUAL:")[1].split("A)")[0].strip(),
                        "options": [
                            "A) " + raw_res.split("A)")[1].split("B)")[0].strip(),
                            "B) " + raw_res.split("B)")[1].split("C)")[0].strip(),
                            "C) " + raw_res.split("C)")[1].split("D)")[0].strip(),
                            "D
