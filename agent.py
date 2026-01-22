import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, VALID_OBJECTIVES, VALID_CTAS, MAX_AD_TEXT_LENGTH, MIN_CAMPAIGN_NAME_LENGTH
from mock_tiktok_api import MockTikTokAPI

class HybridTikTokAgent:
    
    def __init__(self):
        # Configure Gemini
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Initialize API
        self.api = MockTikTokAPI()
        auth_result = self.api.oauth_authorize("valid_client", "valid_secret")
        if auth_result["success"]:
            print("✅ OAuth Authentication Successful")
        
        self.ad_data = {
            "campaign_name": None,
            "objective": None,
            "ad_text": None,
            "cta": None,
            "music_option": None,
            "music_id": None
        }
        self.current_step = "start"
        self.conversation_history = []
    
    def _call_gemini(self, prompt):

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            text = response.text.strip()
            text = text.replace('```', '').strip()
            return text
        except Exception as e:
            print(f"⚠️ Gemini error: {e}")
            return None
    
    def _is_question(self, text):
        question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'is', 'are', 'can', 'should', 'do', 'does']
        text_lower = text.lower().strip()
        
        if text_lower.endswith('?'):
            return True
        
        first_word = text_lower.split()[0] if text_lower.split() else ""
        if first_word in question_words:
            return True
        
        return False
    
    def chat(self, user_message):
        """Main conversation interface"""
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Route to appropriate handler
        if self.current_step == "start":
            response = "👋 Hi! I'll help you create an AI TikTok ad campaign.\n\nLet's start with the basics. What would you like to name your campaign? (minimum 3 characters)"
            self.current_step = "collect_campaign_name"
        
        elif self.current_step == "collect_campaign_name":
            response = self._handle_campaign_name(user_message)
        
        elif self.current_step == "collect_objective":
            response = self._handle_objective(user_message)
        
        elif self.current_step == "collect_ad_text":
            response = self._handle_ad_text(user_message)
        
        elif self.current_step == "collect_cta":
            response = self._handle_cta(user_message)
        
        elif self.current_step == "collect_music":
            response = self._handle_music(user_message)
        
        elif self.current_step == "validate":
            response = self._validate_and_submit()
        
        else:
            response = "I'm not sure what to do next. Let's start over."
            self.current_step = "start"
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _handle_campaign_name(self, user_input):
        """Collect campaign name with smart validation"""
        
        # Check if user is asking a question
        if self._is_question(user_input):
            return "A campaign name is a title for your ad campaign (Example like 'Summer Sale 2024' or 'Product Launch'). It needs to be at least 3 characters. What would you like to name your campaign?"
        
        name = user_input.strip()
        
        # Validate length
        if len(name) < MIN_CAMPAIGN_NAME_LENGTH:
            return f"❌ Campaign name is too short. You entered '{name}' which is {len(name)} character(s). Please provide at least {MIN_CAMPAIGN_NAME_LENGTH} characters:"
        
        # Success
        self.ad_data["campaign_name"] = name
        self.current_step = "collect_objective"
        
        return f"✅ Great! Campaign name set to: '{name}'\n\nNow, what's your campaign objective?\n1. Traffic - Drive users to your website\n2. Conversions - Drive specific actions (purchases, sign-ups)\n\nPlease type: Traffic or Conversions"
    
    def _handle_objective(self, user_input):
        """Collect objective with clear validation"""
        
        if self._is_question(user_input):
            return "These are the only two objectives TikTok offers:\n• Traffic - Gets people to visit your website\n• Conversions - Gets people to take action (buy, sign up, download)\n\nWhich one do you want? Type: Traffic or Conversions"
        
        objective = user_input.strip().capitalize()
        
        # Validate
        if objective not in VALID_OBJECTIVES:
            return f"❌ '{user_input}' is not a valid objective.\n\nPlease choose exactly:\n• Traffic (for website visits)\n• Conversions (for purchases/sign-ups)\n\nType one of these:"
        
        # Success
        self.ad_data["objective"] = objective
        self.current_step = "collect_ad_text"
        
        music_note = ""
        if objective == "Conversions":
            music_note = "\n\n⚠️ Important: Music is mandatory for Conversions campaigns."
        
        return f"✅ Objective set to: {objective}{music_note}\n\nWhat text would you like to display in your ad?\n(Maximum {MAX_AD_TEXT_LENGTH} characters - this is the main message users will see)"
    
    def _handle_ad_text(self, user_input):
        """Collect ad text with clear validation"""
        
        if self._is_question(user_input):
            return f"Yes, ad text is required. It's the main message that appears in your ad (like 'Summer Sale - 50% Off!' or 'New Collection Out Now'). Maximum {MAX_AD_TEXT_LENGTH} characters.\n\nWhat message would you like to show?"
        
        text = user_input.strip()
        
        # Validate
        if len(text) == 0:
            return "❌ Ad text cannot be empty. Please enter the message you want to show in your ad:"
        
        if len(text) > MAX_AD_TEXT_LENGTH:
            return f"❌ Ad text is too long!\n\nYour text: '{text}'\nLength: {len(text)} characters\nMaximum: {MAX_AD_TEXT_LENGTH} characters\n\nPlease shorten your message by {len(text) - MAX_AD_TEXT_LENGTH} characters:"
        
        # Success
        self.ad_data["ad_text"] = text
        self.current_step = "collect_cta"
        
        return f"✅ Ad text set!\n\nNow, what Call-to-Action (CTA) button would you like?\n\nAvailable options:\n• Shop Now\n• Learn More\n• Sign Up\n• Download\n• Get App\n• Watch Now\n\nPlease type one of these exactly:"
    
    def _handle_cta(self, user_input):
        """Collect CTA with fuzzy matching and clear errors"""

        if self._is_question(user_input):
            return "A CTA (Call-to-Action) is the button users click on your ad. Different buttons work for different goals:\n• Shop Now - for e-commerce\n• Learn More - for information\n• Sign Up - for registrations\n• Download - for apps\n• Get App - for mobile apps\n• Watch Now - for videos\n\nWhich one fits your ad best?"
        
        user_cta = user_input.strip().lower()
        
        matched_cta = None
        for valid_cta in VALID_CTAS:
            if user_cta == valid_cta.lower():
                matched_cta = valid_cta
                break
        
        # Try fuzzy matching
        if not matched_cta:
            cta_map = {
                'shop': 'Shop Now',
                'buy': 'Shop Now',
                'purchase': 'Shop Now',
                'learn': 'Learn More',
                'more': 'Learn More',
                'info': 'Learn More',
                'signup': 'Sign Up',
                'sign up': 'Sign Up',
                'register': 'Sign Up',
                'download': 'Download',
                'install': 'Download',
                'get': 'Get App',
                'app': 'Get App',
                'watch': 'Watch Now',
                'view': 'Watch Now',
                'play': 'Watch Now'
            }
            
            for keyword, cta in cta_map.items():
                if keyword in user_cta:
                    matched_cta = cta
                    break
        
        # Show error if no match
        if not matched_cta:
            return f"❌ '{user_input}' doesn't match any available CTA.\n\nPlease choose from these exact options:\n• Shop Now\n• Learn More\n• Sign Up\n• Download\n• Get App\n• Watch Now\n\nType one of these:"
        
        # Success
        self.ad_data["cta"] = matched_cta
        self.current_step = "collect_music"
        
        # Different prompts based on objective
        if self.ad_data["objective"] == "Conversions":
            return f"✅ CTA set to: {matched_cta}\n\n🎵 Music is REQUIRED for Conversions campaigns.\n\nHow would you like to add music?\n1. Use existing music (you provide a music ID)\n2. Upload custom music\n\nType 1 or 2:"
        else:
            return f"✅ CTA set to: {matched_cta}\n\n🎵 Would you like to add music to your ad?\n\n1. Use existing music (you provide a music ID)\n2. Upload custom music\n3. No music\n\nType 1, 2, or 3:"
    
    def _handle_music(self, user_input):
        """Handle music selection with clear guidance"""
        
        user_input = user_input.strip().lower()
        
        # If user is trying to skip music
        if user_input in ["3", "no music", "none", "no", "skip"]:
            if self.ad_data["objective"] == "Conversions":
                return f"❌ Cannot skip music for Conversions campaigns.\n\nWhy? Music significantly increases engagement, which is critical for driving conversions (purchases, sign-ups, etc.).\n\nPlease choose option 1 or 2:"
            
            self.ad_data["music_option"] = "none"
            self.ad_data["music_id"] = None
            self.current_step = "validate"
            # Automatically proceed to validation - no need for user input
            return self._validate_and_submit()
        
        if user_input in ["1", "existing", "use existing"]:
            self.ad_data["music_option"] = "existing"
            return "Please enter the Music ID (example: music_12345):"
        
        if user_input in ["2", "upload", "custom"]:
            self.ad_data["music_option"] = "custom"
            return "Please enter the file path of your music file (example: /path/to/song.mp3):"
        
        # Handling music ID validation
        if self.ad_data["music_option"] == "existing":
            music_id = user_input
            result = self.api.validate_music_id(music_id)
            
            if result["success"]:
                self.ad_data["music_id"] = music_id
                self.current_step = "validate"
                # Automatically proceed to validation
                return f"✅ Music validated successfully!\n\nMusic: {result['title']}\nDuration: {result['duration']}s\n\n" + self._validate_and_submit()
            else:
                error_msg = f"❌ Music validation failed\n\nMusic ID: {music_id}\nError: {result['message']}\n\n"
                
                if self.ad_data["objective"] == "Conversions":
                    error_msg += "What would you like to do?\n1. Try a different music ID\n2. Upload custom music\n\nType 1 or 2:"
                else:
                    error_msg += "What would you like to do?\n1. Try a different music ID\n2. Upload custom music\n3. Continue without music\n\nType 1, 2, or 3:"
                
                return error_msg
        
        # file upload
        if self.ad_data["music_option"] == "custom":
            file_path = user_input
            result = self.api.upload_music(file_path)
            
            if result["success"]:
                self.ad_data["music_id"] = result["music_id"]
                self.current_step = "validate"
                return f"✅ Music uploaded successfully!\n\nGenerated Music ID: {result['music_id']}\n\n" + self._validate_and_submit()
            else:
                return f"❌ Upload failed: {result['message']}\n\nPlease try again with a valid file path:"
        
        # Invalid input
        if self.ad_data["objective"] == "Conversions":
            return "❌ Invalid choice. Please type 1 or 2:"
        else:
            return "❌ Invalid choice. Please type 1, 2, or 3:"
    
    def _validate_and_submit(self):
        """Final validation and submission"""
        
        # Show reasoning
        print("\nINTERNAL REASONING:")
        print("="*50)
        print("✓ Validating all required fields are collected...")
        print(f"✓ Campaign Name: '{self.ad_data['campaign_name']}' (min 3 chars) - VALID")
        print(f"✓ Objective: '{self.ad_data['objective']}' (Traffic/Conversions) - VALID")
        print(f"✓ Ad Text: {len(self.ad_data['ad_text'])} chars (max 100) - VALID")
        print(f"✓ CTA: '{self.ad_data['cta']}' - VALID")
        
        # Check music logic
        if self.ad_data['objective'] == 'Conversions' and not self.ad_data['music_id']:
            print("✗ Music: MISSING (required for Conversions) - INVALID")
            print("="*50)
            return "❌ Validation failed: Music is mandatory for Conversions campaigns."
        elif self.ad_data['music_id']:
            print(f"✓ Music: '{self.ad_data['music_id']}' - VALID")
        else:
            print("✓ Music: None (optional for Traffic) - VALID")
        
        print("✓ All validations passed!")
        print("="*50)
        
        # Build payload
        payload = {
            "campaign_name": self.ad_data["campaign_name"],
            "objective": self.ad_data["objective"],
            "creative": {
                "text": self.ad_data["ad_text"],
                "cta": self.ad_data["cta"],
                "music_id": self.ad_data["music_id"]
            }
        }
        
        # Display summary
        summary = f"\n{'='*50}\n📊 AD CAMPAIGN SUMMARY\n{'='*50}\n"
        summary += f"Campaign Name: {payload['campaign_name']}\n"
        summary += f"Objective: {payload['objective']}\n"
        summary += f"Ad Text: {payload['creative']['text']}\n"
        summary += f"CTA: {payload['creative']['cta']}\n"
        summary += f"Music ID: {payload['creative']['music_id'] or 'None'}\n"
        summary += f"{'='*50}\n"
        print(summary)
        
        print("📤 Submitting to TikTok Ads API...")
        
        result = self.api.submit_ad(payload)
        
        if result["success"]:
            self.current_step = "complete"
            return f"\n🎉 SUCCESS! Your ad campaign has been created!\n\n📋 Campaign Details:\n• Campaign ID: {result['campaign_id']}\n• Ad ID: {result['ad_id']}\n• Status: {result['status']}\n\nYour ad is now live on TikTok!"
        else:
            # error handling
            error_type = result.get("error")
            message = result.get("message")
            
            error_responses = {
                "unauthorized": f"🔒 Authentication Error\n\n{message}\n\nAction needed: Please re-authenticate with TikTok. Your access token may have expired.",
                
                "missing_music": f"🎵 Missing Music\n\n{message}\n\nThis happened because:\n• Objective is set to 'Conversions'\n• Music is mandatory for Conversions\n\nPlease add music to continue.",
                
                "invalid_music_id": f"❌ Invalid Music\n\n{message}\n\nThe music ID may have been:\n• Removed from TikTok's library\n• Restricted in your region\n• Typed incorrectly\n\nPlease use a different music ID.",
                
                "rate_limit": f"⏱️ Rate Limit Exceeded\n\n{message}\n\nTikTok's API has rate limits. Please wait 60 seconds and try again.",
                
                "geo_restriction": f"🌍 Geographic Restriction\n\n{message}\n\nAction needed:\n1. Check your TikTok Ads account region settings\n2. Verify your business is approved for ads in your region\n3. Contact TikTok support if issue persists",
                
                "insufficient_permissions": f"🔐 Permission Error\n\n{message}\n\nHow to fix:\n1. Go to TikTok Developer Portal\n2. Navigate to your app settings\n3. Add 'Ads Management' permission scope\n4. Re-authenticate with the new permissions"
            }
            
            return error_responses.get(error_type, f"❌ Submission failed: {message}")
    
    def get_payload(self):
        """Return final payload"""
        return {
            "campaign_name": self.ad_data["campaign_name"],
            "objective": self.ad_data["objective"],
            "creative": {
                "text": self.ad_data["ad_text"],
                "cta": self.ad_data["cta"],
                "music_id": self.ad_data["music_id"]
            }
        }
        
    def run_from_ui(self, campaign_name, objective, ad_text, cta, music_option, music_id=None):
        """Run the agent from UI inputs (for Streamlit)"""
        
        self.ad_data["campaign_name"] = campaign_name.strip()
        
        self.ad_data["objective"] = objective.strip().capitalize()
        
        self.ad_data["ad_text"] = ad_text.strip()
        
        self.ad_data["cta"] = cta.strip()
        
        self.ad_data["music_option"] = music_option.lower()
        
        if music_option == "No Music":
            if self.ad_data["objective"] == "Conversions":
                return {"error": "Music is mandatory for Conversions campaigns. Please add music."}
            self.ad_data["music_id"] = None
        elif music_option == "Use Existing Music":
            if not music_id:
                return {"error": "Please provide a Music ID."}
            result = self.api.validate_music_id(music_id)
            if not result["success"]:
                return {"error": f"Music validation failed: {result['message']}"}
            self.ad_data["music_id"] = music_id
        elif music_option == "Upload Custom Music":
            result = self.api.upload_music("path/to/uploaded/file")
            if not result["success"]:
                return {"error": f"Music upload failed: {result['message']}"}
            self.ad_data["music_id"] = result["music_id"]
        
        self.current_step = "validate"
        submission_response = self._validate_and_submit()
        
        if self.current_step == "complete":
            return {"payload": self.get_payload()}
        else:
            return {"error": submission_response}