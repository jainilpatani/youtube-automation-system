from google import genai
from google.genai import errors
import os
import random
import time
from config import GEMINI_API_KEY

# B2B Angles: Focus on "Efficiency" and "Profit", not "Fear"
UNIQUE_ANGLES = [
    "analyze the cost-savings of this approach",
    "explain how a 1-person team can execute this",
    "compare the old manual way vs the new automated way",
    "focus on the competitive advantage for early adopters",
    "explain this as a 'lean business' strategy"
]

# High-Ticket B2B Affiliate Triggers
AFFILIATE_OFFERS = {
    "automation": "I built this workflow using [ZAPIER/MAKE]. Template below.",
    "agent": "Deploy your own agents with [AGENT_PLATFORM]. Link in description.",
    "support": "Automate your helpdesk with [CS_AI_TOOL].",
    "marketing": "Scale your outreach with [EMAIL_TOOL]. Free trial below.",
    "lead": "Capture more leads using [CRM_NAME].",
    "sales": "Automate your follow-ups with [SALES_AI].",
    "website": "Host your AI apps on [VPS_PROVIDER]. Best performance.",
    "data": "Organize your business data with [AIRTABLE/NOTION]."
}


def inject_affiliate(script_text: str, topic: str) -> str:
    """Injects B2B offers naturally."""
    topic_lower = topic.lower()
    offer = ""
    for keyword, pitch in AFFILIATE_OFFERS.items():
        if keyword in topic_lower:
            offer = pitch
            break

    if offer:
        parts = script_text.split("\n\n")
        if len(parts) > 2:
            parts.insert(2, f"\n(💡 PRO TIP: {offer})\n")
            return "\n\n".join(parts)
    return script_text


def generate_original_script(topic: str) -> str:
    angle = random.choice(UNIQUE_ANGLES)
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    You are a Business Automation Consultant.
    TOPIC: {topic}
    ANGLE: {angle}

    GOAL: Convince the viewer that adopting this AI strategy will save them time/money.
    TONE: Professional, ROI-focused, No fluff.
    STRUCTURE: Pain Point -> Solution -> Implementation -> Result.
    LENGTH: 800–1200 words.
    """

    # 💎 PREMIUM MODEL
    model_name = "gemini-2.5-pro"

    print(f"💎 PREMIUM: Using Model {model_name} for maximum uniqueness...")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            raw_script = response.text.strip()
            return inject_affiliate(raw_script, topic)

        except errors.ServerError as e:
            print(f"⚠️ Server Overloaded (Attempt {attempt + 1}/{max_retries}). Waiting 10s...")
            time.sleep(10)
        except Exception as e:
            print(f"❌ Error generating script: {e}")
            break

    return "Error: Could not generate script due to server overload."