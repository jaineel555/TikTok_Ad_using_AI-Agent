import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MOCK_MODE = True

# Business Rules
VALID_OBJECTIVES = ["Traffic", "Conversions"]
VALID_CTAS = ["Shop Now", "Learn More", "Sign Up", "Download", "Get App", "Watch Now"]
MAX_AD_TEXT_LENGTH = 100
MIN_CAMPAIGN_NAME_LENGTH = 3

# Mock Music IDs
VALID_MUSIC_IDS = ["music_12345", "music_67890", "music_11111"]