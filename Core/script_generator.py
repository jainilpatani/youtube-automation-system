# Core/script_generator.py
from openai import OpenAI
from config import OPENAI_API_KEY
import random

client = OpenAI(api_key=OPENAI_API_KEY)

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
    # Automation / Workflow
    "automation": "I built this workflow using [ZAPIER/MAKE]. Template below.",
    "agent": "Deploy your own agents with [AGENT_PLATFORM]. Link in description.",
    "support": "Automate your helpdesk with [CS_AI_TOOL].",

    # Marketing / Sales
    "marketing": "Scale your outreach with [EMAIL_TOOL]. Free trial below.",
    "lead": "Capture more leads using [CRM_NAME].",
    "sales": "Automate your follow-ups with [SALES_AI].",

    # Infrastructure
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
            # Insert a "Tool Recommendation" block
            parts.insert(2, f"\n(💡 PRO TIP: {offer})\n")
            return "\n\n".join(parts)

    return script_text


def generate_original_script(topic: str) -> str:
    angle = random.choice(UNIQUE_ANGLES)

    prompt = f"""
    You are a Business Automation Consultant.
    You are explaining a strategy to business owners and entrepreneurs.

    TOPIC:
    {topic}

    ANGLE:
    {angle}

    GOAL:
    Convince the viewer that adopting this AI/Automation strategy will save them time or money.

    TONE Rules:
    - Professional but accessible (Smart Casual)
    - Focus on ROI (Return on Investment)
    - No fluff or "hustle culture" slang
    - Concrete examples of business application

    STRUCTURE:
    1. The Pain Point (Why the old way is expensive/slow)
    2. The Solution (The specific automation strategy)
    3. The Implementation (How to actually do it)
    4. The Result (Expected savings/growth)

    LENGTH:
    900–1200 words

    OUTPUT:
    Final script text only.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw_script = response.choices[0].message.content.strip()
    return inject_affiliate(raw_script, topic)