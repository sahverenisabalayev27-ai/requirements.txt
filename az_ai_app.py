import streamlit as st
import streamlit.components.v1 as components

# 1. Google-un axtardığı o xüsusi kod (HEAD hissəsi üçün)
# Bu kod Google botunun sayta girən kimi gördüyü ilk şey olacaq
st.markdown(
    f'<p style="display:none;"><meta name="google-site-verification" content="fTstY8SCtoJrmRvDDFjCZOUpBBJnDrdVNYSwSwcL0JY" /></p>',
    unsafe_allow_html=True
)

# 2. Saytın vizual quruluşu
st.set_page_config(page_title="AZ AI Portal", page_icon="🤖")

st.title("🤖 AZ AI Rəsmi Portalı")
st.divider()

st.success("✅ Sayt Google Axtarış Konsolu üçün optimizasiya olundu.")
st.info("Sahveren, indi Google Search Console-a qayıt və **HTML Etiketi** (fayl yox, etiket) üsulu ilə 'Təsdiqlə' düyməsinə bas.")

st.write("---")
st.write("Mülkiyyət təsdiqləndikdən sonra bütün o mükəmməl funksiyaları (oyunlar, təhsil sistemi) buraya əlavə edəcəyik.")
