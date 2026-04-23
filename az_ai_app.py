import streamlit as st
from groq import Groq
import random

# 1. Səhifə Ayarları və Vizual Stil
st.set_page_config(page_title="Akademiya AI", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1a237e;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #303f9f; border: 2px solid white; }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 8px solid #1a237e;
    }
    h1 { color: #1a237e; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Açar Hovuzu (Multi-Key Management)
def get_all_active_keys():
    # Secrets içində "GROQ_API_KEY" sözü keçən bütün açarları siyahıya yığır
    keys = [st.secrets[k] for k in st.secrets if "GROQ_API_KEY" in k]
    return keys

active_keys = get_all_active_keys()

def generate_ai_response(subject, topic, mode):
    if not active_keys:
        return "⚠️ Sistemdə API açarı tapılmadı! Lütfən Secrets hissəsinə açarları əlavə edin."
    
    # Açarları hər sorğuda qarışdırırıq ki, yüklənmə bərabər paylansın
    random.shuffle(active_keys)
    
    # Akademik Müəllim üçün xüsusi təlimat (Prompt)
    if mode == "Dərin İzah (Ensiklopediya)":
        prompt = f"""
        Sən Azərbaycanın ən savadlı akademik müəllimisən. 
        Mövzu: {subject} - {topic}
        Tapşırıq: Bu mövzunu ən az 1500 sözdən ibarət olmaqla, elmi ensiklopediya dərinliyində izah et.
        Struktur: 
        1. Giriş (Mövzunun əhəmiyyəti).
        2. Tarixi faktlar və Elmi əsaslar (çox geniş).
        3. Vacib terminlərin izahı.
        4. Nəticə və xülasə.
        Dil: Tamamilə Azərbaycan dili.
        """
    else:
        prompt = f"Şagird üçün {subject} fənnindən '{topic}' mövzusunda 1 ədəd çətin səviyyəli test sualı hazırlayın. Variantları (A, B, C, D, E) qoyun və düzgün cavabı ən aşağıda izahlı şəkildə gizli yazın."

    # Açarları sırayla yoxlayırıq (Biri limitə düşsə, o birinə keçir)
    for key in active_keys:
        try:
            client = Groq(api_key=key)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Sən dərin elmi biliklərə sahib Azərbaycanlı professorsun."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=4000 # Uzun cavablar üçün vacibdir
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e): # Limit xətası kodudur
                continue
            else:
                return f"❌ Texniki xəta: {str(e)}"
    
    return "😴 Bütün API açarları hazırda yorulub (limit dolub). Lütfən 1 dəqiqə sonra yenidən cəhd edin."

# 3. İnterfeys Dizaynı
st.markdown("<h1 style='text-align: center;'>🎓 Akademiya AI Portalı</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Milli Təhsil Platformasına xoş gəlmisiniz!</p>", unsafe_allow_html=True)
st.divider()

# Yan Menyu (Sidebar)
st.sidebar.markdown("## ⚙️ Sistem Paneli")
st.sidebar.markdown(f"<div class='status-card'>✅ <b>Server:</b> Aktiv<br>🔑 <b>Açar Sayı:</b> {len(active_keys)}</div>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.warning("🕒 **Tezliklə:** Google Qeydiyyat, Xal Sistemi və Liderlər Lövhəsi aktivləşdiriləcək.")
st.sidebar.info("Bu platforma Sahveren tərəfindən Azərbaycan təhsilinə töhfə olaraq hazırlanır.")

# Əsas Bölmə
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 🔍 Seçimlər")
    subject = st.selectbox("Fən
