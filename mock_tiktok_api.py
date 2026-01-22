import random
import time
from config import VALID_MUSIC_IDS

class MockTikTokAPI:
    
    def __init__(self):
        self.access_token = None
        self.token_valid = False
    
    def oauth_authorize(self, client_id, client_secret):
        """OAuth flow"""
        print("\n🔐 Simulating OAuth Authorization...")
        time.sleep(1)
        
        # Invalid
        if client_id == "invalid":
            return {
                "success": False,
                "error": "invalid_client",
                "message": "Client ID is invalid"
            }
        
        if client_secret == "invalid":
            return {
                "success": False,
                "error": "invalid_secret",
                "message": "Client secret is invalid"
            }
        
        # Successful
        self.access_token = f"mock_token_{random.randint(1000, 9999)}"
        self.token_valid = True
        
        return {
            "success": True,
            "access_token": self.access_token,
            "token_type": "Bearer",
            "expires_in": 3600
        }
    
    def validate_music_id(self, music_id):
        """Check if music ID exists"""
        print(f"\n🎵 Validating Music ID: {music_id}")
        time.sleep(0.5)
        
        if not self.token_valid:
            return {
                "success": False,
                "error": "unauthorized",
                "message": "Access token is invalid or expired. Please re-authenticate."
            }
        
        if music_id in VALID_MUSIC_IDS:
            return {
                "success": True,
                "music_id": music_id,
                "title": f"Sample Track {music_id.split('_')[1]}",
                "duration": 30
            }
        else:
            return {
                "success": False,
                "error": "music_not_found",
                "message": f"Music ID '{music_id}' not found in TikTok library. It may have been removed or is unavailable in your region."
            }
    
    def upload_music(self, file_path):
        """Music upload"""
        print(f"\n⬆️  Uploading custom music: {file_path}")
        time.sleep(1)
        
        if not self.token_valid:
            return {
                "success": False,
                "error": "unauthorized",
                "message": "Access token is invalid or expired."
            }
        
        #Upload success
        new_music_id = f"music_{random.randint(20000, 99999)}"
        
        return {
            "success": True,
            "music_id": new_music_id,
            "message": "Music uploaded successfully"
        }
    
    def submit_ad(self, ad_payload):
        
        print("\n📤 Submitting ad to TikTok Ads API...")
        time.sleep(1)
        
        if not self.token_valid:
            return {
                "success": False,
                "error": "unauthorized",
                "message": "Access token is invalid or expired. Please re-authenticate."
            }
        
        # Check music logic
        objective = ad_payload.get("objective")
        music_id = ad_payload.get("creative", {}).get("music_id")
        
        if objective == "Conversions" and not music_id:
            return {
                "success": False,
                "error": "missing_music",
                "message": "Music is mandatory for Conversions campaigns. Please add music or change objective to Traffic."
            }
        
        # Check music ID if provided
        if music_id and music_id not in VALID_MUSIC_IDS:
            return {
                "success": False,
                "error": "invalid_music_id",
                "message": f"Music ID '{music_id}' is invalid or expired."
            }
        
        # random API failures
        if random.random() < 0.1:
            errors = [
                {
                    "error": "rate_limit",
                    "message": "Rate limit exceeded. Please try again in 60 seconds."
                },
                {
                    "error": "geo_restriction",
                    "message": "Ad creation is restricted in your geographic region (403 Forbidden)."
                },
                {
                    "error": "insufficient_permissions",
                    "message": "Your app doesn't have 'Ads Management' permission. Please update scopes in TikTok Developer portal."
                }
            ]
            error = random.choice(errors)
            return {
                "success": False,
                "error": error["error"],
                "message": error["message"]
            }
        
        # Success!
        ad_id = f"ad_{random.randint(100000, 999999)}"
        campaign_id = f"campaign_{random.randint(100000, 999999)}"
        
        return {
            "success": True,
            "ad_id": ad_id,
            "campaign_id": campaign_id,
            "message": "Ad campaign created successfully!",
            "status": "ACTIVE"
        }