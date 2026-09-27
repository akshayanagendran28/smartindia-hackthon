import os
import re
import json

lang_file = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_file, 'r', encoding='utf-8') as f:
    code = f.read()

# Let's see what keys are in DICTIONARY['hi']
hi_start = code.find('"hi": {', code.find('export const DICTIONARY'))
hi_end = code.find('\n  },\n  "ta": {', hi_start)
hi_text = code[hi_start:hi_end]
hi_keys = re.findall(r'"([^"]+)":', hi_text)
print('Number of keys in DICTIONARY["hi"]:', len(hi_keys))
print('Sample keys:', hi_keys[:15])
