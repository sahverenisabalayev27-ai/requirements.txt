import streamlit as st
import google.generativeai as genai

st.title("Sultan AI: Diaqnoz Rejimi")

api_key = st.sidebar.text_input("Açarı bura yapışdırın:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Sənin açarının icazə verdiyi bütün modelləri siyahılayırıq
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write("Sizin açarın dəstəklədiyi modellər:")
        st.success(models)
    except Exception as e:
        st.error(f"Xəta baş verdi: {e}")
