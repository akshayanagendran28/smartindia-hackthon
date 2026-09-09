import urllib.request
import json
import time

t0 = time.time()
req_body = {
    "model": "qwen3:4b",
    "messages": [
        {"role": "system", "content": "You are Scheme Sathi, an expert AI assistant for government schemes. Answer in 2 sentences in English."},
        {"role": "user", "content": "Tell me about PMEGP subsidy for rural SC women."}
    ],
    "stream": False,
    "options": {
        "num_predict": 100,
        "temperature": 0.2
    }
}

req = urllib.request.Request(
    "http://127.0.0.1:11434/api/chat",
    data=json.dumps(req_body).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"Generated via /api/chat in {time.time()-t0:.2f}s:")
        msg = res.get("message", {})
        print("Role:", msg.get("role"))
        print("Content:", repr(msg.get("content")))
except Exception as e:
    print("Error:", e)
