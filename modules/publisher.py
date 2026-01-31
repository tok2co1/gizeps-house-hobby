import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

class WordPressPublisher:
    def __init__(self):
        self.url = os.getenv("WP_URL")
        self.username = os.getenv("WP_USERNAME")
        self.app_password = os.getenv("WP_APP_PASSWORD")
        self.auth = HTTPBasicAuth(self.username, self.app_password) if self.username and self.app_password else None

    def upload_media(self, file_path, alt_text="Rubon Design"):
        """
        WordPress Medya Kütüphanesine görsel yükler.
        """
        if not self.auth:
            print("⚠️ WP Credentials missing. Skipping upload.")
            return None

        media_url = f"{self.url}/wp-json/wp/v2/media"
        filename = os.path.basename(file_path)
        
        with open(file_path, "rb") as img:
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "image/png"
            }
            response = requests.post(media_url, auth=self.auth, headers=headers, data=img)
            
        if response.status_code == 201:
            media_id = response.json().get("id")
            print(f"✅ Media uploaded successfully. ID: {media_id}")
            return media_id
        else:
            print(f"❌ Media upload failed: {response.text}")
            return None

    def create_post(self, title, content, media_id, tags=""):
        """
        Yüklenen görseli içeren bir galeri/post oluşturur.
        """
        if not self.auth or not media_id:
            return None

        posts_url = f"{self.url}/wp-json/wp/v2/posts"
        
        # Basit bir Gutenberg blok yapısı veya klasik editör içeriği
        post_content = f'<!-- wp:image {{"id":{media_id},"sizeSlug":"large","linkDestination":"none"}} -->\n' \
                       f'<figure class="wp-block-image size-large"><img src="" alt="{title}" class="wp-image-{media_id}"/></figure>\n' \
                       f'<!-- /wp:image -->\n\n' \
                       f'<!-- wp:paragraph -->\n<p>{content}</p>\n<!-- /wp:paragraph -->'

        payload = {
            "title": title,
            "content": post_content,
            "status": "publish",
            "featured_media": media_id,
            "format": "image"
        }

        response = requests.post(posts_url, auth=self.auth, json=payload)
        
        if response.status_code == 201:
            print(f"✅ Post created successfully: {response.json().get('link')}")
            return response.json().get("link")
        else:
            print(f"❌ Post creation failed: {response.text}")
            return None

if __name__ == "__main__":
    # Test
    publisher = WordPressPublisher()
    # publisher.upload_media("output/test.png")
