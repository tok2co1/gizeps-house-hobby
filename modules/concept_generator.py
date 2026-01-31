import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class ConceptGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_concept(self, keywords=None):
        if not keywords:
            # Kullanıcının istediği karmaşık kombinasyonlar için genişletilmiş keyword listesi
            keywords = [
                "vintage çay seti + çiçekler + muffin", 
                "cyberpunk kask + neon graffiti", 
                "steampunk saat + mekanik dişliler", 
                "retro atari + 80s neon", 
                "minimalist hat sanatı + suluboya çiçekler"
            ]
        
        prompt = f"""
        Sen otonom bir rubon ütü baskı (transfer) tasarımcısısın. 
        Şu anahtar kelimelerden birini veya birkaçını kullanarak trend, estetik ve transfer baskıya uygun bir konsept üret: {keywords}
        
        PROMPT TALİMATLARI:
        1. Tasarım yüksek çözünürlüklü ve keskin hatlara sahip olmalıdır.
        2. Imagen 3 için üretilecek prompt'un sonuna mutlaka şu teknik detayları ekle: 
           "3000x3000 px, 300 dpi print quality, high detail, detailed background, professional photography style, isolated on high contrast background for easy removal"
        3. Tasarım kombinasyonu karmaşık olmalı (örn: bir obje + doğa elemanı + dekoratif unsur).

        YANIT FORMATI (JSON):
        {{
            "Tasarım Adı": "...",
            "Detaylı Görsel Açıklaması": "...",
            "Renkli_Palet": ["...", "..."],
            "SEO_Aciklamasi": "Karışık dekor PNG, rubon uyumlu. ...",
            "Etiketler": "rubon, ütü baskı, transfer kağıdı, ..."
        }}

        Yanıtı sadece saf JSON formatında ver.
        """
        
        response = self.model.generate_content(prompt)
        try:
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "{" in text:
                text = text[text.find("{"):text.rfind("}")+1]
            return json.loads(text)
        except Exception as e:
            print(f"Error generating concept: {e}")
            return None

if __name__ == "__main__":
    generator = ConceptGenerator()
    concept = generator.generate_concept()
    print(json.dumps(concept, indent=4, ensure_ascii=False))
