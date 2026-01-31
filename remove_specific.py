import json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "products.json"))

def main():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    with open(DB_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    # Filter out the two specific products
    titles_to_remove = ["Mavi kristal çiçek bahçesi", "Dört mevsim hobi kutusu"]
    updated_products = [p for p in products if p.get("title") not in titles_to_remove]

    removed_count = len(products) - len(updated_products)

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(updated_products, f, indent=4, ensure_ascii=False)

    print(f"Successfully removed {removed_count} products.")

if __name__ == "__main__":
    main()
