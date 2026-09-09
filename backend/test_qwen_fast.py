import urllib.request
import json
import time

t0 = time.time()
req_body = {
    "model": "qwen3:4b",
    "prompt": "You are Scheme Sathi. Explain the PMEGP subsidy for rural SC women in 2 sentences.",
    "stream": False,
    "options": {
        "num_predict": 120,
        "temperature": 0.2
    }
}

req = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(req_body).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req, timeout=90) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print(f"Generated in {time.time()-t0:.2f} seconds:")
    print(res.get("response"))
