import os
from dotenv import load_dotenv
from google import genai
from rembg import remove
from PIL import Image, ImageEnhance
import io
import requests

load_dotenv()

class ImageEngine:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    def generate_image(self, prompt, output_path):
        """
        Pollinations.ai kullanarak ücretsiz görsel üretir (Imagen alternatifi).
        """
        import requests
        import urllib.parse
        
        # Prompt'u URL güvenli hale getiriyoruz
        safe_prompt = urllib.parse.quote(prompt)
        # Genişlik ve yükseklik parametrelerini ekleyerek kaliteli bir çıktı istiyoruz
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&model=flux"
        
        print(f"Generating image with Pollinations AI (Free). Prompt: {prompt[:50]}...")
        
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"Pollinations output saved to: {output_path}")
                return output_path
            else:
                print(f"Pollinations AI error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error invoking Pollinations AI: {e}")
            return None

    def process_image(self, input_path, output_path):
        """
        Rembg ile arka planı temizler ve Pillow ile 300 DPI olarak kaydeder.
        """
        print(f"Processing image for 300 DPI and transparency: {input_path}")
        
        try:
            with open(input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)
            
            img = Image.open(io.BytesIO(output_data)).convert("RGBA")
            
            # 3000x3000px kontrolü/yükseltmesi (Gerekirse)
            if img.size != (3000, 3000):
                img = img.resize((3000, 3000), Image.LANCZOS)
            
            # Kontrast ve Doygunluk Artırımı
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            converter = ImageEnhance.Color(img)
            img = converter.enhance(1.2)
            
            # 300 DPI olarak kaydet
            img.save(output_path, "PNG", dpi=(300, 300))
            print(f"Success! Processed image (300 DPI) saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error during image processing: {e}")
            return None

if __name__ == "__main__":
    engine = ImageEngine()
    # engine.process_image("test_input.jpg", "test_output.png")
