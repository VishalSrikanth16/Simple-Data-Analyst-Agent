import requests

TOGETHER_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key :D

def ask_llama(prompt):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
        print("🔍 API raw response:", data)
    except Exception as e:
        print("❌ JSON parsing failed:", e)
        print("Raw content:", response.text)
        raise
    if "choices" in data:
        return data["choices"][0]["text"].strip()
    else:
        return "⚠️ No response text received from LLaMA."
