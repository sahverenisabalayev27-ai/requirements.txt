import streamlit as st

# --- 1. GOOGLE TƏSDİQ MODULU (GÜCLÜ ÜSUL) ---
# Google botu sayta daxil olanda bu kodu axtaracaq
st.markdown('<meta name="google-site-verification" content="googlee9f98e586bf85b6c.html" />', unsafe_allow_html=True)

# Alternativ olaraq, əgər Google birbaşa faylı oxumaq istəsə:
query_params = st.query_params
if "file" in query_params and query_params["file"] == "googlee9f98e586bf85b6c.html":
    st.write("google-site-verification: googlee9f98e586bf85b6c.html")
    st.stop()

# --- 2. SULTAN MEDIA AI - BİZNES PANELİ ---
st.set_page_config(page_title="Sultan Media AI", page_icon="💰", layout="wide")

# Premium Dizayn (Qaranlıq Stil)
st.markdown("""
    <style>
    .stApp { background-color: #0c0d12; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161821 !important; border-right: 1px solid #2d2f3b; }
    .main-title { color: #a78bfa; font-size: 40px; font-weight: bold; text-align: center; }
    .feature-card { background-color: #161821; padding: 25px; border-radius: 15px; border: 1px solid #2d2f3b; transition: 0.3s; }
    .feature-card:hover { border-color: #7c3aed; }
    .stButton>button { background-color: #7c3aed; color: white; border-radius: 10px; height: 3em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 style="color:#a78bfa;">SULTAN MEDIA AI</h2>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENYU", ["🚀 Başlanğıc", "✍️ AI Copywriter", "📊 Reklam Analizi", "💎 Premium Plan"])
    st.write("---")
    st.info("Status: Google Təsdiqləmə Gözlənilir...")

# --- DASHBOARD ---
if menu == "🚀 Başlanğıc":
    st.markdown('<p class="main-title">Biznesinizi AI ilə Böyüdün</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #6b7280;'>Sultan Sahveren tərəfindən idarə olunan rəsmi biznes portalı</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2
