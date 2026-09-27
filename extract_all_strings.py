import os
import re
import glob

src_dir = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src'
backend_file = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\backend\app\routers\questions.py'

jsx_files = glob.glob(os.path.join(src_dir, '**', '*.jsx'), recursive=True)

found_t_strings = set()
found_jsx_strings = set()

# Regex for t('...') and t("...")
t_regex = re.compile(r"""t\(\s*['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?\s*\)""")

for fpath in jsx_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = t_regex.findall(content)
    for m in matches:
        if m[0]:
            found_t_strings.add(m[0].strip())
        if m[1]:
            found_t_strings.add(m[1].strip())

# Also scan backend questions.py
with open(backend_file, 'r', encoding='utf-8') as f:
    bcontent = f.read()

labels = re.findall(r'"label":\s*"([^"]+)"', bcontent)
titles = re.findall(r'"title":\s*"([^"]+)"', bcontent)
subtitles = re.findall(r'"subtitle":\s*"([^"]+)"', bcontent)
help_texts = re.findall(r'"help_text":\s*"([^"]+)"', bcontent)
badges = re.findall(r'"badge":\s*"([^"]+)"', bcontent)

for s in labels + titles + subtitles + help_texts + badges:
    found_t_strings.add(s.strip())

print(f'Total unique strings found: {len(found_t_strings)}')
# Save to file for processing
with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\all_extracted_strings.txt', 'w', encoding='utf-8') as f:
    for s in sorted(found_t_strings):
        f.write(s + '\n')
