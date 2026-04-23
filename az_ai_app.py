import streamlit as st
from groq import Groq
import random
import time

# 1. Səhifə Ayarları və Vizual Stil
st.set_page_config(page_title="Akademiya AI - Premium", page_icon="🏫", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f1f3f6; }
    .stTabs [aria-selected="true"] { background-color: #1a237e !important; color: white !important; }
    .stButton>button { border-radius: 10px; height: 3em; font-weight: bold; }
    .info-card, .game-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .event-image { width: 100%; border-radius: 10px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Menecment
active_keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]

def call_ai(prompt, tokens=1500):
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
    return "Xəta oldu."

# --- QEYDİYYAT VƏ GİRİŞ SİSTEMİ ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_method' not in st.session_state: st.session_state.user_method = ""
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_test' not in st.session_state: st.session_state.current_test = None

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1a237e;'>🔐 Akademiya AI - Giriş Portalı</h1>", unsafe_allow_html=True)
    st.divider()
    
    login_method = st.radio("Daxil olma üsulu seçin:", ["📧 Email", "📱 Telefon Nömrəsi", "🌐 Google Hesabı"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if login_method == "📧 Email":
            email = st.text_input("Email ünvanınız:")
            pwd = st.text_input("Şifrə:", type="password")
        elif login_method == "📱 Telefon Nömrəsi":
            phone = st.text_input("Telefon nömrəniz:", placeholder="+994 50 000 00 00")
            code = st.text_input("SMS Kodu:")
        elif login_method == "🌐 Google Hesabı":
            st.markdown("""
                <div style='background-color: white; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #ddd;'>
                    <img src='https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_jfkdg/512/google.png' width='50'><br>
                    <b>Google ilə birbaşa bağlan</b>
                </div>
                """, unsafe_allow_html=True)
            google_connect = st.button("🔗 Google ilə Giriş")

    with col2:
        st.write("Giriş etmək üçün məlumatlarınızı doldurun.")
        if login_method != "🌐 Google Hesabı":
            if st.button("Daxil Ol 🚀"):
                # Sadə simulyasiya: Məlumat yazılıbsa girişə icazə ver
                if (login_method == "📧 Email" and email and pwd) or (login_method == "📱 Telefon Nömrəsi" and phone and code):
                    st.session_state.logged_in = True
                    st.session_state.user_method = email if email else phone
                    st.rerun()
        else:
            if 'google_connect' in locals() and google_connect:
                st.session_state.logged_in = True
                st.session_state.user_method = "Google User"
                st.rerun()

    st.stop() # Giriş etməyibsə aşağıdakı kodu görməsin

# --- ƏSAS PORTAL ---
st.markdown(f"<h1 style='text-align: center; color: #1a237e;'>🎓 Akademiya AI Premium</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("👤 Profil")
    st.write(f"**İstifadəçi:** {st.session_state.user_method}")
    st.metric("Topladığın Xal 🏆", f"{st.session_state.score} XP")
    st.divider()
    
    # 🌍 Dillərin və Fənlərin geniş siyahısı
    subject_list = [
        # Təbiət və Dəqiq Elmlər
        "Riyaziyyat", "Fizika", "Kimya", "Biologiya", "Coğrafiya", "İnformatika",
        # Humanitar Elmlər
        "Tarix", "Azərbaycan dili", "Ədəbiyyat", "Həyat bilgisi",
        # Xarici Dillər
        "İngilis dili", "Rus dili", "Alman dili", "Fransız dili", "İspan dili", "İtalyan dili", "Ərəb dili", "Türkiyə türkcəsi"
    ]
    subject = st.selectbox("Tədris sahəsi:", subject_list)
    topic = st.text_input("Mövzu:", value="Müstəqillik Günü")
    
    if st.button("🚪 Çıxış"):
        st.session_state.logged_in = False
        st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["📖 Öyrən & Şəkilli İzah", "📝 Sual Bankı", "🎮 Təhsil Oyunları", "🌐 Xarici Dil"])

# 📖 TAB 1: ÖYRƏN VƏ ŞƏKİLLİ İZAH
with tab1:
    col_info, col_img = st.columns([2, 1])
    
    with col_info:
        if st.button("Mövzunu Təsvir Et 📚"):
            with st.spinner("AI hadisəni canlandırır..."):
                # AI-dan həm məlumat, həm də şəkil təsviri istəyirik
                prompt = f"""{subject} fənnindən '{topic}' haqqında akademik məlumat ver. 
                Sonda isə bu hadisəni canlandıran möhtəşəm bir şəkil təsviri (English prompt) yaz."""
                result = call_ai(prompt, 3000)
                
                if "English prompt:" in result:
                    st.session_state.explanation = result.split("English prompt:")[0]
                    st.session_state.img_prompt = result.split("English prompt:")[1]
                else:
                    st.session_state.explanation = result
                    st.session_state.img_prompt = f"Historical scene: {topic}"
                st.rerun()

        if 'explanation' in st.session_state:
            st.markdown(f"<div class='info-card'>{st.session_state.explanation}</div>", unsafe_allow_html=True)
            # Səsli oxuma funksiyası (Sadə placeholder)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

    with col_img:
        st.write("🖼️ **Hadisənin Canlandırılması:**")
        # Real şəkil generatoru yoxdursa, mövzuya uyğun təsadüfi şəkil simulyasiyası
        if 'topic' in st.session_state and st.session_state.topic != topic:
             st.session_state.explanation = "" # Movzu deyişibse kohne izahi sil
             st.session_state.img_prompt = ""
        
        # Pulsuz şəkil simulyasiyası üçün LoremFlickr istifadə edirik
        img_url = f"https://loremflickr.com/640/480/{topic.replace(' ', ',')}"
        st.image(img_url, caption=f"AI-nin təsəvvüründə: {topic}", use_container_width=True)
        if 'img_prompt' in st.session_state and st.session_state.img_prompt:
             st.caption(f"**Təsvir Promptu:** {st.session_state.img_prompt}")

# 📝 TAB 2: SONSUZ SUAL
with tab2:
    def load_new_test():
        res = call_ai(f"{subject} fənnindən {topic} haqqında bir test hazırla. Format: SUAL: [..] A) [..] B) [..] C) [..] D) [..] DOĞRU: [Hərf] İZAH: [..]")
        if "DOĞRU:" in res:
            try:
                st.session_state.current_test = {
                    "q": res.split("SUAL:")[1].split("A)")[0].strip(),
                    "opts": [res.split("A)")[1].split("B)")[0].strip(), res.split("B)")[1].split("C)")[0].strip(), res.split("C)")[1].split("D)")[0].strip(), res.split("D)")[1].split("DOĞRU:")[0].strip()],
                    "ans": res.split("DOĞRU:")[1].split("İZAH:")[0].strip(),
                    "expl": res.split("İZAH:")[1].strip()
                }
            except: pass

    col_test, col_next = st.columns([3, 1])
    
    with col_test:
        if st.button("Yeni Sual 🔄"):
            load_new_test()
            st.rerun()

        if st.session_state.current_test:
            t = st.session_state.current_test
            st.info(f"**Sual:** {t['q']}")
            choice = st.radio("Variant seç:", ["A", "B", "C", "D"], key="test_radio")
            if st.button("✅ Yoxla"):
                if choice == t['ans']:
                    st.success(f"Düzdür! {t['expl']}")
                    st.session_state.score += 10
                    st.balloons()
                else:
                    st.error(f"Səhvdir! Doğru cavab: {t['ans']}. İzah: {t['expl']}")

# 🎮 TAB 3: TƏHSİL OYUNLARI
with tab3:
    st.subheader("🎲 AI ilə Təhsil Oyunları")
    game_type = st.radio("Oyun növü seçin:", ["🔍 Söz Tapmaca", "📜 Tarix Viktorinası", "🧠 Məntiq Yarışı"])
    
    if st.button("Oyunu Başlat 🕹️"):
        with st.spinner("AI oyun qurur..."):
            game_prompt = call_ai(f"{subject} fənnindən {topic} mövzusunda şagird üçün {game_type} oyunu hazırla.")
            st.markdown(f"<div class='game-card'>{game_prompt}</div>", unsafe_allow_html=True)

# 🌐 TAB 4: XARİCİ DİL (MÜƏLLİM)
with tab3:
    st.subheader("🇬🇧 AI Xarici Dil Müəllimi")
    lang_topic = st.text_input("Öyrənmək istədiyiniz mövzu (məs: At Home):", value="Travel")
    if st.button("Dərsə Başla 🎧"):
        with st.spinner(f"AI {subject} müəllimi dərsi hazırlayır..."):
            lesson = call_ai(f"Mən {subject} öyrənmək istəyirəm. Mövzu: {lang_topic}. Mənə ən vacib sözləri, nümunə cümlələri və bir qısa dialoq yaz. Həm original, həm də Azərbaycan dilində izah et.")
            st.markdown(lesson)

st.markdown("---")
st.caption("© 2026 Akademiya AI | Sahveren Premium")
