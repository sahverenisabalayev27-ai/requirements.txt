import streamlit as st
import pandas as pd
import random

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="AZ AI - Təhsil Portalı", page_icon="🎓", layout="wide")

# --- CUSTOM CSS (Göndərdiyin şəkildəki qaranlıq dizayn) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0d12 !important; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161821 !important; border-right: 1px solid #2d2f3b; }
    .stButton>button { background-color: #7c3aed; color: white; border-radius: 8px; width: 100%; }
    .course-card { background-color: #161821; padding: 20px; border-radius: 15px; border: 1px solid #2d2f3b; margin-bottom: 10px; }
    .profile-avatar { width: 45px; height: 45px; background-color: #db2777; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SOL MENYU (Sidebar) ---
with st.sidebar:
    st.markdown('<h1 style="color:#a78bfa; font-size:26px;">AZ AI Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7280; font-size:12px; margin-top:-15px;">TƏHSİL VƏ İNKİŞAF</p>', unsafe_allow_html=True)
    
    st.write("---")
    menu = st.radio("ƏSAS MENYU", ["🏠 İcmal", "💬 AI Köməkçi", "📚 Kurslarım", "🧠 Beyin Məşqi", "⚙️ Parametrlər"])
    
    # Sultan Profili (Aşağıda)
    st.write("---")
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div class="profile-avatar">S</div>
            <div>
                <b>Sahveren</b><br>
                <span style="color:#6b7280; font-size:12px;">Portal Rəhbəri</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ANA MƏZMUN ---

if menu == "🏠 İcmal":
    st.title("Xoş gəldin, Sahveren!")
    st.write("Bu gün öyrənmək üçün əla gündür.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="course-card">🏆 <b>Xalın</b><br><span style="font-size:25px;">1,250</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="course-card">📖 <b>Bitən Dərs</b><br><span style="font-size:25px;">12</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="course-card">🔥 <b>Aktivlik</b><br><span style="font-size:25px;">5 Gün</span></div>', unsafe_allow_html=True)

    st.subheader("Davam edən təlimlər")
    st.info("🚀 Süni İntellektin Əsasları - 65% tamamlanıb")

elif menu == "💬 AI Köməkçi":
    st.title("💬 AZ AI Müəllim")
    st.write("İstənilən mövzuda sual ver, dərhal izah edim.")
    quest = st.text_input("Sualınızı bura yazın...")
    if quest:
        st.chat_message("user").write(quest)
        st.chat_message("assistant").write(f"Mükəmməl sualdır! '{quest}' mövzusunda sənə kömək edə bilərəm. Hazırda sistemim yenilənir, amma dərslərinə fokuslanmağını tövsiyə edirəm.")

elif menu == "📚 Kurslarım":
    st.title("📚 Tədris Materialları")
    courses = ["Python Proqramlaşdırma", "Riyaziyyat (Ali)", "Xarici Dil - İngilis", "Süni İntellekt Etikası"]
    for c in courses:
        with st.expander(f"📘 {c}"):
            st.write(f"{c} kursu üzrə video dərslər və testlər burada yerləşir.")
            st.button(f"{c} dərsinə başla")

elif menu == "🧠 Beyin Məşqi":
    st.title("🎮 Riyazi Sürət Oyunu")
    if 'n1' not in st.session_state:
        st.session_state.n1, st.session_state.n2 = random.randint(10, 50), random.randint(10, 50)
    
    st.write(f"Sual: **{st.session_state.n1} + {st.session_state.n2}**")
    ans = st.number_input("Cavabınız:", step=1)
    if st.button("Yoxla"):
        if ans == st.session_state.n1 + st.session_state.n2:
            st.success("Düzdür! +10 Xal! 🎉")
            del st.session_state.n1 # Yeni sual üçün
        else:
            st.error("Səhvdir, yenidən cəhd et.")

elif menu == "⚙️ Parametrlər":
    st.title("👑 Sultan Paneli")
    code = st.text_input("Giriş kodunu yazın:", type="password")
    if code == "sahveren27":
        st.success("Sultan səlahiyyətləri aktiv edildi.")
        st.write("✅ İstifadəçi idarəetməsi: Açıq")
        st.write("✅ Verilənlər bazası: Stabil")
