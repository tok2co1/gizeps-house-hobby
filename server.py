from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from modules.database import ProductDatabase
import os

app = FastAPI(title="Rubon Factory API")

# Enable CORS for the Next.js storefront
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you should specify the actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = ProductDatabase()

@app.get("/products")
async def get_products():
    products = db.get_all_products()
    return products

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    product = db.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Serve images from the output directory
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

app.mount("/output", StaticFiles(directory=output_dir), name="output")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
