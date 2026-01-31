import json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "products.json"))

NAME_MAPPING = {
    "GZP-DEN-027F": "Şişe İçinde Gizemli Mesaj ve Deniz Kabukları",
    "GZP-DEN-03FD": "Yaz Güneşi ve Tatil Keyfi Aranjmanı",
    "GZP-DEN-DA3F": "Egzotik Büyük Deniz Yıldızı ve Mercanlar",
    "GZP-DEN-D864": "Mavi Deniz Kabuklarından Aşk Kalbi",
    "GZP-DEN-6F46": "Paslı Gemi Çapası ve Deniz Yıldızı",
    "GZP-DEN-5FF6": "Egzotik Mavi Benekli Vatoz Balığı",
    "GZP-DEN-2B4B": "Dev Kırmızı Ahtapot ve Derin Denizler",
    "GZP-DEN-CB3D": "Sevimli Turuncu Dev Gözlü Ahtapot",
    "GZP-DEN-4986": "Suluboya Efektli Renkli Ahtapot",
    "GZP-DEN-6787": "Gerçekçi Turuncu Ahtapot Tasarımı",
    "GZP-DEN-87B7": "Canlı Mercan Resifi ve Deniz Yıldızları",
    "GZP-DEN-295B": "Renkli Derin Deniz Mercan Bahçesi",
    "GZP-DEN-EFBC": "Pembe Mercan ve İstriye Kabuğu",
    "GZP-DEN-FA91": "Zarif Deniz Kaplumbağası ve Resif",
    "GZP-DEN-D0FE": "Işıltılı Deniz Anası ve Tropikal Balıklar",
    # Women Figures
    "GZP-KAD-C387": "Klasik Avrupalı Kadın Portresi",
    "GZP-KAD-1E60": "Kitap Okuyan Zarif Kadın",
    "GZP-KAD-3909": "Çiçekli Tacı ile Kızıl Saçlı Kadın",
    "GZP-KAD-B201": "Bohem Şapkalı ve Çiçekli Kadın",
    "GZP-KAD-254D": "Dans Eden Üç Neşeli Kadın",
    "GZP-KAD-5F08": "Mor Elbiseli Modern Kadın Portresi",
    "GZP-KAD-9966": "Şık Giyimli Kadınlar Topluluğu",
    "GZP-KAD-A570": "Mavi Şapkalı ve Güllü Kadın",
    "GZP-KAD-38C9": "Pembe Çiçekler İçinde Bahar Kadını",
    "GZP-KAD-C310": "Mavi Güllü ve Şapkalı Vintage Portre",
    # Kitchen & Food
    "GZP-MUT-34A3": "Mor Çiçekli Kavanoz ve Mutfak Dekoru",
    "GZP-MUT-C20D": "Mutfak Gereçleri ve Kahve Keyfi Teması",
    "GZP-MUT-DB8F": "Pastel Renkli Çay ve Kek Sunumu",
    "GZP-MUT-7053": "Sonbahar Temalı Balkabaklı Kahve Keyfi",
    "GZP-MUT-430D": "Taze Kruvasan ve Çiçekli Mutfak Köşesi",
    "GZP-MUT-0B91": "Tropikal Meyve Sepeti ve Egzotik Çiçekler",
    "GZP-MUT-E343": "Egzotik Meyveler ve Çiçekli Kompozisyon",
    "GZP-MUT-669C": "Deniz Kabukları ve Yıldızları Aranjmanı",
    "GZP-MUT-05E4": "Hasır Sepette Deniz Hazineleri",
    "GZP-MUT-82F3": "Vintage Baharatlık ve Çiçekli Mutfak Seti",
    # Mixed Designs
    "GZP-ÇIÇ-B7C1": "Mavi Kristal Çiçek Bahçesi ve Suluboya Detaylar",
    "GZP-KAR-D3B1": "Japon Pagodası ve Kiraz Çiçekleri Manzarası",
    "GZP-KAR-8ECF": "Zarif Beyaz Kuğular ve Beyaz Gül Aranjmanı",
    "GZP-KAR-DD3C": "Dekoratif Çiçekli Melek Kanatları Tasarımı",
    "GZP-KAR-F721": "Göl Kenarında Mavi Kuğu ve Bahar Çiçekleri",
    "GZP-KAR-DAA2": "Viktoryen Elbiseli Tavşan ve Havuç Sepeti",
    "GZP-KAR-17D2": "Çiçeklerle Süslü Masalsı Çaydanlık Evi",
    "GZP-KAR-A3E4": "Suluboya Efektli Görkemli Fil ve Doğa Teması",
    "GZP-KAR-FEAC": "Nostaljik Dikiş Makinesi ve Vintage Moda Kanvası",
    "GZP-KAR-74A6": "Şanslı Oyun Kağıtları, Zarlar ve Kırmızı Çiçekler",
    "GZP-KAR-B8D8": "Pastel Renkli Çiçeklerle Bezeli Melek Kanatları"
}

