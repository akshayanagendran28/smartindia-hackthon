# -*- coding: utf-8 -*-
import json
import re

# Load existing LanguageContext.jsx to preserve SCHEME_MAP and existing DICTIONARY keys
lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    orig_code = f.read()

# Extract SCHEME_MAP verbatim
scheme_map_start = orig_code.find('export const SCHEME_MAP = {')
scheme_map_end = orig_code.find('export const DICTIONARY = {')
scheme_map_str = orig_code[scheme_map_start:scheme_map_end].strip()

print('SCHEME_MAP extracted length:', len(scheme_map_str))
