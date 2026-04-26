import streamlit as st
import pandas as pd
import plotly.express as px

# --- SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="MarketPro Panel", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Şəkildəki dizaynı bərpa etmək üçün) ---
st.markdown("""
    <style>
    /* Ümumi fon rəngi (Mərkəzi hissə) */
    .stApp {
        background-color: #0c0d12 !important;
        color: #ffffff;
    }

    /* Sol Menyu (Sidebar) Dizaynı */
    [data-testid="stSidebar"] {
        background-color: #161821 !important;
        border-right: 1px solid #2d2f3b;
    }
    [data-testid="stSidebar"] * {
        color: #a0a5b9 !important;
    }
    
    /* Aktiv menyu düyməsinin stili */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* MarketPro Başlığı */
    .marketpro-title {
        color: #a78bfa; /* Violet rəng */
        font-size: 24px;
        font-weight: bold;
        margin-bottom: -5px;
    }
    .marketpro-subtitle {
        color: #6b7280;
        font-size: 12px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Metrik Kartları (Aylıq Gəlir və s.) */
    .metric-card {
        background-color: #161821;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d2f3b;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
    }
    .metric-delta-green {
        color: #10b981; /* Yaşıl */
        font-size: 14px;
    }

    /* Profil bölməsi */
    .profile-section {
        position: fixed;
        bottom: 20px;
        left: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .profile-avatar {
        width: 40px;
        height: 40px;
        background-color: #db2777; /* Çəhrayı */
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL MENYU (Sidebar) ---
with st.sidebar:
    st.markdown('<p class="marketpro-title">MarketPro</p>', unsafe_allow_html=True)
    st.markdown('<p class="marketpro-subtitle">MARKETİNQ PANELİ</p>', unsafe_allow_html=True)
    
    st.markdown("### ƏSAS")
    menu_selection = st.radio(
        label="", # Label gizli qalır
        options=["📊 İcmal", "📢 Kampaniyalar", "📈 Analitika", "👥 Hədəf Kütləsi"],
        index=0 # Default olaraq İcmal seçilir
    )
    
    st.markdown("### DİGƏR")
    st.radio(label="", options=["⚙️ Parametrlər"], index=0)

    # Profil (bottom)
    st.markdown('---')
    st.markdown("""
        <div class="profile-section">
            <div class="profile-avatar">Q</div>
            <div>
                <b style="color:white;">Quba</b><br>
                <span style="color:#6b7280; font-size:12px;">Marketinq Direktoru</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ANA SƏHİFƏ MƏZMUNU ---

# Başlıq bölməsi (İcmal, Tarix)
col_title, col_date = st.columns([3, 1])
with col_title:
    st.title("İcmal")
with col_date:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:right; color:#6b7280;">
            Aprel 2025<br>
            <span style="color:#10b981; font-size:12px;">● canlı məlumatlar</span>
        </div>
    """, unsafe_allow_html=True)

# 📊 METRİK KARTLARI
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div style="color:#6b7280;">💰 Ümumi Gəlir</div>
            <div class="metric-value">₼ 12,450</div>
            <div class="metric-delta-green">↑ 12% keçən aya nəzərən</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <div style="color:#6b7280;">👁️ Təəssüratlar</div>
            <div class="metric-value">84,120</div>
            <div class="metric-delta-green">↑ 8% keçən aya nəzərən</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div style="color:#6b7280;">🖱️ Klikləmələr</div>
            <div class="metric-value">5,200</div>
            <div style="color:#ef4444; font-size:14px;">↓ 2% keçən aya nəzərən</div>
        </div>
    """, unsafe_allow_html=True)

# 📈 QRAFİK BÖLMƏSİ (Aylıq Gəlir)
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Aylıq Gəlir Trendi")

# Örnək data qrafik üçün
chart_data = pd.DataFrame({
    'Ay': ['Yan', 'Fev', 'Mar', 'Apr'],
    'Gəlir': [8000, 9500, 11000, 12450]
})

fig = px.line(chart_data, x='Ay', y='Gəlir', text='Gəlir', markers=True)
fig.update_traces(line_color='#a78bfa', marker=dict(size=10, color="#ffffff"))
fig.update_layout(
    plot_bgcolor='#161821',
    paper_bgcolor='#0c0d12',
    font_color='#ffffff',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#2d2f3b')
)
st.plotly_chart(fig, use_container_width=True)