CATEGORY_POOLS = {
    "DENİZ VE MARİN": [
        "Turkuaz Deniz Esintisi", "Mercan Resifi Manzarası", "Güneşli Sahil Kasabası", 
        "Deniz Yıldızları ve Kum", "Mavi Derinlikler Portresi", "Yelkenli ve Martılar",
        "Egzotik Balıklar Senfonisi", "Altın Kumsal ve Palmiyeler", "Fener ve Dalga Sesleri",
        "Kristal Berrak Deniz", "Deniz Kabuğu Koleksiyonu", "Okyanus Esintili Tasarım"
    ],
    "KADIN FİGÜRLERİ": [
        "Zarif Bohem Portre", "Çiçekli Modern Sanat", "Nostaljik Bahar Hanımefendisi",
        "Suluboya Kadın Figürü", "Modern Stil Kadın Eskizi", "Şapkalı Zarif Profil",
        "Güller Arasında Kadın", "Minimalist Kadın Silüeti", "Renkli Hayaller Kadını",
        "Klasik Sanat Kadın Portresi", "Huzurlu Kadın Tasarımı", "Işıltılı Kadın Figürü"
    ],
    "KARIŞIK TASARIMLAR": [
        "Masalsı Doğa Kompozisyonu", "Vintage Eşyalar Aranjmanı", "Hayvanlar Alemi Dekor",
        "Sürreal Sanat Çalışması", "Geometrik Fantazi Tasarım", "Retro Kolaj Sanatı",
        "Doğa ve Hayvan Dostluğu", "Düşsel Yolculuk Teması", "Karma Sanat Koleksiyonu",
        "Kuşlar ve Çiçekler Dünyası", "Sihirli Mekan Tasarımı", "Zamansız Sanat Eseri"
    ],
    "MUTFAK VE GIDA": [
        "Lezzetli İtalyan Mutfağı", "Taze Meyve Şöleni", "Kahve ve Kitap Keyfi",
        "Vintage Mutfak Gereçleri", "Güneşli Mutfak Penceresi", "Pastel Kek ve Poğaçalar",
        "Yaz Meyveleri Sepeti", "Sıcak Çay ve Kurabiye", "Organik Sebze Bahçesi",
        "Aşçı Şapkası ve Lezzetler", "Mutfak Dekoratif Sanatı", "Enfes Sofra Aranjmanı"
    ],
    "ÇİÇEKLER VE DOĞA": [
        "Baharın Renkleri Buketi", "Sakin Orman Manzarası", "Vahşi Doğa Çiçekleri",
        "Bahçe Keyfi Aranjmanı", "Gökkuşağı Çiçek Bahçesi", "Sabah Çiği ve Yapraklar",
        "Lavanta Tarlası Esintisi", "Tropikal Doğa Manzarası", "Kır Çiçekleri Senfonisi",
        "Yaz Bahçesi Posteri", "Botanik Sanat Çalışması", "Huzur Veren Doğa Tablosu"
    ]
}

def get_descriptive_name(sku, category):
    import hashlib
    if category not in CATEGORY_POOLS:
        return f"{category.capitalize()} Özel Tasarım"
    
    pool = CATEGORY_POOLS[category]
    # Use MD5 of SKU to always pick the same name for the same product
    hash_idx = int(hashlib.md5(sku.encode()).hexdigest(), 16) % len(pool)
    return pool[hash_idx]

def clean_generic(title, category, sku):
    # If title is numeric or has UUID-like structure or just the category name
    if any(c.isdigit() for c in title) or title.lower() == category.lower() or "özel tasarım" in title.lower():
        return get_descriptive_name(sku, category)
    
    # Standard cleaning
    title = title.replace("_", " ").replace(".", " ")
    title = " ".join(title.split())
    # Remove category prefix if it's there
    title = title.replace(category.upper(), "").replace(category, "")
    title = title.strip(" -.")
    
    if not title or len(title) < 4:
        return get_descriptive_name(sku, category)
        
    return title.capitalize()

def main():
    if not os.path.exists(DB_PATH):
        return

    with open(DB_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    updated_count = 0
    for p in products:
        sku = p.get("sku", "")
        if sku in NAME_MAPPING:
            p["title"] = NAME_MAPPING[sku]
            updated_count += 1
        else:
            p["title"] = clean_generic(p["title"], p.get("category", ""), sku)

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print(f"Final Naming: Updated {updated_count} mapping names and generated descriptive titles for all other products.")

if __name__ == "__main__":
    main()
