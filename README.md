# 🎯 AI-Assisted TikTok Ad Campaign Creation Agent

An AI-assisted conversational agent that guides users through creating a TikTok ad campaign.

The system combines **Google Gemini (LLM)** for natural conversation with **deterministic business rules** to validate inputs and generate a production-ready ad payload (JSON).

This project was built as part of an AI Engineer assignment to demonstrate real-world AI agent design.

---

## ✨ Key Highlights

- 🤖 **AI-assisted conversation** using Google Gemini
- 🧠 **Hybrid architecture** (AI + deterministic validation)
- 🔐 **Simulated TikTok OAuth flow**
- 🎵 **Music validation & upload simulation**
- 📦 **Produces a validated TikTok ad payload**
- 💻 **CLI-based interface**
- 🧪 **Mock TikTok Ads API** with realistic error handling

---

## 🧠 How AI Is Used

**AI (Google Gemini)** is used to:
- Understand free-form user input
- Handle questions, ambiguity, and clarification
- Guide the user through a multi-step campaign creation flow
- Generate friendly, human-like responses

**All business-critical logic** (objectives, CTA, music rules, payload structure) is enforced **deterministically** to ensure correctness and safety—mirroring production AI systems.

---

## 🗂 Project Structure
```
.
├── agent.py              # Core AI + rule-based agent
├── main.py               # CLI entry point
├── mock_tiktok_api.py    # Mock TikTok Ads API
├── config.py             # Constants & configuration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── README.md             # Documentation
└── .venv/                # Virtual environment
```

---

## ⚙️ Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/tiktok-ad-ai-agent.git
cd tiktok-ad-ai-agent
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
```

### 3️⃣ Activate the virtual environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

You should now see `(.venv)` in your terminal.

### 4️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5️⃣ Configure environment variables

Create a `.env` file in the project root:
```bash
touch .env
```

Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your free Gemini API key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## ▶️ Running the Project

### 🔹 CLI (Recommended)
```bash
python main.py
```

You will be guided step-by-step to create a TikTok ad campaign.

---

## 🧪 Example Interaction (CLI)
```
Campaign Name: Summer Discount 2026
Objective: Conversions
Ad Text: Heavy discounts available on our website
CTA: Shop Now
Music ID: music_12345
```

### 📦 Final Output (Validated JSON)
```json
{
  "campaign_name": "Summer Discount 2026",
  "objective": "Conversions",
  "creative": {
    "text": "Heavy discounts available on our website",
    "cta": "Shop Now",
    "music_id": "music_12345"
  }
}
```

---

## 🔐 OAuth & API Simulation

Because real TikTok Ads APIs require approval, this project includes:

- ✅ Simulated OAuth authorization
- ✅ Mock access tokens
- ✅ Music validation & upload simulation
- ✅ Realistic API errors:
  - Rate limits
  - Invalid music IDs
  - Missing permissions
  - Geo-restrictions

---

## 🛠 Tech Stack

- **Python 3.8+**
- **Google Gemini** (google-genai SDK)
- **python-dotenv** for configuration

---

## 📌 Design Philosophy

- ✅ **AI assists** understanding and conversation
- ✅ **Deterministic logic** ensures correctness & safety
- ✅ Mirrors **production-grade AI agent architecture**
- ✅ Clear **separation of AI vs business logic**

---

## 🎯 Assignment Requirements Met

### ✅ TikTok OAuth Integration
- Simulated OAuth Authorization Code flow
- Error handling for invalid credentials, missing scopes, expired tokens

### ✅ Conversational Ad Creation
- Collects: Campaign Name, Objective, Ad Text, CTA, Music
- Validates all inputs according to business rules

### ✅ Music Logic (Primary Evaluation Area)
- **Case A:** Existing Music ID validation
- **Case B:** Custom music upload simulation
- **Case C:** No music (only allowed for Traffic campaigns)

### ✅ Prompting & Structured Output
- Separation of user conversation, internal reasoning, and final payload
- Structured JSON output
- Clear validation messages

### ✅ API Failure Reasoning
- Interprets OAuth errors, music validation failures, submission errors
- Suggests corrective actions
- Decides retry feasibility

---

## 👤 Author

**Jaineel Purani**  
AI/ML Engineering Student  
Ahmedabad, India

---

## 📜 License

This project is for educational and evaluation purposes.

---

## 🚀 Quick Start (Copy-Paste Commands)
```bash
# Clone and setup
git clone https://github.com/your-username/tiktok-ad-ai-agent.git
cd tiktok-ad-ai-agent
python -m venv .venv

# Activate virtual environment (choose your OS)
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file and add your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the agent
python main.py
```

**Get your free Gemini API key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
