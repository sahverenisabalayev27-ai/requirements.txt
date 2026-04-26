# Saytın daxilinə bu funksiyanı əlavə edirik (Beyin hissəsi)
def sultan_brain_analysis(user_input):
    # Bu funksiya daxil olan mətni analiz edir
    words = user_input.lower().split()
    if "bahadır" in words or "bahalı" in words:
        return "⚠️ Müştəri qiymətə etiraz edir. Ona 'keyfiyyət' arqumentini deyin."
    elif "istəyirəm" in words or "almaq" in words:
        return "✅ Müştəri almağa hazırdır! Ona dərhal ödəniş linkini göndərin."
    else:
        return "ℹ️ Müştəri sadəcə məlumat alır. Onu maraqlandıracaq bir sual verin."

# Saytda istifadəsi:
user_msg = st.text_input("Müştərinin yazdığı mesajı bura yapışdır:")
if user_msg:
    analiz_neticesi = sultan_brain_analysis(user_msg)
    st.info(analiz_neticesi)
