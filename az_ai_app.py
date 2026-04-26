import streamlit as st

# 1. Google Təsdiqləmə Kodu (Mütləq ən başda və təmiz olmalıdır)
st.set_page_config(page_title="AZ AI Portal", layout="centered")

# Bu hissə Google-un axtardığı koddur
st.markdown('<meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" />', unsafe_allow_html=True)

# 2. Saytın Brauzerdə Görünən Hissəsi
st.title("🤖 AZ AI Rəsmi Portalı")
st.success("✅ Sayt Google təsdiqi üçün tam hazırdır!")
st.info("Sahveren, bu mətni görürsənsə, deməli saytın işləyir. İndi Google-da 'Təsdiqlə' düyməsinə bas.")

st.write("---")
st.write("Axtarış sistemlərinə qoşulduqdan sonra bütün funksiyalar bərpa olunacaq.")
