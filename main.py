import time
import os
import datetime
from modules.concept_generator import ConceptGenerator
from modules.image_engine import ImageEngine
from modules.branding_engine import BrandingEngine
from modules.publisher import WordPressPublisher
from modules.database import ProductDatabase
from dotenv import load_dotenv

load_dotenv()

def main_loop():
    print("🚀 Antigravity OS Otonom Rubon Fabrikası v2.0 Başlatıldı!")
    
    concept_gen = ConceptGenerator()
    image_engine = ImageEngine()
    branding_engine = BrandingEngine()
    publisher = WordPressPublisher()
    db = ProductDatabase()
    
    daily_limit = 25
    generated_today = 0
    last_reset_date = datetime.date.today()

    while True:
        try:
            # Günlük limit sıfırlama kontrolü
            if datetime.date.today() > last_reset_date:
                generated_today = 0
                last_reset_date = datetime.date.today()
                print("📅 Yeni gün başladı, limit sıfırlandı.")

            if generated_today >= daily_limit:
                print(f"🛑 Günlük limite ulaşıldı ({daily_limit}). Yarın devam edilecek.")
                # 1 saat bekle ve sonra tekrar kontrol et
                time.sleep(3600)
                continue

            print(f"\n--- Üretim Döngüsü Başlıyor ({generated_today + 1}/{daily_limit}) ---")
            
            # 1. Konsept Üretimi (Gemini Pro)
            concept = concept_gen.generate_concept()
            if not concept:
                print("⚠️ Konsept üretilemedi, 1 dk sonra tekrar denenecek.")
                time.sleep(60)
                continue
            
            task_name = concept.get('Tasarım Adı', 'Adsız Tasarım')
            print(f"🎨 Tasarım: {task_name}")
            
            # 2. Görsel Üretimi (Imagen 3)
            raw_filename = f"raw_{int(time.time())}.png"
            raw_path = os.path.join("assets", raw_filename)
            prompt = concept.get("Detaylı Görsel Açıklaması")
            
            if image_engine.generate_image(prompt, raw_path):
                # 3. Temizleme ve 300 DPI Set Etme (Rembg & Pillow)
                clean_filename = f"clean_{int(time.time())}.png"
                clean_path = os.path.join("assets", clean_filename)
                
                if image_engine.process_image(raw_path, clean_path):
                    # 4. Branding (HTML/CSS Template)
                    branded_filename = f"{task_name.replace(' ', '_')}_{int(time.time())}_branded.png"
                    branded_path = os.path.join("output", branded_filename)
                    
                    branding_engine.apply_branding(clean_path, branded_path, trend=task_name)
                    
                    # 5. Kayıt (Yerel Veritabanı)
                    sku = f"GZP-RUB-{int(time.time()) % 10000:04d}"
                    db.add_product({
                        "title": task_name,
                        "category": "RUB ON TRANSFER",
                        "price": "145", # Varsayılan fiyat
                        "sku": sku,
                        "image": f"/output/{branded_filename}",
                        "description": concept.get("SEO_Aciklamasi", ""),
                        "isNew": True
                    })
                    
                    # 6. Yayınlama (WordPress REST API)
                    media_id = publisher.upload_media(branded_path, alt_text=task_name)
                    if media_id:
                        publisher.create_post(
                            title=task_name,
                            content=concept.get("SEO_Aciklamasi", "Karışık dekor PNG, rubon uyumlu."),
                            media_id=media_id,
                            tags=concept.get("Etiketler", "")
                        )
                    
                    generated_today += 1
                    print(f"✅ Döngü Başarıyla Tamamlandı: {task_name}")
                else:
                    print("❌ Görsel işleme (Rembg/DPI) başarısız.")
            else:
                print("❌ Imagen 3 üretimi başarısız.")

            print("🕒 5 dakika bekliyor...")
            time.sleep(300)
            
        except Exception as e:
            print(f"❌ Kritik Hata: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main_loop()
