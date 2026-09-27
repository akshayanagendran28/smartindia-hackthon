import os
import re

lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract dictionary for 'en'
en_start = text.find('"en": {', text.find('export const DICTIONARY'))
en_end = text.find('\n  },\n  "hi": {', en_start)
en_dict_text = text[en_start:en_end]

lines = [l.strip() for l in en_dict_text.split('\n') if ':' in l and l.startswith('"')]
print(f'Total English dictionary keys: {len(lines)}')
print('First 20 keys:')
for l in lines[:20]:
    print('  ', l[:80])
