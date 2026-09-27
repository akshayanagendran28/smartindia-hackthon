# -*- coding: utf-8 -*-
"""
Compiles the complete master LanguageContext.jsx for Scheme Sathi.
"""

import os
import json
import re

print("Compiling Scheme Sathi Complete Multilingual Master Context...")

lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    orig_code = f.read()

scheme_map_start = orig_code.find('export const SCHEME_MAP = {')
scheme_map_end = orig_code.find('export const DICTIONARY = {')
scheme_map_str = orig_code[scheme_map_start:scheme_map_end].strip()

# Import base master translations from master_entries.json
with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\master_entries.json', 'r', encoding='utf-8') as f:
    master_entries = json.load(f)

print(f"Loaded {len(master_entries)} base entries from master_entries.json.")
