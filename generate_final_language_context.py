# -*- coding: utf-8 -*-
"""
Assembles and writes the complete production-grade LanguageContext.jsx.
"""

import json
import os
import re

print("Loading data for LanguageContext.jsx generation...")

# 1. Load all translations
with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\all_translations_data.json', 'r', encoding='utf-8') as f:
    ALL_DATA = json.load(f)

# 2. Load existing SCHEME_MAP from LanguageContext.jsx
lang_path = r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx'
with open(lang_path, 'r', encoding='utf-8') as f:
    orig_code = f.read()

scheme_map_start = orig_code.find('export const SCHEME_MAP = {')
scheme_map_end = orig_code.find('export const DICTIONARY = {')
scheme_map_str = orig_code[scheme_map_start:scheme_map_end].strip()

LANGS = ['en', 'hi', 'ta', 'te', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'or', 'as']

# Construct DICTIONARY for 12 languages
dictionary_obj = {l: {} for l in LANGS}
phrase_map_obj = {l: {} for l in LANGS}

for en_key, trans in ALL_DATA.items():
    clean_k = en_key.strip()
    lower_k = clean_k.lower()
    for l in LANGS:
        val = trans.get(l, clean_k)
        dictionary_obj[l][clean_k] = val
        phrase_map_obj[l][lower_k] = val
        # Also strip trailing punctuation for loose matching
        norm_k = re.sub(r'[:\?\*\!]+$', '', clean_k).strip().lower()
        if norm_k != lower_k:
            phrase_map_obj[l][norm_k] = val

dict_json = json.dumps(dictionary_obj, ensure_ascii=False, indent=2)
phrase_json = json.dumps(phrase_map_obj, ensure_ascii=False, indent=2)

