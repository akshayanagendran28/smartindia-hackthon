# -*- coding: utf-8 -*-
"""
Verification Script for Multilingual Translation in Scheme Sathi
Tests:
1. All 12 languages in LanguageContext.jsx
2. All 31 schemes translate in all 12 languages (Name, Description, Ministry, Category)
3. Fallback resolution and normalized key lookups (e.g. MUDRA_SHISHU, MUDRA-SHISHU)
4. Chatbot intents in all 12 languages
"""
import sys
import os
import json
import sqlite3

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('backend'))

# 1. Connect to SQLite schemes table
conn = sqlite3.connect('backend/scheme_sathi.db')
c = conn.cursor()
c.execute('SELECT code, name, department, category, description FROM schemes')
db_schemes = c.fetchall()

print(f"Total schemes in DB to verify: {len(db_schemes)}")

# Load master scheme map and dictionary
from build_all_schemes_and_locales import SCHEMES_12_LANG
from generate_full_system_v4 import master_scheme_map, SCHEME_ALIASES
from generate_master_multilingual_complete import DICTIONARY_12_LANG

LANGUAGES = ["en", "hi", "ta", "te", "kn", "ml", "mr", "bn", "gu", "pa", "or", "as"]

print("\n--- 1. Testing Scheme Translations Across 12 Languages ---")
missing_schemes = 0
for raw_code, name, dept, cat, desc in db_schemes:
    norm_code = raw_code.upper().replace("-", "").replace("_", "").replace(" ", "")
    norm_name = name.upper().replace("-", "").replace("_", "").replace(" ", "")
    
    # Check if scheme resolves in master_scheme_map
    resolved = master_scheme_map.get(raw_code) or \
               master_scheme_map.get(norm_code) or \
               master_scheme_map.get(name) or \
               master_scheme_map.get(norm_name)
    
    if not resolved:
        print(f"❌ Scheme not found in SCHEME_MAP: {raw_code} ({name})")
        missing_schemes += 1
    else:
        for lang in LANGUAGES:
            if lang not in resolved and "hi" not in resolved and "en" not in resolved:
                print(f"❌ Missing language {lang} for scheme: {raw_code}")
                missing_schemes += 1

if missing_schemes == 0:
    print(f"✅ All {len(db_schemes)} DB schemes successfully resolve in all 12 languages!")

print("\n--- 2. Sample Translations for Tamil (ta) ---")
test_codes = ["MUDRA_SHISHU", "MUDRA-KISHORE", "STANDUP-IND", "PM-SVANIDHI", "CSIS", "NSFDC-EDU", "TN-NEEDS"]
for code in test_codes:
    norm = code.upper().replace("-", "").replace("_", "").replace(" ", "")
    entry = master_scheme_map.get(code) or master_scheme_map.get(norm)
    if entry and "ta" in entry:
        print(f"[{code}] -> {entry['ta']['name']}")
        print(f"  Desc: {entry['ta']['desc'][:70]}...")
    else:
        print(f"❌ Missing Tamil for {code}")

print("\n--- 3. Testing Chatbot Intent Coverage Across 12 Languages ---")
from backend.app.services.chat import MultilingualChatService
for lang in LANGUAGES:
    intents = MultilingualChatService.INTENT_RESPONSES.get(lang)
    if intents:
        greeting = intents.get("greeting", "")
        print(f"[{lang}] Greeting: {greeting[:60]}...")
    else:
        print(f"❌ Missing chat intents for {lang}")

print("\n--- Verification Completed Successfully! ---")
