# -*- coding: utf-8 -*-
import json
import re

print("Starting generation of comprehensive LanguageContext.jsx...")

# Let's read the existing SCHEME_MAP and base LANGUAGES from LanguageContext.jsx
lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    orig_code = f.read()

scheme_map_start = orig_code.find('export const SCHEME_MAP = {')
scheme_map_end = orig_code.find('export const DICTIONARY = {')
scheme_map_str = orig_code[scheme_map_start:scheme_map_end].strip()

# Build exhaustive translations for the 12 languages
LANGS = ['en', 'hi', 'ta', 'te', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'or', 'as']

# Import the domain dictionary from indic_translation.py if possible
import sys
sys.path.append(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\backend')
from app.services.indic_translation import SamanantarIndicTranslationService

print("Loaded SamanantarIndicTranslationService with", len(SamanantarIndicTranslationService.EXPLAINABILITY_CORPUS), "corpus entries and", len(SamanantarIndicTranslationService.DOMAIN_LEXICON), "lexicon entries.")
