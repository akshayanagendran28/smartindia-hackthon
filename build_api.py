import os
import json

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def write(rel_path, content):
    p = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {rel_path}")

print("Writer helper ready.")