final_js_content = f"""import React, {{{{ createContext, useContext, useState, useEffect }}}} from 'react';
import api from '../services/api';

const LanguageContext = createContext();

export const LANGUAGES = [
  {{ code: 'en', name: 'English', native: 'English' }},
  {{ code: 'hi', name: 'Hindi', native: 'हिन्दी' }},
  {{ code: 'ta', name: 'Tamil', native: 'தமிழ்' }},
  {{ code: 'te', name: 'Telugu', native: 'తెలుగు' }},
  {{ code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' }},
  {{ code: 'ml', name: 'Malayalam', native: 'മലയാളം' }},
  {{ code: 'mr', name: 'Marathi', native: 'मराठी' }},
  {{ code: 'bn', name: 'Bengali', native: 'বাংলা' }},
  {{ code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' }},
  {{ code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' }},
  {{ code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' }},
  {{ code: 'as', name: 'Assamese', native: 'অসমীয়া' }}
];

{scheme_map_str}

export const DICTIONARY = {dict_json};

export const PHRASE_MAP = {phrase_json};

export const LanguageProvider = ({{ children }}) => {{
  const [currentLanguage, setCurrentLanguage] = useState(() => {{
    return localStorage.getItem('scheme_sathi_language') || 'en';
  }});

  useEffect(() => {{
    localStorage.setItem('scheme_sathi_language', currentLanguage);
  }}, [currentLanguage]);

  const setLanguage = (langCode) => {{
    setCurrentLanguage(langCode);
  }};

  const t = (keyOrPhrase, fallback) => {{
    if (!keyOrPhrase) return '';
    const textStr = String(keyOrPhrase).trim();
    if (currentLanguage === 'en') {{
      const enDict = DICTIONARY['en'];
      if (enDict && enDict[textStr]) return enDict[textStr];
      return fallback !== undefined ? fallback : textStr;
    }}

    const langDict = DICTIONARY[currentLanguage];
    const phraseMap = PHRASE_MAP[currentLanguage] || {{}};
    const lowerKey = textStr.toLowerCase();

    // 1. Direct dictionary exact key match
    if (langDict && langDict[textStr]) {{
      return langDict[textStr];
    }}

    // 2. Direct phrase map match (case-insensitive)
    if (phraseMap[lowerKey]) {{
      return phraseMap[lowerKey];
    }}

    // 3. Normalized match (strip trailing colons, question marks, asterisks, currency brackets)
    const strippedKey = textStr.replace(/[:\\?\\*\\!]+$/, '').replace(/\\s*\\(₹\\)/g, '').trim().toLowerCase();
    if (phraseMap[strippedKey]) {{
      return phraseMap[strippedKey];
    }}

    // 4. Dynamic template matchers for numbers & patterns
    // e.g. "Stage 2 of 5" -> "चरण 2 of 5"
    const stageMatch = textStr.match(/^Stage\\s+(\\d+)\\s+of\\s+(\\d+)$/i);
    if (stageMatch) {{
      const stageWord = phraseMap['stage'] || 'Stage';
      const ofWord = phraseMap['of'] || 'of';
      return `${{stageWord}} ${{stageMatch[1]}} ${{ofWord}} ${{stageMatch[2]}}`;
    }}

    // e.g. "Year 2" -> "वर्ष 2"
    const yearMatch = textStr.match(/^Year\\s+(\\d+)$/i);
    if (yearMatch) {{
      const yearWord = phraseMap['year'] || 'Year';
      return `${{yearWord}} ${{yearMatch[1]}}`;
    }}

    // e.g. "X of Y Mandatory Verified"
    const mandatoryMatch = textStr.match(/^(\\d+)\\s+of\\s+(\\d+)\\s+Mandatory Verified$/i);
    if (mandatoryMatch) {{
      const ofWord = phraseMap['of'] || 'of';
      const mandWord = phraseMap['mandatory verified'] || 'Mandatory Verified';
      return `${{mandatoryMatch[1]}} ${{ofWord}} ${{mandatoryMatch[2]}} ${{mandWord}}`;
    }}

    // e.g. "+ Test Aadhaar Card"
    const testMatch = textStr.match(/^\\+\\s*Test\\s+(.+)$/i);
    if (testMatch) {{
      const targetDoc = testMatch[1].trim();
      const translatedDoc = phraseMap[targetDoc.toLowerCase()] || targetDoc;
      const testWord = phraseMap['test'] || 'Test';
      return `+ ${{testWord}} ${{translatedDoc}}`;
    }}

    // e.g. "Upload Aadhaar Card"
    const uploadMatch = textStr.match(/^Upload\\s+(.+)$/i);
    if (uploadMatch) {{
      const targetDoc = uploadMatch[1].trim();
      const translatedDoc = phraseMap[targetDoc.toLowerCase()] || targetDoc;
      const uploadWord = phraseMap['upload'] || 'Upload';
      return `${{uploadWord}} ${{translatedDoc}}`;
    }}

    // 5. Match via English dictionary phrase lookup
    if (DICTIONARY.en && DICTIONARY.en[textStr]) {{
      const enValLower = DICTIONARY.en[textStr].toLowerCase();
      if (phraseMap[enValLower]) {{
        return phraseMap[enValLower];
      }}
      if (PHRASE_MAP.hi && PHRASE_MAP.hi[enValLower]) {{
        return PHRASE_MAP.hi[enValLower];
      }}
      return DICTIONARY.en[textStr];
    }}

    // 6. Fallback to Hindi phrase map if available
    if (PHRASE_MAP.hi && PHRASE_MAP.hi[lowerKey] && currentLanguage !== 'en') {{
      return PHRASE_MAP.hi[lowerKey];
    }}

    // 7. Default fallback
    return fallback !== undefined ? fallback : textStr;
  }};

  const translateScheme = (scheme) => {{
    if (!scheme || currentLanguage === 'en') return scheme;
    const rawCode = scheme.code || scheme.scheme_code || '';
    const normCode = rawCode.toUpperCase().replace(/[-_ ]/g, '');
    const nameStr = scheme.name || scheme.scheme_name || '';
    const normName = nameStr.toUpperCase().replace(/[-_ ]/g, '');

    let localized = SCHEME_MAP[rawCode]?.[currentLanguage] ||
                    SCHEME_MAP[normCode]?.[currentLanguage] ||
                    SCHEME_MAP[nameStr]?.[currentLanguage] ||
                    SCHEME_MAP[normName]?.[currentLanguage] ||
                    SCHEME_MAP[rawCode]?.hi ||
                    SCHEME_MAP[normCode]?.hi;

    const translatedDept = scheme.department ? t(scheme.department) : (scheme.ministry ? t(scheme.ministry) : '');
    const translatedMinistry = scheme.ministry ? t(scheme.ministry) : translatedDept;
    const translatedCat = scheme.category ? t(scheme.category) : (scheme.target_category ? t(scheme.target_category) : '');

    if (localized) {{
      return {{
        ...scheme,
        name: localized.name || scheme.name,
        scheme_name: localized.name || scheme.scheme_name,
        description: localized.desc || scheme.description,
        scheme_description: localized.desc || scheme.scheme_description,
        department: translatedDept || scheme.department,
        ministry: translatedMinistry || scheme.ministry,
        category: translatedCat || scheme.category,
        target_category: translatedCat || scheme.target_category
      }};
    }}

    return {{
      ...scheme,
      name: t(scheme.name || scheme.scheme_name),
      scheme_name: t(scheme.scheme_name || scheme.name),
      description: t(scheme.description || scheme.scheme_description),
      scheme_description: t(scheme.scheme_description || scheme.description),
      department: translatedDept || scheme.department,
      ministry: translatedMinistry || scheme.ministry,
      category: translatedCat || scheme.category,
      target_category: translatedCat || scheme.target_category
    }};
  }};

  const translateDynamic = async (text) => {{
    if (!text || currentLanguage === 'en') return text;
    try {{
      const res = await api.post('/translate', {{
        text: text,
        target_language: currentLanguage
      }});
      return res.data.translated_text || text;
    }} catch (e) {{
      return text;
    }}
  }};

  return (
    <LanguageContext.Provider value={{{{
      currentLanguage,
      language: currentLanguage,
      setLanguage,
      t,
      translateScheme,
      translateDynamic,
      languages: LANGUAGES
    }}}}>
      {{children}}
    </LanguageContext.Provider>
  );
}};

export const useLanguage = () => useContext(LanguageContext);
"""

# Write LanguageContext.jsx
with open(lang_path, 'w', encoding='utf-8') as f:
    f.write(final_js_content)

print(f"Successfully wrote LanguageContext.jsx (Size: {len(final_js_content)} bytes).")
