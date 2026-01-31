import os
import json
import hashlib
import re

# Configuration
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "products.json"))

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except:
        return None

def clean_title(title):
    # Remove "Kopya", "Copy", "(1)", "(2)", etc.
    title = re.sub(r'\s*-?\s*Kopya.*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*-?\s*Copy.*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\(\d+\)', '', title)
    title = re.sub(r'\s*-\s*\d+', '', title)
    # Strip extra whitespace
    title = title.strip()
    return title

def main():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found.")
        return

    with open(DB_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"Initial products: {len(products)}")

    # 1. Identify duplicates via hashing
    unique_hashes = {} # hash -> primary_filename
    file_to_hash = {}
    duplicates_to_remove = []
    
    # Calculate hashes for all files referenced in DB
    referenced_files = set()
    for p in products:
        img_path = p.get("image", "")
        if img_path.startswith("/output/"):
            filename = img_path.replace("/output/", "")
            full_path = os.path.join(OUTPUT_DIR, filename)
            referenced_files.add(full_path)

    print(f"Hashing {len(referenced_files)} files...")
    for f_path in referenced_files:
        h = get_file_hash(f_path)
        if h:
            if h in unique_hashes:
                # This file is a duplicate of an already seen one
                duplicates_to_remove.append(f_path)
            else:
                unique_hashes[h] = f_path
            file_to_hash[f_path] = h

    # 2. Re-build database without duplicates and with cleaned titles
    new_products = []
    seen_hashes_in_db = set()
    removed_count = 0

    for p in products:
        img_path = p.get("image", "")
        if img_path.startswith("/output/"):
            filename = img_path.replace("/output/", "")
            full_path = os.path.join(OUTPUT_DIR, filename)
            h = file_to_hash.get(full_path)
            
            if h and h in seen_hashes_in_db:
                removed_count += 1
                continue # Skip duplicate
            
            seen_hashes_in_db.add(h)
        
        # Clean title
        p["title"] = clean_title(p["title"])
        new_products.append(p)

    # 3. Save new database
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(new_products, f, indent=4, ensure_ascii=False)

    # 4. Cleanup actual files (optional but good)
    print(f"Removed {removed_count} duplicate entries from database.")
    print(f"Titles cleaned for remaining {len(new_products)} products.")
    
    # Actually delete duplicate files from output dir to save space
    deleted_files_count = 0
    for f_path in duplicates_to_remove:
        try:
            os.remove(f_path)
            deleted_files_count += 1
        except:
            pass
    print(f"Deleted {deleted_files_count} physical duplicate files.")

if __name__ == "__main__":
    main()
