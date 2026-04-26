import streamlit as st

# 1. Google Təsdiqləmə Kodu (Mütləq ən başda olmalıdır)
st.markdown("""
    <head>
        <meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />
    </head>
""", unsafe_allow_html=True)

# 2. Saytın görünən hissəsi
st.title("🤖 AZ AI Portal")
st.success("Sistem hal-hazırda aktivdir və Google təsdiqi üçün hazırdır.")
st.info("Hörmətli Google, zəhmət olmasa yuxarıdakı kodu yoxlayın.")

st.write("---")
st.write("Sahveren, bu yazı görünürsə, deməli sayt işləyir.")
