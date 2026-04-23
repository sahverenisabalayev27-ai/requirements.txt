import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları
st.set_page_config(page_title="Akademiya AI - Tam Təhsil Portalı", page_icon="🎓", layout="wide")

# Müasir və Təhsil Fokuslu CSS
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #1a237e; color: white !important; }
    .info-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); line-height: 1.8; }
    .question-card { background: #ffffff; padding: 25px; border-radius: 20px; border-left: 10px solid #43a047; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. API Açar Hovuzu
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
    return None

# 3. Məntiqi Funksiyalar
def get_lesson_content(subject, topic):
    prompt = f"{subject} fənnindən {topic} haqqında ən az 2000 sözdən ibarət, başlıqlarla zəngin, elmi və ensiklopediya səviyyəsində geniş məlumat yaz. Azərbaycan dilində olsun."
    return call_ai(prompt, 4000)

def get_unique_question(subject, topic):
    prompt = f"""{subject} fənnindən {topic} mövzusunda əvvəlkilərdən fərqli, unikal bir test sualı hazırla. 
    Format: SUAL: [mətni] A) [..] B) [..] C) [..] D) [..] E) [..] DOĞRU_CAVAB: [Hərf] İZAH: [Geniş izah]"""
    res = call_ai(prompt, 1500)
    if res and "DOĞRU_CAVAB:" in res:
        try:
            return {
                "q": res.split("SUAL:")[1].split("A)")[0].strip(),
                "opts": ["A) "+res.split("A)")[1].split("B)")[0].strip(), "B) "+res.split("B)")[1].split("C)")[0].strip(), "C) "+res.split("C)")[1].split("D)")[0].strip(), "D) "+res.split("D)")[1].split("E)")[0].strip(), "E) "+res.split("E)")[1].split("DOĞRU_CAVAB:")[0].strip()],
                "ans": res.split("DOĞRU_CAVAB:")[1].split("İZAH:")[0].strip(),
                "expl": res.split("İZAH:")[1].strip()
            }
        except: return None
    return None

# 4. İnterfeys
st.markdown("<h1 style='text-align: center; color: #1a237e;'>🏫 Akademiya AI: Tam Təhsil Portalı</h1>", unsafe_allow_html=True)

# Session State
if 'lesson_data' not in st.session_state: st.session_state.lesson_data = ""
if 'current_test' not in st.session_state: st.session_state.current_test = None
if 'score' not in st.session_state: st.session_state.score = 0

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=80)
    st.title("İdarəetmə Paneli")
    subject = st.selectbox("Fənn:", ["Tarix", "Azərbaycan dili", "Riyaziyyat", "Biologiya", "Fizika", "Kimya", "Coğrafiya"])
    topic = st.text_input("Mövzu daxil et:", value="Azərbaycanın coğrafiyası")
    
    if st.button("🚀 Mövzunu və Sualları Yüklə"):
        with st.spinner("Ensiklopedik məlumat və suallar hazırlanır..."):
            st.session_state.lesson_data = get_lesson_content(subject, topic)
            st.session_state.current_test = get_unique_question(subject, topic)
            st.rerun()
    
    st.divider()
    st.metric("Topladığın Xal 🏆", f"{st.session_state.score * 10} XP")

# Əsas Hissə (Tablar)
tab1, tab2 = st.tabs(["📖 Məlumat Xanası (Öyrən)", "✍️ Sual Xanası (Sına)"])

with tab1:
    if st.session_state.lesson_data:
        st.markdown(f"<div class='info-card'>{st.session_state.lesson_data}</div>", unsafe_allow_html=True)
    else:
        st.info("Sol tərəfdən mövzunu yazıb 'Yüklə' düyməsinə basaraq dərslərə başlaya bilərsiniz.")

with tab2:
    if st.session_state.current_test:
        t = st.session_state.current_test
        st.markdown(f"<div class='question-card'><h3>Sual:</h3><p style='font-size: 1.2rem;'>{t['q']}</p></div>", unsafe_allow_html=True)
        
        choice = st.radio("Variantını seç:", t['opts'], index=None)
        
        col_check, col_next = st.columns(2)
        with col_check:
            if st.button("✅ Yoxla"):
                if choice and choice[0] == t['ans']:
                    st.success(f"Düzdür! {t['ans']}")
                    st.session_state.score += 1
                    st.balloons()
                else:
                    st.error(f"Səhvdir! Doğru cavab: {t['ans']}")
                st.info(f"📚 **İzah:** {t['expl']}")
        
        with col_next:
            if st.button("Növbəti Sual ➡️"):
                st.session_state.current_test = get_unique_question(subject, topic)
                st.rerun()
    else:
        st.warning("Əvvəlcə mövzunu yükləməlisiniz.")

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren - Mükəmməl Öyrənmə Təcrübəsi")
