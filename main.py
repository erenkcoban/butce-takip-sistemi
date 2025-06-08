import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.kategori import Kategori
from src.harcama import Harcama
from utils import veri_yukle, veri_kaydet, dictten_harcama
# versiyon 1.1

st.set_page_config(page_title="Bütçe Takip Sistemi", layout="wide")

# Kategoriler
kategori_listesi = [Kategori("Gıda"), Kategori("Ulaşım"), Kategori("Eğlence"), Kategori("Fatura")]

# Veriyi yükle
veri = veri_yukle()
harcamalar = [dictten_harcama(v) for v in veri]

# Menü
menu = st.sidebar.radio("Menü", ["Ana Sayfa", "Harcamalar", "Analiz"])

# Veri aktarımı (İçe/dışa)
st.sidebar.subheader("🔄 Veri Aktarımı")

uploaded_file = st.sidebar.file_uploader("📂 JSON Yükle", type=["json"])
if uploaded_file:
    import json
    yeni_veri = json.load(uploaded_file)
    veri.extend(yeni_veri)
    veri_kaydet(veri)
    st.sidebar.success("Veriler içe aktarıldı.")
    st.rerun()

st.sidebar.download_button("💾 Veriyi İndir", data=pd.DataFrame(veri).to_json(orient="records", indent=2),
                           file_name="harcamalar.json", mime="application/json")

# ANA SAYFA
if menu == "Ana Sayfa":
    st.title("📥 Harcama Ekle")
    with st.form("harcama_form"):
        aciklama = st.text_input("Açıklama")
        tutar = st.number_input("Tutar", min_value=0.0, step=0.5)
        kategori_secimi = st.selectbox("Kategori", kategori_listesi, format_func=lambda k: k.isim)
        submitted = st.form_submit_button("Ekle")

        if submitted and aciklama and tutar:
            yeni = Harcama(aciklama, tutar, kategori_secimi)
            veri.append(yeni.to_dict())
            veri_kaydet(veri)
            st.success(f"✅ {aciklama} harcaması başarıyla eklendi!")
            st.rerun()

# HARCAMALAR
elif menu == "Harcamalar":
    st.title("📄 Harcamalar")
    if not veri:
        st.info("Henüz harcama eklenmedi.")
    else:
        df = pd.DataFrame(veri)
        kategori_filtre = st.selectbox("Kategoriye göre filtrele", ["Tümü"] + list(df["kategori"].unique()))
        if kategori_filtre != "Tümü":
            df = df[df["kategori"] == kategori_filtre]

        st.dataframe(df[["aciklama", "tutar", "kategori", "tarih"]])

        st.subheader("Silmek istediğiniz harcamayı seçin:")
        for i, row in df.iterrows():
            if st.button(f"❌ {row['aciklama']} - {row['tutar']} TL", key=f"sil_{i}"):
                veri.pop(i)
                veri_kaydet(veri)
                st.success("Harcama silindi.")
                st.rerun()

# ANALİZ
elif menu == "Analiz":
    st.title("📊 Harcama Analizi")

    if not veri:
        st.info("Analiz yapılacak veri yok.")
    else:
        df = pd.DataFrame(veri)
        df["tutar"] = df["tutar"].astype(float)
        df["tarih"] = pd.to_datetime(df["tarih"])

        plt.style.use("ggplot")

        # YAN YANA GRAFİKLER
        col1, col2 = st.columns(2)

        # Pie Chart (kategoriye göre)
        with col1:
            st.subheader("📌 Kategoriye Göre Dağılım")
            fig1, ax1 = plt.subplots()
            df_group = df.groupby("kategori")["tutar"].sum()
            ax1.pie(df_group, labels=df_group.index, autopct="%1.1f%%", startangle=90)
            ax1.axis("equal")
            st.pyplot(fig1)

        # Line Chart (zaman bazlı)
        with col2:
            st.subheader("📈 Günlük Harcama Artışı")
            tarihsel = df.groupby("tarih")["tutar"].sum().reset_index()
            fig2, ax2 = plt.subplots()
            ax2.plot(tarihsel["tarih"], tarihsel["tutar"], marker="o")
            ax2.set_title("Zamana Göre Harcama")
            ax2.set_xlabel("Tarih")
            ax2.set_ylabel("Tutar (TL)")
            st.pyplot(fig2)
