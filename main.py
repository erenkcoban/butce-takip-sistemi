from src.kategori import Kategori
from src.harcama import Harcama, OnlineHarcama
from utils import veri_yukle, veri_kaydet

# Streamlit ayarları ve kategori listesi
st.set_page_config(page_title="Bütçe Takip", layout="wide")
kategori_listesi = [Kategori("Gıda"), Kategori("Ulaşım"), Kategori("Eğlence")]

# Veri yükle
veri = veri_yukle()

# Form kısmı
st.title("📥 Harcama Ekle")
with st.form("harcama_form"):
    aciklama = st.text_input("Açıklama")
    tutar = st.number_input("Tutar", min_value=0.0)
    kategori_secimi = st.selectbox("Kategori", kategori_listesi, format_func=lambda k: k.isim)
    odeme_yontemi = st.text_input("Ödeme Yöntemi (isteğe bağlı)")
    submitted = st.form_submit_button("Ekle")

    if submitted and aciklama and tutar:
        if odeme_yontemi:
            yeni = OnlineHarcama(aciklama, tutar, kategori_secimi, odeme_yontemi)
        else:
            yeni = Harcama(aciklama, tutar, kategori_secimi)

        veri.append(yeni.to_dict())
        veri_kaydet(veri)
        st.success("Harcama başarıyla eklendi!")
        st.rerun()
