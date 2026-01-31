import json
import os
import datetime

class ProductDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to the root of the project
            self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../products.json"))
        else:
            self.db_path = db_path
        
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def get_all_products(self):
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading database: {e}")
            return []

    def add_product(self, product_data):
        products = self.get_all_products()
        
        # Ensure ID and Timestamp
        product_data["id"] = len(products) + 1
        product_data["created_at"] = datetime.datetime.now().isoformat()
        
        products.append(product_data)
        
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to database: {e}")
            return False

    def get_product_by_id(self, product_id):
        products = self.get_all_products()
        for p in products:
            if p.get("id") == product_id:
                return p
        return None
