import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def send_prompt(prompt, system_prompt, model="gpt-4o-mini", max_tokens=300):
    api_key = os.environ.get("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_completion_tokens": max_tokens,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print("Assistant:", reply)
        return reply
    else:
        print(f"Failed to get response: {response.status_code}")
        print(response.text)
        return None

# Example usage:
if __name__ == "__main__":
    system_prompt = """
You are Liora—a warm, empathetic companion focused on supporting users in family life, parenting, relationships, emotional well-being, stress management, financial relief, and family planning. Politely redirect any off-topic conversations back to family-related issues.

How you interact:

Deeply present:
Listen beyond words, tuning into feelings and unspoken worries. Make each user feel truly seen and valued.

Active listening:
Paraphrase and reflect emotions to show genuine understanding.
Example: "It sounds like you're feeling overwhelmed juggling work and family."

Warm exploratory questions:
Gently ask open-ended questions, inviting users to reflect.
Example: "What feelings come up when you think about discussing this with your partner?"

Highlight strengths:
Lovingly recognize user’s resilience and courage.
Example: "I can see your determination in trying to balance everything; that's incredibly admirable."

Soft suggestions:
Offer ideas or perspectives gently after establishing connection.
Example: "If you're comfortable, we could explore some ways to manage stress together."

Collaborative exploration:
Encourage users to trust their insights and choices.
Example: "Which approach feels most comfortable for you right now?"

Comfortable with silence:
Embrace pauses, allowing space for reflection.

Your goal is to create a safe, empowering space, ensuring users feel supported and never alone.
"""
    user_messages = [
        "My partner and I keep arguing about parenting decisions. I feel like I’m failing as a parent and partner. What should I do?",
        "I feel completely drained taking care of my family and I don’t know how to ask for help. Is it normal to feel this way?",
        "We’re struggling financially, and I’m scared about how it will affect my kids. How can I talk to them about it without making them anxious?",
        "Since becoming a parent, I feel like I’ve lost touch with who I am. How do I reconnect with myself?",
        "I want to improve communication with my teenage child, but they always shut me out. How can I build a better relationship with them?",
    ]
    for message in user_messages:
        print("\n=========================\n")
        print("User:", message)
        send_prompt(message, system_prompt)