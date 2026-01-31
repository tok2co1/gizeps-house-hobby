from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import threading
import time
import datetime
import sys

# Path setup to import factory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from modules.concept_generator import ConceptGenerator
from modules.image_engine import ImageEngine
from modules.branding_engine import BrandingEngine
from modules.publisher import WordPressPublisher
from modules.database import ProductDatabase

app = FastAPI(title="Rubon Factory Control API")

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared state
class FactoryState:
    def __init__(self):
        self.is_running = False
        self.generated_today = 0
        self.daily_limit = 25
        self.last_reset_date = datetime.date.today()
        self.logs = []
        self.last_generated_image = None
        self.current_task = "Beklemede"
        self.custom_prompt = None
        self._stop_event = threading.Event()

    def add_log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        if len(self.logs) > 50:
            self.logs.pop(0)
        print(log_entry)

state = FactoryState()
db = ProductDatabase()

# Mount output folder to serve images
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))
os.makedirs(output_path, exist_ok=True)
app.mount("/output", StaticFiles(directory=output_path), name="output")

def factory_worker():
    state.add_log("🚀 Fabrika çalışma birimi başlatıldı.")
    
    concept_gen = ConceptGenerator()
    image_engine = ImageEngine()
    branding_engine = BrandingEngine()
    publisher = WordPressPublisher()
    
    while not state._stop_event.is_set():
        try:
            # Check daily limit
            if datetime.date.today() > state.last_reset_date:
                state.generated_today = 0
                state.last_reset_date = datetime.date.today()
                state.add_log("📅 Yeni gün başladı, limit sıfırlandı.")

            if state.generated_today >= state.daily_limit:
                state.current_task = "Limite Ulaşıldı"
                state.add_log(f"🛑 Günlük limite ulaşıldı ({state.daily_limit}).")
                time.sleep(60)
                continue

            state.current_task = "Konsept Üretiliyor"
            state.add_log(f"🎨 Yeni konsept üretiliyor... (Özel İstek: {state.custom_prompt or 'Yok'})")
            
            # Eğer özel istek varsa bunu konsept üreticisine anahtar kelime olarak iletelim
            keywords = [state.custom_prompt] if state.custom_prompt else None
            concept = concept_gen.generate_concept(keywords=keywords)
            
            if not concept:
                state.add_log("⚠️ Konsept üretilemedi. 1 dk içinde tekrar denenecek.")
                time.sleep(60)
                continue
            
            task_name = concept.get('Tasarım Adı', 'Bilinmiyor')
            state.add_log(f"✨ Konsept hazır: {task_name}")

            state.current_task = "Görsel Üretiliyor"
            raw_filename = f"raw_{int(time.time())}.png"
            raw_path = os.path.join(os.path.dirname(__file__), "../../assets", raw_filename)
            
            if image_engine.generate_image(concept.get("Detaylı Görsel Açıklaması"), raw_path):
                state.current_task = "Görsel İşleniyor"
                clean_filename = f"clean_{int(time.time())}.png"
                clean_path = os.path.join(os.path.dirname(__file__), "../../assets", clean_filename)
                
                if image_engine.process_image(raw_path, clean_path):
                    state.current_task = "Markalama"
                    branded_filename = f"{task_name.replace(' ', '_')}_{int(time.time())}_branded.png"
                    branded_path = os.path.join(output_path, branded_filename)
                    
                    branding_engine.apply_branding(clean_path, branded_path, trend=task_name)
                    state.last_generated_image = branded_filename
                    
                    # Store in Local Database
                    sku = f"GZP-RUB-{int(time.time()) % 10000:04d}"
                    db.add_product({
                        "title": task_name,
                        "category": "RUB ON TRANSFER",
                        "price": "145",
                        "sku": sku,
                        "image": f"/output/{branded_filename}",
                        "description": concept.get("SEO_Aciklamasi", ""),
                        "isNew": True
                    })
                    
                    state.current_task = "Yayınlanıyor"
                    state.add_log(f"📤 {task_name} WordPress'e yükleniyor...")
                    media_id = publisher.upload_media(branded_path, alt_text=task_name)
                    if media_id:
                        publisher.create_post(
                            title=task_name,
                            content=concept.get("SEO_Aciklamasi", ""),
                            media_id=media_id,
                            tags=concept.get("Etiketler", "")
                        )
                    
                    state.generated_today += 1
                    state.add_log(f"✅ Döngü tamamlandı: {task_name}")
                else:
                    state.add_log("❌ Görsel işleme başarısız.")
            else:
                state.add_log("❌ Görsel üretimi başarısız.")

            state.current_task = "Bekliyor"
            for _ in range(300): # 5 minutes wait
                if state._stop_event.is_set(): break
                time.sleep(1)
                
        except Exception as e:
            state.add_log(f"❌ Hata: {str(e)}")
            time.sleep(60)

@app.get("/status")
def get_status():
    return {
        "is_running": state.is_running,
        "generated_today": state.generated_today,
        "daily_limit": state.daily_limit,
        "last_image": state.last_generated_image,
        "current_task": state.current_task,
        "logs": state.logs[-20:],
        "custom_prompt": state.custom_prompt
    }

@app.get("/products")
def get_products():
    return db.get_all_products()

@app.get("/product/{product_id}")
def get_product(product_id: int):
    product = db.get_product_by_id(product_id)
    if product:
        return product
    return {"error": "Product not found"}, 404

from pydantic import BaseModel

class StartRequest(BaseModel):
    custom_prompt: str = None

@app.post("/start")
def start_factory(request: StartRequest = None):
    if not state.is_running:
        state.is_running = True
        state.custom_prompt = request.custom_prompt if request else None
        state._stop_event.clear()
        thread = threading.Thread(target=factory_worker, daemon=True)
        thread.start()
        state.add_log("▶️ Fabrika Dashboard üzerinden başlatıldı.")
        return {"message": "Factory started"}
    return {"message": "Factory already running"}

@app.post("/stop")
def stop_factory():
    if state.is_running:
        state.is_running = False
        state._stop_event.set()
        state.current_task = "Beklemede"
        state.add_log("⏹️ Fabrika Dashboard üzerinden durduruldu.")
        return {"message": "Factory stopping"}
    return {"message": "Factory not running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

