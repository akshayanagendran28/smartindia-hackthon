import os
import re
import glob

src_dir = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src'
jsx_files = glob.glob(os.path.join(src_dir, '**', '*.jsx'), recursive=True)

all_strings = set()

# Read existing strings from all_extracted_strings.txt if available
txt_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\all_extracted_strings.txt'
if os.path.exists(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s:
                all_strings.add(s)

# Regex patterns for finding text in JSX
# 1. >Text< (excluding {expressions} and tags)
jsx_text_pattern = re.compile(r'>\s*([^<>{}\n]+?)\s*<')
# 2. placeholder="..."
placeholder_pattern = re.compile(r'placeholder=["\']([^"\']+)["\']')
# 3. title="..."
title_pattern = re.compile(r'title=["\']([^"\']+)["\']')
# 4. alt="..."
alt_pattern = re.compile(r'alt=["\']([^"\']+)["\']')
# 5. t('...')
t_pattern = re.compile(r"""t\(\s*['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?\s*\)""")

for fpath in jsx_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Matches
    for m in t_pattern.findall(content):
        if m[0] and len(m[0].strip()) > 1:
            all_strings.add(m[0].strip())
        if m[1] and len(m[1].strip()) > 1:
            all_strings.add(m[1].strip())

    for m in placeholder_pattern.findall(content):
        if m and len(m.strip()) > 1 and not m.startswith('http'):
            all_strings.add(m.strip())

    for m in title_pattern.findall(content):
        if m and len(m.strip()) > 1 and not m.startswith('http'):
            all_strings.add(m.strip())

    for m in alt_pattern.findall(content):
        if m and len(m.strip()) > 1:
            all_strings.add(m.strip())

    for m in jsx_text_pattern.findall(content):
        s = m.strip()
        # Filter out numbers, punctuation, css, code
        if s and len(s) > 1 and not re.match(r'^[\d\s\.,;:!?@#\$%\^&\*\(\)_\+\-=\[\]\{\}\|\\/<>\'\"]+$', s):
            if not s.startswith('&') and not s.startswith('http') and not s.startswith('console.'):
                all_strings.add(s)

print(f'Total extracted candidate strings: {len(all_strings)}')

# Filter strings: length > 1, contains letters
clean_strings = []
for s in sorted(all_strings):
    if re.search(r'[a-zA-Z]', s) and not s.startswith('className') and not s.startswith('style='):
        clean_strings.append(s)

print(f'Total clean strings: {len(clean_strings)}')

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\all_clean_strings.txt', 'w', encoding='utf-8') as f:
    for s in clean_strings:
        f.write(s + '\n')
