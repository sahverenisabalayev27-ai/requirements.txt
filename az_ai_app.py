import streamlit as st
import pandas as pd
import random
import time

# --- KONFİQURASİYA ---
st.set_page_config(page_title="AZ AI - Universal Təhsil Portalı", page_icon="🎓", layout="wide")

# --- DİZAYN (Dark Mode & Premium Look) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0d12; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161821 !important; border-right: 1px solid #2d2f3b; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #a0a5b9; background-color: #161821; border-radius: 10px; padding: 10px 20px; border: 1px solid #2d2f3b; }
    .stTabs [aria-selected="true"] { background-color: #7c3aed !important; color: white !important; }
    .feature-card { background-color: #161821; padding: 25px; border-radius: 15px; border: 1px solid #2d2f3b; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- SOL MENYU ---
with st.sidebar:
    st.markdown('<h1 style="color:#a78bfa;">AZ AI EDU</h1>', unsafe_allow_html=True)
    st.info("İstifadəçi: **Sultan Sahveren**")
    
    choice = st.radio("BÖLMƏLƏR", [
        "🏠 Dashboard", 
        "🤖 AI Müəllim (Ağıllı)", 
        "📚 Fənlər və Kitabxana", 
        "📝 Test Mərkəzi", 
        "🎮 İntellektual Oyunlar", 
        "📤 Fayl Mübadiləsi",
        "⚙️ Parametrlər"
    ])
    
    st.write("---")
    st.caption("Dil: AZ / EN / RU / TR")
    st.progress(85, text="Aylıq Hədəf")

# --- 1. DASHBOARD ---
if choice == "🏠 Dashboard":
    st.title("Xoş gəldiniz, Sultan!")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ümumi Fənn", "14", "+2")
    col2.metric("Həll olunan test", "1,420", "+12%")
    col3.metric("AI Sual-Cavab", "345", "Aktiv")
    col4.metric("Reytinq", "#1", "Sultan")

# --- 2. AI MÜƏLLİM (Real AI Məntiqi) ---
elif choice == "🤖 AI Müəllim (Ağıllı)":
    st.title("💬 AZ AI Universal Köməkçi")
    st.write("İstənilən dildə soruş, sənədini analiz etdir və ya dərsi izah etdir.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nəyi öyrənmək istəyirsən?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Süni İntellekt simulyasiyası (Gələcəkdə bura API qoşacağıq)
            response = f"Sultan Sahveren, '{prompt}' haqqında araşdırma edirəm... Hazırda dərslikləri skan edirəm. Bu mövzu sabahkı imtahanında vacib ola bilər!"
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- 3. FƏNLƏR VƏ KİTABXANA ---
elif choice == "📚 Fənlər və Kitabxana":
    st.title("📚 Bütün Fənlər")
    tab1, tab2, tab3 = st.tabs(["Təbiət Elmləri", "Humanitar", "Dillər"])
    
    with tab1:
        st.checkbox("Riyaziyyat")
        st.checkbox("Fizika")
        st.checkbox("Biologiya")
    with tab2:
        st.checkbox("Tarix")
        st.checkbox("Coğrafiya")
    with tab3:
        st.selectbox("Öyrənmək istədiyiniz dil:", ["Azərbaycan", "İngilis", "Rus", "Türk", "Alman", "Fransız"])

# --- 4. TEST MƏRKƏZİ ---
elif choice == "📝 Test Mərkəzi":
    st.title("📝 Özünü Sına")
    fenn = st.selectbox("Fənn seç:", ["Riyaziyyat", "Məntiq", "İngilis dili"])
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.write(f"**Sual:** {fenn} üzrə növbəti sual gəlir...")
    ans = st.radio("Doğru variantı seçin:", ["A variantı", "B variantı", "C variantı", "D variantı"])
    if st.button("Cavabı Yoxla"):
        st.balloons()
        st.success("Möhtəşəm! Sultan həmişə düz tapır.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. İNTELLEKTUAL OYUNLAR ---
elif choice == "🎮 İntellektual Oyunlar":
    st.title("🎮 Beyin Gimnastikası")
    game_type = st.selectbox("Oyun növü:", ["Sürətli Hesablama", "Söz Tapmacası", "Tarixi Faktlar"])
    
    if game_type == "Sürətli Hesablama":
        num1 = random.randint(50, 200)
        num2 = random.randint(50, 200)
        st.subheader(f"{num1} x {num2} = ?")
        st.text_input("Nəticəni bura yaz...")
        st.button("Təsdiqlə")

# --- 6. FAYL MÜBADİLƏSİ ---
elif choice == "📤 Fayl Mübadiləsi":
    st.title("📤 Fayl və PDF Mərkəzi")
    uploaded_file = st.file_uploader("Dərslik və ya şəkil yüklə (AI analiz etsin)", type=['pdf', 'png', 'jpg', 'docx'])
    if uploaded_file:
        st.success(f"'{uploaded_file.name}' uğurla yükləndi. AI tərəfindən oxunur...")

# --- 7. PARAMETRLƏR ---
elif choice == "⚙️ Parametrlər":
    st.title("⚙️ Sistem Ayarları")
    st.toggle("Gecə Rejimi (Aktiv)")
    st.toggle("Səsli Cavablar")
    if st.button("Sistemi Yenilə"):
        with st.spinner('Yenilənir...'):
            time.sleep(2)
            st.success("Bütün fənlər üzrə bazalar yeniləndi!")
