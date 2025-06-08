from datetime import datetime

class Harcama:
    def __init__(self, aciklama, tutar, kategori, tarih=None):
        self.aciklama = aciklama
        self.tutar = tutar
        self.kategori = kategori
        self.tarih = tarih or datetime.now()

    def to_dict(self):
        return {
            "aciklama": self.aciklama,
            "tutar": self.tutar,
            "kategori": self.kategori.isim,
            "tarih": self.tarih.strftime("%Y-%m-%d")
        }

    def __str__(self):
        return f"{self.aciklama} - {self.tutar} TL - {self.kategori} - {self.tarih.strftime('%Y-%m-%d')}"
