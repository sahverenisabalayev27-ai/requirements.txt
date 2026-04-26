import streamlit as st

# 1. BU HİSSƏ GOOGLE BOTUNU TUTMAQ ÜÇÜNDÜR
# Google botu sayta müxtəlif yollarla sızmağa çalışır, biz hər yolu bağlayırıq.
st.set_page_config(page_title="Sultan Media AI", layout="wide")

# HTML-in ən başına etiketi yerləşdiririk
st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />
    </head>
    """, 
    unsafe_allow_html=True
)

# Əgər Google "fayl" metodunu yoxlayırsa, ekrana birbaşa mətni çıxarırıq
st.write(f"")

# 2. İSTİFADƏÇİLƏR ÜÇÜN GÖRÜNÜŞ
st.title("🚀 Sultan Media AI")
st.success("Sistem tam gücü ilə işləyir!")

st.info("Hörmətli istifadəçi, Sultan Media AI portalına xoş gəldiniz. Hazırda sistem Google təhlükəsizlik yoxlamasından keçir.")

# 3. GOOGLE ÜÇÜN GİZLİ MƏTN (Botlar bunu oxuya bilir)
st.write("Verification Code: fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY")
