import sys
from agent import HybridTikTokAgent

def main():
    print("\n" + "="*60)
    print("🎯 TIKTOK AD CAMPAIGN CREATION AGENT")
    print("🤖 Google Gemini AI")
    print("="*60)
    print("This AI agent will guide you through creating a TikTok Advertisment")
    print("Type 'quit' or 'exit' at any time to stop.")
    print("="*60 + "\n")
    
    # Initialize AI agent
    try:
        agent = HybridTikTokAgent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nPlease make sure:")
        print("1. You have set GEMINI_API_KEY in your .env file")
        print("2. You have installed all requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start conversation 
    response = agent.chat("start")
    print(f"\n🤖 Agent: {response}\n")
    
    while agent.current_step != "complete":
        try:
            if agent.current_step == "validate":
                continue
            
            user_input = input("You: ").strip()
            
            # Check for exit
            if user_input.lower() in ["quit", "exit", "stop"]:
                print("\n👋 Goodbye! Campaign creation cancelled.\n")
                break
            
            if not user_input:
                continue
            
            # Get AI agent response
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Campaign creation cancelled.\n")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")
            print("Please try again or type 'quit' to exit.\n")
    
    # Show final payload if completed
    if agent.current_step == "complete":
        print("\n" + "="*60)
        print("📦 FINAL AD PAYLOAD (JSON)")
        print("="*60)
        import json
        print(json.dumps(agent.get_payload(), indent=2))
        print("="*60 + "\n")

if __name__ == "__main__":
    main()