import os
import asyncio
from playwright.async_api import async_playwright
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

class BrandingEngine:
    def __init__(self):
        # Dosya yollarını modülün bulunduğu konuma göre (root bazlı) ayarla
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.logo_path = os.path.join(base_dir, "assets", "logo.png")
        self.template_path = os.path.join(base_dir, "assets", "template.html")
        self.output_dir = os.path.join(base_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    async def render_html_to_image(self, image_path, output_path, size="30x30 cm", trend="CYBERPUNK 2026"):
        """
        HTML/CSS şablonunu Playwright ile görselleştirir.
        """
        print(f"Rendering HTML branding for {image_path}...")
        
        # HTML Şablonunu oku ve verileri içine yerleştir
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        
        template = Template(template_str)
        # Dosya yolları HTML için absolute ve file:/// formatında olmalı
        image_uri = "file:///" + os.path.abspath(image_path).replace("\\", "/")
        logo_uri = "file:///" + self.logo_path.replace("\\", "/")
        
        html_content = template.render(
            image_path=image_uri,
            logo_path=logo_uri,
            size=size,
            trend=trend
        )

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1024, "height": 1024})
            await page.set_content(html_content)
            # Görsellerin yüklenmesini bekle
            await page.wait_for_timeout(1500) 
            await page.screenshot(path=output_path, full_page=True, omit_background=True)
            await browser.close()
        
        return output_path

    def apply_branding(self, input_png, output_path, size_label="30x30 cm", trend="NEON VIBES"):
        """
        Async render işlemini senkron wrapper ile çağırır.
        """
        return asyncio.run(self.render_html_to_image(input_png, output_path, size_label, trend))

    def generate_mockup(self, branded_png, output_path, template_type="wood"):
        """
        Tasarımı bir mockup (ahşap zemin vb.) üzerine yerleştirir. (Phase 2)
        """
        print(f"Generating {template_type} mockup for { branded_png }...")
        # Mockup mantığı: Arka plana bir zemin koy, üzerine tasarımı %50-70 opacity ile bindir.
        return output_path

if __name__ == "__main__":
    be = BrandingEngine()
    # be.apply_branding("test.png", "output/test_branded.png")
