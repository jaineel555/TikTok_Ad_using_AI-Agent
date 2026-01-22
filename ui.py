import streamlit as st
from agent import HybridTikTokAgent

st.set_page_config(page_title="TikTok Ad AI Agent", layout="centered")

st.title("🎯 TikTok Ad Campaign AI Agent")
st.caption("Hybrid AI Agent with deterministic validation")

agent = HybridTikTokAgent()

st.header("Campaign Details")

campaign_name = st.text_input("Campaign Name (min 3 chars)")
objective = st.selectbox("Objective", ["Traffic", "Conversions"])
ad_text = st.text_area("Ad Text (max 100 chars)")
cta = st.selectbox(
    "Call To Action",
    ["Shop Now", "Learn More", "Sign Up", "Download", "Get App", "Watch Now"]
)

st.header("Music")

music_option = st.radio(
    "Music Option",
    ["No Music", "Use Existing Music", "Upload Custom Music"]
)

music_id = None
if music_option == "Use Existing Music":
    music_id = st.text_input("Enter Music ID (e.g. music_12345)")
elif music_option == "Upload Custom Music":
    music_file = st.file_uploader("Upload Music File")

if st.button("Create Campaign"):
    with st.spinner("Validating and creating campaign..."):
        result = agent.run_from_ui(
            campaign_name=campaign_name,
            objective=objective,
            ad_text=ad_text,
            cta=cta,
            music_option=music_option,
            music_id=music_id
        )

    if "error" in result:
        st.error(result["error"])
    else:
        st.success("Campaign created successfully!")
        st.json(result["payload"])
