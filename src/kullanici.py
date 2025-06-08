class Kullanici:
    def __init__(self, isim):
        self.isim = isim
        self.harcamalar = []

    def harcama_ekle(self, harcama):
        self.harcamalar.append(harcama)

    def toplam_harcama(self):
        return sum(h.tutar for h in self.harcamalar)
