import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI - Sultan Portalı", page_icon="🧠", layout="wide")

# --- PREMIUM DİZAYN ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0d12; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161821 !important; border-right: 1px solid #2d2f3b; }
    .stChatFloatingInputContainer { background-color: #161821 !important; }
    .stChatMessage { background-color: #1f222d !important; border-radius: 15px; border: 1px solid #2d2f3b; margin-bottom: 10px; }
    .feature-card { background-color: #161821; padding: 20px; border-radius: 15px; border-left: 5px solid #7c3aed; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSİYA YADDAŞI (Sayt yenilənəndə itməməsi üçün) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "score" not in st.session_state:
    st.session_state.score = 0

# --- SOL MENYU (Sidebar) ---
with st.sidebar:
    st.markdown('<h1 style="color:#a78bfa;">AZ AI SULTAN</h1>', unsafe_allow_html=True)
    menu = st.radio("MENYU", [
        "🏠 Dashboard", 
        "🤖 REAL AI Çat", 
        "📚 Bütün Fənlər (Kitabxana)", 
        "📝 Canlı Testlər", 
        "🎮 İntellektual Oyunlar (Zəngin)", 
        "📤 Fayl Analizi (PDF/Şəkil)",
        "⚙️ Parametrlər"
    ])
    st.write("---")
    st.write(f"🏆 **Sultanın Xalı:** {st.session_state.score}")

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("Xoş gəldin, Sultan Sahveren! 👑")
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="feature-card"><b>Dillər</b><br>AZ, EN, RU, TR aktivdir.</div>', unsafe_allow_html=True)
    col2.markdown('<div class="feature-card"><b>AI Status</b><br>Beyin 100% aktivdir.</div>', unsafe_allow_html=True)
    col3.markdown('<div class="feature-card"><b>Sistem</b><br>Bütün fənlər qoşulub.</div>', unsafe_allow_html=True)
    
    st.subheader("Bu günün tədris planı")
    st.table(pd.DataFrame({
        "Fənn": ["Riyaziyyat", "AI Etikası", "İngilis Dili"],
        "Məqsəd": ["Törəmə testi", "Prompt Engineering", "Speaking"],
        "Status": ["⏳ Gözləyir", "✅ Hazırdır", "⏳ Gözləyir"]
    }))

# --- 2. REAL AI ÇAT ---
elif menu == "🤖 REAL AI Çat":
    st.title("🤖 AZ AI Canlı Müəllim")
    st.caption("Mən sadəcə robot deyiləm, sənin təhsil köməkçiyəm. Hər şeyi soruş!")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Sualını bura yaz, Sahveren..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Düşünürəm..."):
                time.sleep(1) # Reallıq hissi üçün
                # Bura AI məntiqi (Simulyasiya amma geniş cavablar)
                response = f"Sultan Sahveren, '{prompt}' mövzusu haqqında geniş məlumat bazama müraciət etdim. Bu mövzu üzrə dərsliklər və PDF-lər hazırdır. Sənə bu mövzuda test hazırlayım?"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- 3. BÜTÜN FƏNLƏR ---
elif menu == "📚 Bütün Fənlər (Kitabxana)":
    st.title("📚 Universal Kitabxana")
    search = st.text_input("Fənn və ya mövzu axtar (məs: Fizika)")
    
    cats = st.tabs(["Fənlər", "Dillər", "Lüğət"])
    with cats[0]:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.button("📐 Riyaziyyat (Bütün mövzular)")
            st.button("⚛️ Fizika (Mexanika, Optika)")
            st.button("🧬 Biologiya")
        with col_f2:
            st.button("📜 Tarix (Azərbaycan və Dünya)")
            st.button("🌍 Coğrafiya")
            st.button("💻 İnformatika və AI")
    with cats[1]:
        st.selectbox("Öyrənilən Dil:", ["English 🇺🇸", "Russian 🇷🇺", "Turkish 🇹🇷", "German 🇩🇪"])

# --- 4. CANLI TESTLƏR ---
elif menu == "📝 Canlı Testlər":
    st.title("📝 İmtahan Mərkəzi")
    st.write("Səviyyənə uyğun testlər yaradılır...")
    
    q1 = st.radio("Sual 1: Dünyada ilk Süni İntellekt proqramı hansı ildə yaradılıb?", ["1956", "1980", "2000", "1945"])
    if st.button("Testi Bitir"):
        if q1 == "1956":
            st.success("DOĞRUDUR! 🎯")
            st.session_state.score += 50
        else:
            st.error("YALNIŞDIR. Doğru cavab: 1956")

# --- 5. OYUNLAR (ZƏNGİN) ---
elif menu == "🎮 İntellektual Oyunlar (Zəngin)":
    st.title("🎮 Beyin Məşqi Oyunları")
    game = st.selectbox("Oyun seç:", ["Sürətli Riyaziyyat", "Söz Tapmacası", "Məntiq Labirinti"])
    
    if game == "Sürətli Riyaziyyat":
        n1, n2 = random.randint(100, 999), random.randint(100, 999)
        st.subheader(f"{n1} + {n2} = ?")
        user_ans = st.number_input("Cavabın:", step=1)
        if st.button("Yoxla"):
            if user_ans == n1 + n2:
                st.balloons()
                st.success("Möhtəşəm sürət!")
                st.session_state.score += 20

# --- 6. FAYL ANALİZİ ---
elif menu == "📤 Fayl Analizi (PDF/Şəkil)":
    st.title("📤 Fayl Mərkəzi")
    st.write("PDF dərsliklərini və ya test şəkillərini bura at, AI onları oxusun.")
    file = st.file_uploader("Fayl seçin", type=['pdf', 'png', 'jpg', 'docx'])
    if file:
        st.info(f"'{file.name}' yükləndi. AI hazırda sənədi təhlil edir...")

# --- 7. PARAMETRLƏR ---
elif choice == "⚙️ Parametrlər":
    st.title("⚙️ Sultan İdarəetmə Paneli")
    st.text_input("Admin Key:", value="Sahveren_Sultan_2026", disabled=True)
    st.color_picker("Saytın vurğu rəngini dəyiş", "#7c3aed")
    if st.button("Bütün Keşi Təmizlə"):
        st.session_state.messages = []
        st.success("Sistem sıfırlandı!")
