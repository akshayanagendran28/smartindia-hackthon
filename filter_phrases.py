import os
import re

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\all_clean_strings.txt', 'r', encoding='utf-8') as f:
    raw_lines = [l.strip() for l in f if l.strip()]

genuine_phrases = []
for l in raw_lines:
    # Filter out code artifacts, urls, endpoints, html fragments
    if any(l.startswith(x) for x in ['/', 'http', 'className', 'style=', ') :', '( ', 'import ', 'export ', 'const ', 'let ', 'var ', 'return ', '<', '>']):
        continue
    if any(x in l for x in ['===', '!==', '&&', '||', '=>', 'function(', '${', 'px ', 'rem ']):
        continue
    if len(l) < 2:
        continue
    # Strip quotes if surrounded
    cleaned = l.strip('"\'')
    if len(cleaned) > 1 and re.search(r'[a-zA-Z]', cleaned):
        genuine_phrases.append(cleaned)

genuine_phrases = sorted(list(set(genuine_phrases)))
print(f'Total genuine user-facing phrases: {len(genuine_phrases)}')

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\genuine_phrases.txt', 'w', encoding='utf-8') as f:
    for p in genuine_phrases:
        f.write(p + '\n')
