from atproto import Client
import os

class BlueskyService:
    def __init__(self):
        self.enabled = os.getenv('BLUESKY_ENABLE_POSTING', 'false').lower() == 'true'
        if not self.enabled:
            return
            
        self.client = Client()
        self.username = os.getenv('BLUESKY_USERNAME')
        self.password = os.getenv('BLUESKY_PASSWORD')
        
        try:
            self.client.login(self.username, self.password)
            print("Successfully authenticated with Bluesky")
        except Exception as e:
            print(f"Failed to authenticate with Bluesky: {e}")
            self.enabled = False

    def post(self, message):
        if not self.enabled:
            return
            
        try:
            self.client.send_post(text=message)
            print(f"Posted to Bluesky: {message}")
        except Exception as e:
            print(f"Failed to post to Bluesky: {e}")


    def post_with_link(self, message, title, uri, description=None, image_url=None):
        if not self.enabled:
            return
            
        try:
            external = {
                'uri': uri,
                'title': title,
                'description': description
            }
            if image_url:
                external['thumb'] = image_url
                
            self.client.send_post(text=message, external=external)
            print(f"Posted to Bluesky with link: {message}")
        except Exception as e:
            print(f"Failed to post to Bluesky: {e}")