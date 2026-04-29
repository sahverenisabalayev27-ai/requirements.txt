import streamlit as st
import google.generativeai as genai
from PIL import Image
import qrcode
from io import BytesIO

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Sultan AI - Universal Ekosistem", layout="wide")

# API Açarı Girişi (Təhlükəsizlik üçün kənarda saxla)
# Real istifadədə bunu st.secrets-dən oxumaq məsləhətdir
API_KEY = st.sidebar.text_input("Google AI Key daxil edin:", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- ANA MENYU ---
st.sidebar.title("Sultan AI Mərkəzi")
choice = st.sidebar.radio("Bölmə Seçin:", 
    ["Ana Səhifə", "Vision AI (Göz)", "Biznes & QR", "İnşaat & Milli Dizayn", "Gündəlik Köməkçi"])

# --- 1. ANA SƏHİFƏ ---
if choice == "Ana Səhifə":
    st.title("Sultan AI: Milli Super-Portal 🇦🇿")
    st.subheader("Hər kəs üçün, hər sahədə, tək bir nöqtədən süni intellekt həlləri.")
    st.write("Sultan Media tərəfindən 'Zəka Core' vizyonu ilə hazırlanmışdır.")
    # Bura hazırladığın 3D loqonu əlavə edə bilərsən
    st.info("Sol tərəfdən ehtiyacınız olan bölməni seçərək başlayın.")

# --- 2. VISION AI (GÖZ) ---
elif choice == "Vision AI (Göz)":
    st.header("👁️ Sultan Göz: Şəkil ilə Həll")
    st.write("Şəkil çəkin: Problemi tapaq, təmiri deyək və ya reklam mətni yazaq.")
    
    img_file = st.camera_input("Şəkil çək və ya yüklə")
    
    if img_file and API_KEY:
        img = Image.open(img_file)
        st.image(img, caption="Analiz edilir...", width=300)
        
        prompt = "Bu şəkli analiz et. Əgər texniki problemdirsə təmiri, məhsuldursa satış mətni və qiymətini, əgər saqqal/saçdırsa kəsim tövsiyəsini ver."
        
        with st.spinner("Sultan AI düşünür..."):
            response = model.generate_content([prompt, img])
            st.success("Analiz Nəticəsi:")
            st.write(response.text)
            
            # WhatsApp düyməsi
            wa_msg = f"Sultan AI Analizi: {response.text[:100]}..."
            st.markdown(f"[Nəticəni WhatsApp ilə göndər](https://wa.me/?text={wa_msg})")

# --- 3. BİZNES & QR ---
elif choice == "Biznes & QR":
    st.header("💼 Biznes Mərkəzi")
    biz_name = st.text_input("Biznesin adı (məs: Sultan Bərbər):")
    biz_info = st.text_area("Xidmət haqqında məlumat:")
    
    if st.button("QR Kod və Reklam Yarat"):
        # QR Generator
        qr_data = f"Biznes: {biz_name}\nXidmət: {biz_info}"
        qr_img = qrcode.make(qr_data)
        
        buf = BytesIO()
        qr_img.save(buf)
        st.image(buf, caption=f"{biz_name} üçün QR Kod")
        
        # Reklam mətni
        if API_KEY:
            res = model.generate_content(f"{biz_name} adlı {biz_info} xidməti üçün cəlbedici Instagram reklamı yaz.")
            st.write(res.text)

# --- 4. İNŞAAT & MİLLİ DİZAYN ---
elif choice == "İnşaat & Milli Dizayn":
    st.header("🏗️ İnşaat və Milli Dizayn")
    st.write("Evinizin şəklini atın, biz onu Milli ruhla (Lahıc, Xınalıq) yenidən dizayn edək.")
    # Bura yuxarıdakı Vision AI məntiqini spesifik dizayn promptları ilə əlavə edəcəyik.

# --- 5. GÜNDƏLİK KÖMƏKÇİ ---
elif choice == "Gündəlik Köməkçi":
    st.header("🏠 Sultan Life")
    user_q = st.text_input("Nə baş verib? (Məs: Paltarda yağ ləkəsi var...)")
    if user_q and API_KEY:
        res = model.generate_content(f"Gündəlik həyat köməkçisi kimi cavab ver: {user_q}")
        st.write(res.text)
