import os
import json
import shutil
import time
import uuid
from datetime import datetime
from PIL import Image

# Configuration
SOURCE_DIR = r"C:\Users\MotoCraft\Desktop\masaüstü\GİZEPS\yüklenecekler"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "products.json"))

# Categories mapping
CATEGORIES = {
    "deniz": "DENİZ VE MARİN",
    "kadınlar": "KADIN FİGÜRLERİ",
    "karışık": "KARIŞIK TASARIMLAR",
    "mutfak": "MUTFAK VE GIDA",
    "çiçekler": "ÇİÇEKLER VE DOĞA"
}

def get_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def process_image(file_path, category_key):
    try:
        # Generate unique filename
        ext = os.path.splitext(file_path)[1].lower()
        if not ext: ext = ".jpg"
        new_filename = f"prod_{uuid.uuid4().hex[:12]}{ext}"
        target_path = os.path.join(OUTPUT_DIR, new_filename)
        
        # Copy file
        shutil.copy2(file_path, target_path)
        
        # Determine Title (Simple logic for now, using filename or generic)
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        
        if "WhatsApp" in base_name:
            title = f"{CATEGORIES.get(category_key, 'Özel Tasarım')} - {base_name.split(' ')[-1]}"
        else:
            title = base_name.capitalize().replace("-", " ").replace("_", " ")

        category = CATEGORIES.get(category_key, "GENEL")
        
        product = {
            "id": int(time.time() * 1000) % 1000000, # Simplified unique ID
            "title": title,
            "category": category,
            "price": "145", # Default price
            "sku": f"GZP-{category_key[:3].upper()}-{uuid.uuid4().hex[:4].upper()}",
            "image": f"/output/{new_filename}",
            "description": f"{title} özel tasarım rub-on transfer. {category} koleksiyonuna ait yüksek kaliteli bir üründür.",
            "isNew": True,
            "created_at": datetime.now().isoformat()
        }
        
        return product
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    db_data = get_db()
    existing_ids = {p["id"] for p in db_data}
    
    total_processed = 0
    
    for category_folder in os.listdir(SOURCE_DIR):
        folder_path = os.path.join(SOURCE_DIR, category_folder)
        if not os.path.isdir(folder_path):
            continue
            
        print(f"📂 Processing category: {category_folder}")
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_path = os.path.join(root, file)
                    
                    # Process one by one
                    print(f"  🖼️ Loading: {file}...", end="\r")
                    product = process_image(file_path, category_folder)
                    
                    if product:
                        # Ensure no ID collision (unlikely but safe)
                        while product["id"] in existing_ids:
                            product["id"] += 1
                        
                        db_data.append(product)
                        existing_ids.add(product["id"])
                        
                        # Save after each item to prevent data loss and keep state fresh
                        save_db(db_data)
                        total_processed += 1
                        print(f"  ✅ Added: {product['title']} (Total: {total_processed})")
                        
                        # Sequential delay to prevent locking
                        time.sleep(0.5) 
                    
    print(f"\n🚀 SUCCESS! Total products added: {total_processed}")

if __name__ == "__main__":
    main()
