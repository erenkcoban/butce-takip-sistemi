import json
from datetime import datetime
from src.kategori import Kategori
from src.harcama import Harcama

def veri_yukle(dosya="data.json"):
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def veri_kaydet(veri, dosya="data.json"):
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

def dictten_harcama(obj):
    return Harcama(
        aciklama=obj["aciklama"],
        tutar=obj["tutar"],
        kategori=Kategori(obj["kategori"]),
        tarih=datetime.strptime(obj["tarih"], "%Y-%m-%d")
    )
