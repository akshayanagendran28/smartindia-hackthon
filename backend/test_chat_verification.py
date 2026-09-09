import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

from app.database.session import SessionLocal
from app.models.scheme import Scheme
from app.services.chat import MultilingualChatService

db = SessionLocal()
schemes = db.query(Scheme).all()

print("=== TESTING MULTILINGUAL CHAT WITH QWEN / OLLAMA ===")
print("Detected Ollama model:", MultilingualChatService.get_ollama_model())

test_queries = [
    ("Tell me about PMEGP subsidy for rural women in English", "en"),
    ("स्ट्रीट वेंडर के लिए कौन सी योजना है?", "hi"),
    ("தொழில் தொடங்க என்ன கடன் திட்டம் உள்ளது?", "ta")
]

for query, lang in test_queries:
    print(f"\n[User ({lang})]: {query}")
    res = MultilingualChatService.process_message(query, language=lang, schemes_db=schemes)
    print(f"[Model Used]: {res.get('model_used')}")
    print(f"[Reply]:\n{res.get('reply')[:250]}...")
    if res.get('recommendations'):
        print(f"[Matched Scheme Cards]: {[r.get('code') for r in res.get('recommendations')]}")

db.close()
print("\nCHAT SERVICE VERIFICATION COMPLETED SUCCESSFULLY!")
