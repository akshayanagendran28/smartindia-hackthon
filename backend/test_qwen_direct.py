import urllib.request
import json

def test_qwen_chat(prompt_text, lang="en"):
    system_prompt = """You are Scheme Sathi, an expert, compassionate AI government financial scheme advisor for Indian entrepreneurs and marginalized founders (SC/ST, Women, OBC, Minorities, Artisans, Street Vendors).
You provide strictly factual, statutory information from the official myScheme.gov.in repository.
Key Scheme Rules:
- PMEGP: Up to Rs 50 Lakh for manufacturing (Rs 20L for services). Rural Special Category (SC/ST/Women/OBC/Minorities) get 35% capital subsidy with 5% own margin contribution.
- Stand-Up India: Rs 10 Lakh to Rs 1 Crore for SC/ST and Women greenfield enterprises.
- PM MUDRA: Shishu (up to Rs 50,000), Kishore (Rs 50,000 to Rs 5 Lakh), Tarun (Rs 5 Lakh to Rs 10 Lakh). Zero collateral.
- PM SVANidhi: Rs 10,000 to Rs 50,000 micro working capital for street vendors with 7% interest subvention.
- PM Vishwakarma: Rs 3 Lakh collateral-free loan at 5% concessional interest + Rs 15,000 toolkit voucher for traditional artisans.
- Mahila Samridhi: Up to Rs 1.4 Lakh at 4% interest for backward class women.

Respond clearly, concisely, and helpfully in the requested language."""

    full_prompt = f"{system_prompt}\n\nLanguage requested: {lang}\nUser Question: {prompt_text}\n\nScheme Sathi Answer:"

    body = {
        "model": "qwen3:4b",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9
        }
    }

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("response")

print("--- Testing Qwen on Ollama (English) ---")
print(test_qwen_chat("What is the subsidy for an SC woman starting a manufacturing unit under PMEGP in rural area?", "en"))

print("\n--- Testing Qwen on Ollama (Hindi) ---")
print(test_qwen_chat("स्ट्रीट वेंडर के लिए कौन सी योजना अच्छी है?", "hi"))
