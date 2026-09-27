import os
import re

lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    text = f.read()

print('File size in characters:', len(text))
langs = ['en', 'hi', 'ta', 'te', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'or', 'as']

# Find where DICTIONARY starts
dict_pos = text.find('export const DICTIONARY')
print('DICTIONARY position:', dict_pos)

# Find where PHRASE_MAP starts
phrase_pos = text.find('export const PHRASE_MAP')
print('PHRASE_MAP position:', phrase_pos)

# Find where SCHEME_MAP starts
scheme_pos = text.find('export const SCHEME_MAP')
print('SCHEME_MAP position:', scheme_pos)
