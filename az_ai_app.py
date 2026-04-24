import streamlit as st
from groq import Groq
import random

# 1. GOOGLE ÜÇÜN SEO VƏ SAYT AYARLARI
st.set_page_config(
    page_title="AZ AI | Azərbaycanın Süni İntellekt Təhsil Portalı", 
    page_icon="🇦🇿", 
    layout="wide"
)

# Google Botları üçün Meta Tag-lar (Pulsuz SEO)
st.markdown("""
    <head>
        <title>AZ AI - Sahveren Premium</title>
        <meta name="description" content="AZ AI ilə Azərbaycan dilində süni intellekt təhsili, coğrafiya oyunları və 5 AZN-ə premium dərslər.">
        <meta name="keywords" content="AZ AI, Sahveren, Süni İntellekt Azərbaycan, Bayraq oyunu, Onlayn təhsil">
        <meta name="robots" content="index, follow">
    </head>
""", unsafe_allow_html=True)

# --- QALAN KODUN (Dünənki sistemin eynisi) ---
# Buradan aşağıda dünən yazdığımız kodları (Giriş, Oyunlar, Admin Panel) saxla.
