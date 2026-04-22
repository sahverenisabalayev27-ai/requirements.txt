import streamlit as st
from groq import Groq

# Səhifənin vizual tənzimləmələri
st.set_page_config(page_title="AI Məktəbim", page_icon="🎓", layout="centered")

# Dizaynı gözəlləşdirək
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    h1 {
        color: #2E7D32;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 AI Məktəbim")
st.markdown("<p style='text-align: center;'>Sənin fərdi süni intellekt müəllimin. İstədiyin mövzunu soruş, sadə dildə öyrən!</p>", unsafe_allow_html=True)
st.divider()

# API Açarını Secrets-dən oxuyuruq
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # İstifadəçi girişləri
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Fənni seç:", 
                                 ["Riyaziyyat", "Azərbaycan dili", "Tarix", "Coğrafiya", "Biologiya", "Fizika", "İngilis dili"])
        with col2:
            level = st.selectbox("Səviyyəni seç:", ["Aşağı sinif", "Orta sinif", "Abituriyent"])

        topic = st.text_input("Mövzunun adını yaz (məsələn: Səfəvilər dövləti və ya Fotosintez):")

        if st.button("Müəllim, İzah Et! 🍎"):
            if topic:
                with st.spinner("Müəllim izah hazırlayır, bir neçə saniyə gözlə..."):
                    
                    # Süni intellektə "Müəllim" rolu veririk
                    prompt = f"""
                    Sən mehriban, səbirli və peşəkar bir Azərbaycanlı müəllimsən. 
                    Fənn: {subject}
                    Səviyyə: {level}
                    Mövzu: {topic}
                    
                    Tapşırıq:
                    1. Mövzunu şagirdin seçdiyi səviyyəyə uyğun olaraq çox sadə və maraqlı dildə izah et. 
                    2. İzahın içində vacib terminləri qalın (bold) yaz.
                    3. İzahın sonunda şagirdin biliyini yoxlamaq üçün 3 dənə maraqlı TEST sualı (variantları ilə) hazırl.
                    4. Sonda şagirdə motivasiya verici bir cümlə yaz.
                    Dil: Azərbaycan dili.
                    """

                    # Groq ilə sorğu göndəririk
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sən savadlı bir müəllimsən."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile", # Ən güclü Llama modeli
                    )
                    
                    response_text = chat_completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.success("Dərsimiz hazırdır! 👇")
                    st.markdown(response_text)
                    st.balloons()
            else:
                st.warning("Zəhmət olmasa mövzu adını daxil et.")
                
    except Exception as e:
        st.error(f"Sistemdə xəta baş verdi: {e}")
else:
    st.error("GROQ_API_KEY tapılmadı! Lütfən Streamlit Settings > Secrets hissəsinə açarı əlavə et.")

st.sidebar.markdown("### 📱 Haqqımızda")
st.sidebar.info("Bu layihə Sahveren tərəfindən təhsilə dəstək məqsədilə hazırlanıb. Süni intellekt köməkliyi ilə dərslər artıq daha maraqlıdır!")
