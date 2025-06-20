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


class OnlineHarcama(Harcama):
    def __init__(self, aciklama, tutar, kategori, odeme_yontemi, tarih=None):
        super().__init__(aciklama, tutar, kategori, tarih)
        self.odeme_yontemi = odeme_yontemi

    def to_dict(self):
        data = super().to_dict()
        data["odeme_yontemi"] = self.odeme_yontemi
        return data

    def __str__(self):
        return f"{super().__str__()} - Ödeme: {self.odeme_yontemi}"
