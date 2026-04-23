import streamlit as st
from groq import Groq
import random
import requests

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="Akademiya AI - Global", page_icon="🌐", layout="wide")

# Müasir Premium Dizayn
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px; background-color: #ffffff; border-radius: 12px;
        font-weight: bold; font-size: 16px; border: 1px solid #ddd;
    }
    .stTabs [aria-selected="true"] { background-color: #1a237e !important; color: white !important; }
    .content-box { 
        background: white; padding: 40px; border-radius: 25px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); line-height: 2; color: #333;
    }
    .image-caption { text-align: center; font-style: italic; color: #555; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API və Sistem Məntiqi
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def get_ai_response(prompt, length="long"):
    random.shuffle(active_keys)
    # Professional Müəllim Təlimatı
    system_instruction = "Sən dünyanın ən savadlı Azərbaycanlı professorusan. Məlumatı ən az 3000 sözlə, dərin akademik detallarla, başlıqlarla və maraqlı faktlarla izah etməlisən."
    
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=4000 if length == "long" else 1500
            )
            return resp.choices[0].message.content
        except: continue
    return "Limit dolub, az sonra yoxlayın."

# 3. Giriş Sistemi (Email, Telefon, Google)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'score' not in st.session_state: st.session_state.score = 0

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🌐 Akademiya AI Giriş</h1>", unsafe_allow_html=True)
    login_type = st.radio("Giriş üsulu:", ["Email", "Telefon", "Google"], horizontal=True)
    
    with st.container():
        user_id = st.text_input(f"{login_type} daxil edin:")
        pwd = st.text_input("Şifrə:", type="password")
        if st.button("Giriş Et 🚀"):
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_name = user_id
                st.rerun()
    st.stop()

# --- ƏSAS PORTAL ---
st.sidebar.title("👤 Profilim")
st.sidebar.info(f"İstifadəçi: {st.session_state.user_name}")
st.sidebar.metric("Toplanmış XP 🏆", f"{st.session_state.score} XP")

subject_list = [
    "Tarix", "Azərbaycan dili", "Riyaziyyat", "Fizika", "Kimya", "Biologiya", 
    "Coğrafiya", "İngilis dili", "Rus dili", "Fransız dili", "Alman dili", "İspan dili"
]
sel_subject = st.sidebar.selectbox("Fənn seç:", subject_list)
sel_topic = st.sidebar.text_input("Mövzu:", "Böyük Partlayış və Kainat")

tab_edu, tab_test, tab_game = st.tabs(["📖 Akademik Öyrənmə", "📝 Sual Bankı", "🎮 Təhsil Oyunları"])

# 📖 TAB 1: AKADEMİK ÖYRƏNMƏ (MÖHTƏŞƏM İZAH + REAL ŞƏKİL)
with tab_edu:
    if st.button("Külliyyatı Yüklə (Məlumat + Şəkil) 🚀"):
        with st.spinner("Professor mövzunu araşdırır..."):
            # Məlumat
            content = get_ai_response(f"Mövzu: {sel_subject} - {sel_topic}. Bu mövzunu ən az 3000 sözlə, inanılmaz geniş və maraqlı izah et.")
            st.session_state.last_content = content
            
            # Şəkil (Mövzuya uyğun şəkili Unsplash vasitəsilə çəkirik)
            img_query = sel_topic.replace(" ", "+")
            st.session_state.last_img = f"https://source.unsplash.com/1600x900/?{img_query},science,history"
            
    if 'last_content' in st.session_state:
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.markdown(f"<div class='content-box'><h1>{sel_topic}</h1><br>{st.session_state.last_content}</div>", unsafe_allow_html=True)
        
        with col_side:
            st.image(st.session_state.last_img, use_container_width=True)
            st.markdown("<p class='image-caption'>Mövzuya uyğun süni intellekt tərəfindən seçilmiş vizual təsvir</p>", unsafe_allow_html=True)
            
            # Səsli Oxuma (Professional Səs Simulyasiyası)
            st.write("🎙️ **Müəllim Səsi (Oğlan):**")
            audio_text = st.session_state.last_content[:300] # İlk 300 simvolu səsləndiririk
            # TTS API (Google) istifadə edirik
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={audio_text}&tl=tr&client=tw-ob"
            st.audio(tts_url)

# 📝 TAB 2: SUAL BANKI (TEST VƏ AÇIQ SUAL)
with tab_test:
    st.subheader("📝 Növbəti Səviyyə Sınaqlar")
    if st.button("Yeni Sual Gətir 🔄"):
        type_q = random.choice(["test", "aciq"])
        if type_q == "test":
            res = get_ai_response(f"{sel_subject} - {sel_topic} haqqında çətin test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [..] İZAH: [..]", "short")
            st.session_state.current_q = {"type": "test", "data": res}
        else:
            res = get_ai_response(f"{sel_subject} - {sel_topic} haqqında yazılı cavab tələb edən açıq sual ver.", "short")
            st.session_state.current_q = {"type": "aciq", "data": res}
            
    if 'current_q' in st.session_state:
        q = st.session_state.current_q
        st.markdown(f"<div class='content-box'>{q['data']}</div>", unsafe_allow_html=True)
        
        if q['type'] == "test":
            ans = st.radio("Variant seç:", ["A", "B", "C", "D"])
            if st.button("Yoxla ✅"):
                if ans in q['data']: 
                    st.success("Düzgün! +10 XP")
                    st.session_state.score += 10
                    st.balloons()
        else:
            user_text = st.text_area("Cavabınızı bura yazın:")
            if st.button("Müəllimə Göndər 📤"):
                eval_res = get_ai_response(f"Sual: {q['data']}\nŞagirdin cavabı: {user_text}\nBunu yoxla və rəy ver.")
                st.info(eval_res)
                st.session_state.score += 20

# 🎮 TAB 3: OYUNLAR (AI ROLEPLAY)
with tab_game:
    st.subheader("🎮 Tarixi Şəxsiyyətlərlə Söhbət")
    person = st.text_input("Kiminlə danışmaq istəyirsən? (məs: Şah İsmayıl, Albert Einstein):")
    if st.button("Oyuna Başla 🎭"):
        chat = get_ai_response(f"Sən {person} rolundasan. Şagirdlə onun dövrü haqqında maraqlı danış və bir sirr ver.")
        st.write(chat)

st.markdown("---")
st.caption("© 2026 Akademiya AI | Premium Təhsil Layihəsi")
