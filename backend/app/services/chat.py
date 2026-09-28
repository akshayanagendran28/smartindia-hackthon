# -*- coding: utf-8 -*-
"""
Scheme Sathi Intelligent Multilingual Grounded Chatbot Service
Provides 100% factual, context-aware conversational AI for Government Schemes,
Eligibility Assessment, Real-Time Application Tracking, Document Verification,
EMI Calculations, and Channel Partner Recommendations.
Supports English and 11 Regional Indian Languages:
Hindi, Tamil, Telugu, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, Assamese.
"""

import json
import re
import math
import urllib.request
from typing import Dict, Any, List, Optional
from app.config import settings

class MultilingualChatService:
    """
    Intelligent Conversational AI Assistant grounded strictly in official
    Scheme Sathi database models, user applications, document states,
    and statutory gazette parameters.
    """

    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi (हिंदी)",
        "ta": "Tamil (தமிழ்)",
        "te": "Telugu (తెలుగు)",
        "kn": "Kannada (ಕನ್ನಡ)",
        "ml": "Malayalam (മലയാളം)",
        "mr": "Marathi (मराठी)",
        "bn": "Bengali (বাংলা)",
        "gu": "Gujarati (ગુજરાતી)",
        "pa": "Punjabi (ਪੰਜਾਬੀ)",
        "or": "Odia (ଓଡ଼ିଆ)",
        "as": "Assamese (অসমীয়া)"
    }

    # Canonical 6 Mandatory Documents per Track
    CANONICAL_DOCUMENTS = {
        "EDUCATION": [
            {"key": "aadhaar", "name": "Aadhaar Card", "desc": "UIDAI Identity & Proof of Residence"},
            {"key": "pan", "name": "PAN Card", "desc": "Income Tax Financial KYC Compliance"},
            {"key": "marksheet_10th", "name": "10th Marksheet / Certificate", "desc": "Secondary School Passing & DOB Proof"},
            {"key": "marksheet_12th", "name": "12th Marksheet / Diploma", "desc": "Higher Secondary Academic Qualification"},
            {"key": "income_cert", "name": "Annual Family Income Certificate", "desc": "Revenue Authority Income Proof for 100% CSIS Subsidy (≤ ₹4.5L)"},
            {"key": "caste_cert", "name": "Community / Caste Certificate", "desc": "Competent Authority Proof for NSFDC/NBCFDC Concessional Rates"}
        ],
        "BUSINESS": [
            {"key": "aadhaar", "name": "Aadhaar Card", "desc": "UIDAI Identity & Citizenship Proof"},
            {"key": "pan", "name": "PAN Card", "desc": "Permanent Account Number for Financial Verification"},
            {"key": "project_report", "name": "Detailed Project Report (DPR)", "desc": "Techno-Economic Feasibility Report & Financial Projections"},
            {"key": "income_cert", "name": "Income Certificate / ITR", "desc": "Proof of Annual Earnings & Repayment Capacity"},
            {"key": "caste_cert", "name": "Community / Caste Certificate", "desc": "Statutory Proof for Special Category 35% PMEGP Subsidy / Stand-Up India"},
            {"key": "udyam_cert", "name": "Udyam Registration Certificate", "desc": "Official MSME Enterprise Registration under MoMSME"}
        ]
    }

    # Multilingual UI Dictionary for Core Concepts
    TRANSLATIONS = {
        "en": {
            "greeting": "Namaste! I am your AI Scheme Sathi. How can I assist you with government loan schemes, eligibility, document verification, or your application status today?",
            "no_application": "You have not submitted any scheme application yet. You can explore matching schemes and submit your application on the [Find My Scheme](/find-scheme) page.",
            "app_status_title": "Your Active Application Status",
            "no_docs_uploaded": "You have not uploaded or verified any documents yet. All 6 mandatory statutory documents are currently pending.",
            "all_docs_verified": "All 6 mandatory documents are fully verified and compliant! Your dossier is 100% ready.",
            "partial_docs": "You have verified {verified} of 6 mandatory documents.",
            "verified_badge": "VERIFIED",
            "pending_badge": "PENDING UPLOAD / VERIFICATION",
            "eligible_positive": "You are eligible for {scheme_name}!",
            "eligible_negative": "You are currently not eligible for {scheme_name}.",
            "missing_req_title": "Missing Requirements / Disqualifications",
            "matching_factors_title": "Qualifying Factors",
            "emi_formula_title": "Reducing Balance EMI Calculation Formula",
            "calc_emi_result": "For a loan of ₹{loan:,.0f} at {rate}% annual interest for {tenure} months ({years} years), your estimated monthly EMI is ₹{emi:,.0f}.",
            "partner_assigned": "Your assigned Channel Partner is **{partner_name}** ({branch}, {city}).",
            "partner_none": "No channel partner has been assigned to your application yet. You can invite a nearby partner bank from the [Channel Partner Locator](/partners).",
            "process_steps": "### Step-by-Step Scheme Sathi Application Process:\n1. **Profile Setup**: Enter your demographic and educational/business details.\n2. **AI Document Verification**: Upload 6 mandatory documents for instant OCR cross-matching.\n3. **Scheme Discovery & Ranking**: The AI Eligibility Engine calculates matching scores and subsidies.\n4. **Application Submission & Partner Invitation**: Submit your single dossier and invite your local Lead Bank.\n5. **Transparent Tracking**: Monitor bank review, sanction, and DBT subsidy release in real-time."
        },
        "hi": {
            "greeting": "नमस्ते! मैं आपका एआई स्कीम साथी हूँ। सरकारी ऋण योजनाओं, पात्रता, दस्तावेज़ सत्यापन, या आपकी आवेदन स्थिति में मैं आपकी क्या मदद कर सकता हूँ?",
            "no_application": "आपने अभी तक कोई योजना आवेदन जमा नहीं किया है। आप [Find My Scheme](/find-scheme) पृष्ठ पर पात्र योजनाओं को देखकर आवेदन कर सकते हैं।",
            "app_status_title": "आपकी सक्रिय आवेदन स्थिति",
            "no_docs_uploaded": "आपने अभी तक कोई दस्तावेज़ अपलोड या सत्यापित नहीं किया है। सभी 6 अनिवार्य दस्तावेज़ लंबित हैं।",
            "all_docs_verified": "सभी 6 अनिवार्य दस्तावेज़ पूरी तरह से सत्यापित हैं! आपका डॉसियर 100% तैयार है।",
            "partial_docs": "आपने 6 में से {verified} अनिवार्य दस्तावेज़ सत्यापित कर लिए हैं।",
            "verified_badge": "सत्यापित (VERIFIED)",
            "pending_badge": "लंबित (PENDING)",
            "eligible_positive": "आप {scheme_name} के लिए पात्र हैं!",
            "eligible_negative": "आप वर्तमान में {scheme_name} के लिए पात्र नहीं हैं।",
            "missing_req_title": "अपूर्ण आवश्यकताएं / कारण",
            "matching_factors_title": "पात्रता के मुख्य बिंदु",
            "emi_formula_title": "घटते शेष पर ईएमआई गणना सूत्र",
            "calc_emi_result": "₹{loan:,.0f} के ऋण पर {rate}% वार्षिक ब्याज दर से {tenure} महीनों ({years} वर्ष) के लिए अनुमानित मासिक ईएमआई ₹{emi:,.0f} है।",
            "partner_assigned": "आपके अधिकृत चैनल पार्टनर **{partner_name}** ({branch}, {city}) हैं।",
            "partner_none": "आपके आवेदन के लिए अभी तक कोई चैनल पार्टनर नियुक्त नहीं किया गया है। आप [Channel Partner Locator](/partners) से बैंक को आमंत्रित कर सकते हैं।",
            "process_steps": "### स्कीम साथी आवेदन प्रक्रिया:\n1. **प्रोफाइल पूर्ण करें**: अपनी व्यक्तिगत और व्यवसाय/शिक्षा संबंधी जानकारी दर्ज करें।\n2. **दस्तावेज़ सत्यापन**: AI OCR द्वारा 6 अनिवार्य दस्तावेज़ों का सत्यापन करें।\n3. **योजना चयन**: अपनी पात्रता और अधिकतम सब्सिडी वाली योजना का चयन करें।\n4. **आवेदन व बैंक आमंत्रण**: आवेदन जमा करें और अपने नजदीकी चैनल पार्टनर बैंक को आमंत्रित करें।\n5. **रीयल-टाइम ट्रैकिंग**: ऋण स्वीकृति और डीबीटी सब्सिडी की स्थिति को ट्रैक करें।"
        },
        "ta": {
            "greeting": "வணக்கம்! நான் உங்கள் ஏஐ திட்டம் சாதி. அரசு கடன் திட்டங்கள், தகுதி, ஆவண சரிபார்ப்பு அல்லது உங்கள் விண்ணப்ப நிலை குறித்து உங்களுக்கு எவ்வாறு உதவ முடியும்?",
            "no_application": "நீங்கள் இதுவரை எந்த திட்டத்திற்கும் விண்ணப்பிக்கவில்லை. [Find My Scheme](/find-scheme) பக்கத்தில் தகுதியான திட்டங்களை கண்டறிந்து விண்ணப்பிக்கலாம்.",
            "app_status_title": "உங்கள் தற்போதைய விண்ணப்ப நிலை",
            "no_docs_uploaded": "நீங்கள் இன்னும் எந்த ஆவணங்களையும் பதிவேற்றவில்லை. அனைத்து 6 கட்டாய ஆவணங்களும் நிலுவையில் உள்ளன.",
            "all_docs_verified": "அனைத்து 6 கட்டாய ஆவணங்களும் வெற்றிகரமாக சரிபார்க்கப்பட்டுவிட்டன!",
            "partial_docs": "6 கட்டாய ஆவணங்களில் {verified} ஆவணங்களை சரிபார்த்துள்ளீர்கள்.",
            "verified_badge": "சரிபார்க்கப்பட்டது",
            "pending_badge": "நிலுவையில் உள்ளது",
            "eligible_positive": "நீங்கள் {scheme_name} திட்டத்திற்கு தகுதியுடையவர்!",
            "eligible_negative": "தற்போது நீங்கள் {scheme_name} திட்டத்திற்கு தகுதியற்றவர்.",
            "missing_req_title": "பூர்த்தி செய்யப்படாத தேவைகள்",
            "matching_factors_title": "தகுதி அம்சங்கள்",
            "emi_formula_title": "இஎம்ஐ (EMI) கணக்கீட்டு முறை",
            "calc_emi_result": "₹{loan:,.0f} கடனுக்கு {rate}% வட்டியில் {tenure} மாதங்களுக்கு ({years} ஆண்டுகள்) மாதத் தவணை ₹{emi:,.0f} ஆகும்.",
            "partner_assigned": "உங்களின் நியமிக்கப்பட்ட வங்கி கூட்டாளர்: **{partner_name}** ({branch}, {city}).",
            "partner_none": "இன்னும் வங்கி கூட்டாளர் இணைக்கப்படவில்லை. [Channel Partner Locator](/partners) பக்கத்தில் வங்கியை அழைக்கலாம்.",
            "process_steps": "### திட்டம் சாதி விண்ணப்ப படிகள்:\n1. விவரங்களை பதிவு செய்தல்\n2. 6 கட்டாய ஆவணங்களை AI மூலம் சரிபார்த்தல்\n3. பொருத்தமான அரசு திட்டத்தை தேர்வு செய்தல்\n4. விண்ணப்பத்தை சமர்ப்பித்து வங்கி கூட்டாளரை அழைத்தல்\n5. கடன் ஒப்புதல் நிலையை நேரலையாக கண்காணித்தல்."
        },
        "te": {
            "greeting": "నమస్కారం! నేను మీ ఏఐ స్కీమ్ సాథిని. ప్రభుత్వ రుణ పథకాలు, అర్హత, ధృవీకరణ పత్రాలు మరియు మీ దరఖాస్తు స్థితికి సంబంధించిన సమాచారం కోసం నేను సహాయం చేయగలను.",
            "no_application": "మీరు ఇంకా ఎలాంటి పథకానికి దరఖాస్తు చేసుకోలేదు. [Find My Scheme](/find-scheme) పేజీలో అర్హత గల పథకాలను ఎంచుకోండి.",
            "app_status_title": "మీ దరఖాస్తు స్థితి",
            "no_docs_uploaded": "మీరు ఇంకా ఎలాంటి పత్రాలను అప్‌లోడ్ చేయలేదు. 6 తప్పనిసరి పత్రాలు పెండింగ్‌లో ఉన్నాయి.",
            "all_docs_verified": "అన్ని 6 తప్పనిసరి పత్రాలు విజయవంతంగా ధృవీకరించబడ్డాయి!",
            "partial_docs": "మీరు 6 పత్రాలలో {verified} పత్రాలను ధృవీకరించారు.",
            "verified_badge": "ధృవీకరించబడింది",
            "pending_badge": "పెండింగ్‌లో ఉంది",
            "eligible_positive": "మీరు {scheme_name} పథకానికి అర్హులు!",
            "eligible_negative": "మీరు ప్రస్తుతం {scheme_name} పథకానికి అర్హులు కారు.",
            "missing_req_title": "లోపించిన అర్హతలు",
            "matching_factors_title": "అర్హత కారణాలు",
            "emi_formula_title": "ఈఎంఐ (EMI) లెక్కింపు పద్ధతి",
            "calc_emi_result": "₹{loan:,.0f} రుణానికి {rate}% వార్షిక వడ్డీతో {tenure} నెలలకు నెలవారీ ఈఎంఐ ₹{emi:,.0f}.",
            "partner_assigned": "మీకు కేటాయించిన ఛానల్ పార్టనర్: **{partner_name}** ({branch}, {city}).",
            "partner_none": "ఛానల్ పార్టనర్ ఇంకా కేటాయించబడలేదు. [Channel Partner Locator](/partners) నుండి బ్యాంకును ఆహ్వానించండి.",
            "process_steps": "### దరఖాస్తు ప్రక్రియ:\n1. ప్రొఫైల్ వివరాలు నింపండి\n2. 6 పత్రాలను AI ద్వారా ధృవీకరించండి\n3. పథకాన్ని ఎంచుకోండి\n4. దరఖాస్తు సమర్పించి బ్యాంకును ఆహ్వానించండి\n5. స్థితిని ట్రాక్ చేయండి."
        },
        "kn": {
            "greeting": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಎಐ ಸ್ಕೀಮ್ ಸಾಥಿ. ಸರ್ಕಾರಿ ಸಾಲ ಯೋಜನೆಗಳು, ಅರ್ಹತೆ, ದಾಖಲೆ ಪರಿಶೀಲನೆ ಮತ್ತು ನಿಮ್ಮ ಅರ್ಜಿ ಸ್ಥಿತಿಯ ಕುರಿತು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ.",
            "no_application": "ನೀವು ಇನ್ನೂ ಯಾವುದೇ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿಲ್ಲ. [Find My Scheme](/find-scheme) ಪುಟದಲ್ಲಿ ಯೋಜನೆಗಳನ್ನು ನೋಡಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            "app_status_title": "ನಿಮ್ಮ ಅರ್ಜಿ ಸ್ಥಿತಿ",
            "no_docs_uploaded": "ನೀವು ಇನ್ನೂ ಯಾವುದೇ ದಾಖಲೆಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿಲ್ಲ. 6 ಕಡ್ಡಾಯ ದಾಖಲೆಗಳು ಬಾಕಿ ಇವೆ.",
            "all_docs_verified": "ಎಲ್ಲಾ 6 ಕಡ್ಡಾಯ ದಾಖಲೆಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಪರಿಶೀಲಿಸಲಾಗಿದೆ!",
            "partial_docs": "ನೀವು 6 ರಲ್ಲಿ {verified} ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿದ್ದೀರಿ.",
            "verified_badge": "ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
            "pending_badge": "ಬಾಕಿ ಇದೆ",
            "eligible_positive": "ನೀವು {scheme_name} ಯೋಜನೆಗೆ ಅರ್ಹರಾಗಿದ್ದೀರಿ!",
            "eligible_negative": "ನೀವು ಪ್ರಸ್ತುತ {scheme_name} ಯೋಜನೆಗೆ ಅರ್ಹರಲ್ಲ.",
            "missing_req_title": "ಅಪೂರ್ಣ ಅರ್ಹತೆಗಳು",
            "matching_factors_title": "ಅರ್ಹತೆಯ ಅಂಶಗಳು",
            "emi_formula_title": "ಇಎಂಐ (EMI) ಲೆಕ್ಕಾಚಾರ ಸೂತ್ರ",
            "calc_emi_result": "₹{loan:,.0f} ಸಾಲಕ್ಕೆ {rate}% ಬಡ್ಡಿದರದಲ್ಲಿ {tenure} ತಿಂಗಳುಗಳಿಗೆ ಅಂದಾಜು ಮಾಸಿಕ ಇಎಂಐ ₹{emi:,.0f}.",
            "partner_assigned": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಪಾಲುದಾರರು: **{partner_name}** ({branch}, {city}).",
            "partner_none": "ಇನ್ನೂ ಪಾಲುದಾರ ಬ್ಯಾಂಕ್ ನಿಯೋಜಿಸಿಲ್ಲ. [Channel Partner Locator](/partners) ಬಳಸಿ.",
            "process_steps": "### ಅರ್ಜಿ ಸಲ್ಲಿಕೆ ಹಂತಗಳು:\n1. ಪ್ರೊಫೈಲ್ ಭರ್ತಿ ಮಾಡಿ\n2. 6 ದಾಖಲೆಗಳನ್ನು AI ಮೂಲಕ ಪರಿಶೀಲಿಸಿ\n3. ಯೋಜನೆ ಆಯ್ಕೆಮಾಡಿ\n4. ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ಬ್ಯಾಂಕ್ ಆಹ್ವಾನಿಸಿ\n5. ಲೈವ್ ಟ್ರ್ಯಾಕ್ ಮಾಡಿ."
        },
        "ml": {
            "greeting": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ സ്കീം സാഥി അസിസ്റ്റന്റാണ്. സർക്കാർ വായ്പാ പദ്ധതികൾ, യോഗ്യത, രേഖാ പരിശോധന, അപേക്ഷാ സ്ഥിതി എന്നിവയിൽ സഹായിക്കാം.",
            "no_application": "നിങ്ങൾ ഇതുവരെ അപേക്ഷ സമർപ്പിച്ചിട്ടില്ല. [Find My Scheme](/find-scheme) പേജിൽ അനുയോജ്യമായ പദ്ധതികൾ കണ്ടെത്തുക.",
            "app_status_title": "നിങ്ങളുടെ അപേക്ഷാ സ്ഥിതി",
            "no_docs_uploaded": "താങ്കൾ ഇതുവരെ രേഖകൾ ഒന്നും അപ്‌ലോഡ് ചെയ്തിട്ടില്ല. 6 നിർബന്ധിത രേഖകൾ ബാക്കിയാണ്.",
            "all_docs_verified": "എല്ലാ 6 നിർബന്ധിത രേഖകളും വിജയകരമായി പരിശോധിച്ചു!",
            "partial_docs": "6 നിർബന്ധിത രേഖകളിൽ {verified} എണ്ണം പരിശോധിച്ചു.",
            "verified_badge": "പരിശോധിച്ചു",
            "pending_badge": "ബാക്കിയാണ്",
            "eligible_positive": "താങ്കൾ {scheme_name} പദ്ധതിക്ക് അർഹനാണ്!",
            "eligible_negative": "താങ്കൾ നിലവിൽ {scheme_name} പദ്ധതിക്ക് അർഹനല്ല.",
            "missing_req_title": "പൂർത്തിയാകാത്ത നിബന്ധനകൾ",
            "matching_factors_title": "യോഗ്യതാ ഘടകങ്ങൾ",
            "emi_formula_title": "ഇഎംഐ കണക്കുകൂട്ടൽ രീതി",
            "calc_emi_result": "₹{loan:,.0f} വായ്പയ്ക്ക് {rate}% പലിശ നിരക്കിൽ {tenure} മാസത്തേക്ക് പ്രതിമാസ ഇഎംഐ ₹{emi:,.0f}.",
            "partner_assigned": "നിങ്ങളുടെ ചാനൽ പാർട്ണർ: **{partner_name}** ({branch}, {city}).",
            "partner_none": "പാർട്ണറെ നിയോഗിച്ചിട്ടില്ല. [Channel Partner Locator](/partners) സന്ദർശിക്കുക.",
            "process_steps": "### അപേക്ഷാ ഘട്ടങ്ങൾ:\n1. പ്രൊഫൈൽ പൂർത്തിയാക്കുക\n2. 6 രേഖകൾ പരിശോധിക്കുക\n3. പദ്ധതി തിരഞ്ഞെടുക്കുക\n4. അപേക്ഷ സമർപ്പിക്കുക\n5. തത്സമയം ട്രാക്ക് ചെയ്യുക."
        },
        "mr": {
            "greeting": "नमस्कार! मी तुमचा एआय स्कीम साथी आहे. शासकीय कर्ज योजना, पात्रता, कागदपत्र पडताळणी किंवा अर्जाच्या स्थितीबद्दल मी तुम्हाला मदत करू शकेन.",
            "no_application": "तुम्ही अद्याप कोणत्याही योजनेसाठी अर्ज केलेला नाही. [Find My Scheme](/find-scheme) पृष्ठावर जाऊन पात्र योजना तपासा.",
            "app_status_title": "तुमच्या अर्जाची स्थिती",
            "no_docs_uploaded": "तुम्ही अद्याप कोणतीही कागदपत्रे अपलोड केलेली नाहीत. सर्व 6 अनिवार्य कागदपत्रे प्रलंबित आहेत.",
            "all_docs_verified": "सर्व 6 अनिवार्य कागदपत्रे यशस्वीरित्या पडताळली गेली आहेत!",
            "partial_docs": "तुम्ही 6 पैकी {verified} कागदपत्रे पडताळली आहेत.",
            "verified_badge": "पडताळणी पूर्ण",
            "pending_badge": "प्रलंबित",
            "eligible_positive": "तुम्ही {scheme_name} योजनेसाठी पात्र आहात!",
            "eligible_negative": "तुम्ही सध्या {scheme_name} योजनेसाठी पात्र नाही आहात.",
            "missing_req_title": "अपूर्ण अटी व कारणे",
            "matching_factors_title": "पात्रतेचे निकष",
            "emi_formula_title": "ईएमआय (EMI) गणना सूत्र",
            "calc_emi_result": "₹{loan:,.0f} कर्जासाठी {rate}% वार्षिक व्याजाने {tenure} महिन्यांसाठी अंदाजे मासिक ईएमआय ₹{emi:,.0f} आहे.",
            "partner_assigned": "तुमचे चॅनेल पार्टनर: **{partner_name}** ({branch}, {city}).",
            "partner_none": "अद्याप चॅनेल पार्टनर नियुक्त केलेला नाही. [Channel Partner Locator](/partners) वापरा.",
            "process_steps": "### अर्ज प्रक्रिया:\n1. प्रोफाइल पूर्ण करा\n2. AI द्वारे 6 कागदपत्रे तपासा\n3. योजना निवडा\n4. अर्ज सादर करा\n5. स्थिती ट्रॅक करा."
        },
        "bn": {
            "greeting": "নমস্কার! আমি আপনার এআই স্কিম সাথি। সরকারি ঋণ প্রকল্প, যোগ্যতা, নথি যাচাইকরণ বা আপনার আবেদনের স্থিতি জানতে আমি সাহায্য করতে পারি।",
            "no_application": "আপনি এখনও কোনো প্রকল্পে আবেদন করেননি। [Find My Scheme](/find-scheme) পেজে গিয়ে যোগ্য প্রকল্প দেখে আবেদন করুন।",
            "app_status_title": "আপনার আবেদনের স্থিতি",
            "no_docs_uploaded": "আপনি এখনও কোনো নথি আপলোড বা যাচাই করেননি। ৬টি বাধ্যতামূলক নথি বাকি রয়েছে।",
            "all_docs_verified": "সমস্ত ৬টি বাধ্যতামূলক নথি সফলভাবে যাচাই করা হয়েছে!",
            "partial_docs": "আপনি ৬টি নথির মধ্যে {verified}টি যাচাই করেছেন।",
            "verified_badge": "যাচাইকৃত",
            "pending_badge": "বাকি আছে",
            "eligible_positive": "আপনি {scheme_name} প্রকল্পের জন্য যোগ্য!",
            "eligible_negative": "আপনি বর্তমানে {scheme_name} প্রকল্পের জন্য যোগ্য নন।",
            "missing_req_title": "অনুপস্থিত প্রয়োজনীয়তা",
            "matching_factors_title": "যোগ্যতার কারণসমূহ",
            "emi_formula_title": "ইএমআই (EMI) গণনার সূত্র",
            "calc_emi_result": "₹{loan:,.0f} ঋণের জন্য {rate}% বার্ষিক সুদে {tenure} মাসের জন্য আনুমানিক মাসিক ইএমআই ₹{emi:,.0f}।",
            "partner_assigned": "আপনার চ্যানেল পার্টনার: **{partner_name}** ({branch}, {city})।",
            "partner_none": "এখনও পার্টনার নিযুক্ত হয়নি। [Channel Partner Locator](/partners) দেখুন।",
            "process_steps": "### আবেদন প্রক্রিয়া:\n1. প্রোফাইল সম্পন্ন করুন\n2. ৬টি নথি যাচাই করুন\n3. স্কিম নির্বাচন করুন\n4. আবেদন জমা দিন ও ব্যাংককে আমন্ত্রণ জানান\n5. স্ট্যাটাস ট্র্যাক করুন।"
        },
        "gu": {
            "greeting": "નમસ્તે! હું તમારો એઆઈ સ્કીમ સાથી છું. સરકારી યોજનાઓ, પાત્રતા, દસ્તાવેજ ચકાસણી અથવા તમારી અરજીની સ્થિતિ અંગે હું મદદ કરી શકું છું.",
            "no_application": "તમે હજુ સુધી કોઈ યોજના માટે અરજી કરી નથી. [Find My Scheme](/find-scheme) પૃષ્ઠ પર યોજનાઓ જોઈ અરજી કરો.",
            "app_status_title": "તમારી અરજીની સ્થિતિ",
            "no_docs_uploaded": "તમે હજુ સુધી કોઈ દસ્તાવેજ અપલોડ કર્યા નથી. તમામ 6 ફરજિયાત દસ્તાવેજો બાકી છે.",
            "all_docs_verified": "તમામ 6 ફરજિયાત દસ્તાવેજો ચકાસાઈ ગયા છે!",
            "partial_docs": "તમે 6 માંથી {verified} દસ્તાવેજો ચકાસ્યા છે.",
            "verified_badge": "ચકાસાયેલ",
            "pending_badge": "બાકી છે",
            "eligible_positive": "તમે {scheme_name} યોજના માટે પાત્ર છો!",
            "eligible_negative": "તમે હાલમાં {scheme_name} યોજના માટે પાત્ર નથી.",
            "missing_req_title": "અપૂર્ણ શરતો",
            "matching_factors_title": "પાત્રતાના કારણો",
            "emi_formula_title": "ઇએમઆઇ (EMI) ગણતરી પદ્ધતિ",
            "calc_emi_result": "₹{loan:,.0f} ની લોન પર {rate}% વાર્ષિક વ્યાજે {tenure} મહિના માટે અંદાજિત માસિક EMI ₹{emi:,.0f} થશે.",
            "partner_assigned": "તમારા ચેનલ પાર્ટનર: **{partner_name}** ({branch}, {city}).",
            "partner_none": "હજુ પાર્ટનર ફાળવાયા નથી. [Channel Partner Locator](/partners) જુઓ.",
            "process_steps": "### અરજી પ્રક્રિયા:\n1. પ્રોફાઇલ પૂર્ણ કરો\n2. 6 દસ્તાવેજો ચકાસો\n3. યોજના પસંદ કરો\n4. અરજી સબમિટ કરો\n5. સ્થિતિ ટ્રેક કરો."
        },
        "pa": {
            "greeting": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਏਆਈ ਸਕੀਮ ਸਾਥੀ ਹਾਂ। ਸਰਕਾਰੀ ਕਰਜ਼ਾ ਯੋਜਨਾਵਾਂ, ਯੋਗਤਾ, ਦਸਤਾਵੇਜ਼ ਤਸਦੀਕ ਜਾਂ ਤੁਹਾਡੀ ਅਰਜ਼ੀ ਦੀ ਸਥਿਤੀ ਬਾਰੇ ਮੈਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ।",
            "no_application": "ਤੁਸੀਂ ਅਜੇ ਕਿਸੇ ਯੋਜਨਾ ਲਈ ਅਰਜ਼ੀ ਨਹੀਂ ਦਿੱਤੀ ਹੈ। [Find My Scheme](/find-scheme) 'ਤੇ ਜਾ ਕੇ ਅਰਜ਼ੀ ਦਿਓ।",
            "app_status_title": "ਤੁਹਾਡੀ ਅਰਜ਼ੀ ਦੀ ਸਥਿਤੀ",
            "no_docs_uploaded": "ਤੁਸੀਂ ਅਜੇ ਤੱਕ ਕੋਈ ਦਸਤਾਵੇਜ਼ ਅੱਪਲੋਡ ਨਹੀਂ ਕੀਤੇ ਹਨ। ਸਾਰੇ 6 ਲਾਜ਼ਮੀ ਦਸਤਾਵੇਜ਼ ਬਕਾਇਆ ਹਨ।",
            "all_docs_verified": "ਸਾਰੇ 6 ਲਾਜ਼ਮੀ ਦਸਤਾਵੇਜ਼ ਪੂਰੀ ਤਰ੍ਹਾਂ ਤਸਦੀਕ ਹੋ ਚੁੱਕੇ ਹਨ!",
            "partial_docs": "ਤੁਸੀਂ 6 ਵਿੱਚੋਂ {verified} ਦਸਤਾਵੇਜ਼ ਤਸਦੀਕ ਕੀਤੇ ਹਨ।",
            "verified_badge": "ਤਸਦੀਕਸ਼ੁਦਾ",
            "pending_badge": "ਬਕਾਇਆ",
            "eligible_positive": "ਤੁਸੀਂ {scheme_name} ਯੋਜਨਾ ਲਈ ਯੋਗ ਹੋ!",
            "eligible_negative": "ਤੁਸੀਂ ਫਿਲਹਾਲ {scheme_name} ਯੋਜਨਾ ਲਈ ਯੋਗ ਨਹੀਂ ਹੋ।",
            "missing_req_title": "ਅਧੂਰੀਆਂ ਲੋੜਾਂ",
            "matching_factors_title": "ਯੋਗਤਾ ਦੇ ਕਾਰਨ",
            "emi_formula_title": "ਈਐਮਆਈ (EMI) ਗਣਨਾ ਦਾ ਫਾਰਮੂਲਾ",
            "calc_emi_result": "₹{loan:,.0f} ਦੇ ਕਰਜ਼ੇ 'ਤੇ {rate}% ਵਿਆਜ ਨਾਲ {tenure} ਮਹੀਨਿਆਂ ਲਈ ਮਹੀਨਾਵਾਰ ਕਿਸ਼ਤ ₹{emi:,.0f} ਹੈ।",
            "partner_assigned": "ਤੁਹਾਡੇ ਚੈਨਲ ਪਾਰਟਨਰ: **{partner_name}** ({branch}, {city})।",
            "partner_none": "ਅਜੇ ਕੋਈ ਪਾਰਟਨਰ ਨਿਯੁਕਤ ਨਹੀਂ ਕੀਤਾ ਗਿਆ। [Channel Partner Locator](/partners) ਦੇਖੋ।",
            "process_steps": "### ਅਰਜ਼ੀ ਦੇ ਪੜਾਅ:\n1. ਪ੍ਰੋਫਾਈਲ ਭਰੋ\n2. 6 ਦਸਤਾਵੇਜ਼ ਤਸਦੀਕ ਕਰੋ\n3. ਯੋਜਨਾ ਚੁਣੋ\n4. ਅਰਜ਼ੀ ਜਮ੍ਹਾਂ ਕਰੋ\n5. ਸਥਿਤੀ ਟਰੈਕ ਕਰੋ।"
        },
        "or": {
            "greeting": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ AI ସ୍କିମ ସାଥି। ସରକାରୀ ଋଣ ଯୋଜନା, ଯୋଗ୍ୟତା, ଦସ୍ତାବିଜ ଯାଞ୍ଚ କିମ୍ବା ଆପଣଙ୍କ ଆବେଦନ ସ୍ଥିତି ବିଷୟରେ ମୁଁ ସାହାଯ୍ୟ କରିପାରିବି।",
            "no_application": "ଆପଣ ଏପର୍ଯ୍ୟନ୍ତ କୌଣସି ଯୋଜନା ପାଇଁ ଆବେଦନ କରିନାହାଁନ୍ତି। [Find My Scheme](/find-scheme) ପୃଷ୍ଠାରେ ଯୋଜନା ଦେଖି ଆବେଦନ କରନ୍ତୁ।",
            "app_status_title": "ଆପଣଙ୍କ ଆବେଦନ ସ୍ଥିତି",
            "no_docs_uploaded": "ଆପଣ ଏପର୍ଯ୍ୟନ୍ତ କୌଣସି ଦସ୍ତାବିଜ ଅପଲୋଡ୍ କରିନାହାଁନ୍ତି। ସମସ୍ତ ୬ଟି ବାଧ୍ୟତାମୂଳକ ଦସ୍ତାବିଜ ବାକି ଅଛି।",
            "all_docs_verified": "ସମସ୍ତ ୬ଟି ବାଧ୍ୟତାମୂଳକ ଦସ୍ତାବିଜ ସଫଳତାର ସହ ଯାଞ୍ଚ ହୋଇସାରିଛି!",
            "partial_docs": "ଆପଣ ୬ଟି ମଧ୍ୟରୁ {verified}ଟି ଦସ୍ତାବିଜ ଯାଞ୍ଚ କରିଛନ୍ତି।",
            "verified_badge": "ଯାଞ୍ଚ ହୋଇଛି",
            "pending_badge": "ବାକି ଅଛି",
            "eligible_positive": "ଆପଣ {scheme_name} ଯୋଜନା ପାଇଁ ଯୋଗ୍ୟ!",
            "eligible_negative": "ଆପଣ ବର୍ତ୍ତମାନ {scheme_name} ଯୋଜନା ପାଇଁ ଯୋଗ୍ୟ ନୁହଁନ୍ତି।",
            "missing_req_title": "ଅସମ୍ପୂର୍ଣ୍ଣ ଆବଶ୍ୟକତା",
            "matching_factors_title": "ଯୋଗ୍ୟତାର ମୁଖ୍ୟ କାରଣ",
            "emi_formula_title": "EMI ଗଣନା ପଦ୍ଧତି",
            "calc_emi_result": "₹{loan:,.0f} ଋଣ ପାଇଁ {rate}% ବାର୍ଷିକ ସୁଧରେ {tenure} ମାସ ପାଇଁ ମାସିକ କିସ୍ତି ₹{emi:,.0f} ହେବ।",
            "partner_assigned": "ଆପଣଙ୍କ ଚ୍ୟାନେଲ ପାର୍ଟନର: **{partner_name}** ({branch}, {city})।",
            "partner_none": "ଏପର୍ଯ୍ୟନ୍ତ ପାର୍ଟନର ନିଯୁକ୍ତ ହୋଇନାହାଁନ୍ତି। [Channel Partner Locator](/partners) ବ୍ୟବହାର କରନ୍ତୁ।",
            "process_steps": "### ଆବେଦନ ପ୍ରକ୍ରିୟା:\n1. ପ୍ରୋଫାଇଲ୍ ସମ୍ପୂର୍ଣ୍ଣ କରନ୍ତୁ\n2. ୬ଟି ଦସ୍ତାବିଜ ଯାଞ୍ଚ କରନ୍ତୁ\n3. ଯୋଜନା ଚୟନ କରନ୍ତୁ\n4. ଆବେଦନ ଦାଖଲ କରନ୍ତୁ\n5. ଷ୍ଟାଟସ୍ ଟ୍ରାକ୍ କରନ୍ତୁ।"
        },
        "as": {
            "greeting": "নমস্কাৰ! মই আপোনাৰ AI আঁচনি সাথি। চৰকাৰী ঋণ আঁচনি, যোগ্যতা, নথি পৰীক্ষণ বা আবেদনৰ স্থিতি সম্পৰ্কে মই সহায় কৰিব পাৰো।",
            "no_application": "আপুনি এতিয়ালৈকে কোনো আঁচনিৰ বাবে আবেদন কৰা নাই। [Find My Scheme](/find-scheme) ত গৈ উপযুক্ত আঁচনি চাওক।",
            "app_status_title": "আপোনাৰ আবেদনৰ স্থিতি",
            "no_docs_uploaded": "আপুনি এতিয়ালৈকে কোনো নথি আপলোড কৰা নাই। সকলো ৬টা বাধ্যতামূলক নথি বাকী আছে।",
            "all_docs_verified": "সকলো ৬টা বাধ্যতামূলক নথি সফলতাৰে পৰীক্ষা কৰা হৈছে!",
            "partial_docs": "আপুনি ৬টাৰ ভিতৰত {verified}টা নথি পৰীক্ষা কৰিছে।",
            "verified_badge": "পৰীক্ষিত",
            "pending_badge": "বাকী আছে",
            "eligible_positive": "আপুনি {scheme_name} আঁচনিৰ বাবে যোগ্য!",
            "eligible_negative": "আপুনি বৰ্তমান {scheme_name} আঁচনিৰ বাবে যোগ্য নহয়।",
            "missing_req_title": "অসম্পূৰ্ণ যোগ্যতাসমূহ",
            "matching_factors_title": "যোগ্যতাৰ কাৰণসমূহ",
            "emi_formula_title": "ইএমআই (EMI) গণনা পদ্ধতি",
            "calc_emi_result": "₹{loan:,.0f} ঋণৰ বাবে {rate}% সুতত {tenure} মাহৰ বাবে আনুমানিক মাহেকীয়া কিস্তি ₹{emi:,.0f}।",
            "partner_assigned": "আপোনাৰ চেনেল পাৰ্টনাৰ: **{partner_name}** ({branch}, {city})।",
            "partner_none": "এতিয়ালৈকে পাৰ্টনাৰ সংযোগ কৰা হোৱা নাই। [Channel Partner Locator](/partners) চাওক।",
            "process_steps": "### আবেদন প্রক্রিয়া:\n1. প্ৰফাইল সম্পূৰ্ণ কৰক\n2. ৬টা নথি পৰীক্ষা কৰক\n3. আঁচনি বাছনি কৰক\n4. আবেদন জমা দি বেংকক আমন্ত্রণ জনাওক\n5. স্থিতি ট্র্যাক কৰক।"
        }
    }

    @classmethod
    def get_translation(cls, key: str, lang: str = "en", **kwargs) -> str:
        """Fetch localized template and format with kwargs."""
        lang_dict = cls.TRANSLATIONS.get(lang, cls.TRANSLATIONS["en"])
        template = lang_dict.get(key, cls.TRANSLATIONS["en"].get(key, ""))
        try:
            return template.format(**kwargs)
        except Exception:
            return template

    @classmethod
    def _calculate_emi(cls, principal: float, annual_rate: float, tenure_months: int) -> float:
        """Standard reducing balance EMI formula."""
        if principal <= 0 or tenure_months <= 0:
            return 0.0
        if annual_rate <= 0:
            return principal / tenure_months
        monthly_rate = (annual_rate / 12.0) / 100.0
        try:
            factor = math.pow(1 + monthly_rate, tenure_months)
            emi = (principal * monthly_rate * factor) / (factor - 1)
            return round(emi, 2)
        except Exception:
            return round(principal / tenure_months, 2)

    @classmethod
    def _get_scheme_field(cls, scheme: Any, field: str, default: Any = "") -> Any:
        """Safely extract field from Scheme ORM model or dict."""
        if isinstance(scheme, dict):
            return scheme.get(field, default)
        return getattr(scheme, field, default)

    @classmethod
    def _find_target_scheme(
        cls, 
        message: str, 
        schemes_db: List[Any], 
        context_scheme_code: Optional[str] = None,
        context_scheme_id: Optional[Any] = None
    ) -> Optional[Any]:
        """Find specifically referenced scheme from context or natural language query."""
        if context_scheme_id:
            for s in schemes_db:
                if str(cls._get_scheme_field(s, "id")) == str(context_scheme_id):
                    return s
        if context_scheme_code:
            for s in schemes_db:
                if (cls._get_scheme_field(s, "code") or "").upper() == context_scheme_code.upper():
                    return s

        msg_lower = message.lower()
        
        # Keyword mapping for common schemes
        aliases = {
            "pmegp": "PMEGP",
            "prime minister employment": "PMEGP",
            "svanidhi": "PM_SVANIDHI",
            "street vendor": "PM_SVANIDHI",
            "stand up": "STAND_UP_INDIA",
            "standup": "STAND_UP_INDIA",
            "mudra": "MUDRA_SHISHU",
            "shishu": "MUDRA_SHISHU",
            "kishore": "MUDRA_KISHORE",
            "csis": "CSIS",
            "central sector interest": "CSIS",
            "higher education loan": "CSIS",
            "nsfdc": "NSFDC-EDU",
            "scheduled caste education": "NSFDC-EDU",
            "nbcfdc": "NBCFDC-EDU",
            "nmdfc": "NMDFC-EDU",
            "ambedkar": "AMBEDKAR-EDU",
            "overseas": "AMBEDKAR-EDU",
            "cgfsel": "CGFSEL",
            "vishwakarma": "PM_VISHWAKARMA",
            "artisan": "PM_VISHWAKARMA",
            "mahila samridhi": "MAHILA_SAMRIDHI"
        }

        for alias, code in aliases.items():
            if alias in msg_lower:
                for s in schemes_db:
                    s_code = (cls._get_scheme_field(s, "code") or "").upper()
                    if s_code == code or s_code == code.replace("-", "_") or s_code == code.replace("_", "-"):
                        return s

        for s in schemes_db:
            s_name = (cls._get_scheme_field(s, "name") or cls._get_scheme_field(s, "scheme_name") or "").lower()
            s_code = (cls._get_scheme_field(s, "code") or "").lower()
            if s_code and s_code in msg_lower:
                return s
            name_words = [w for w in s_name.split() if len(w) > 3 and w not in ["scheme", "loan", "yojana", "pradhan", "mantri", "national"]]
            if any(w in msg_lower for w in name_words):
                return s

        return None

    @classmethod
    def _detect_intent(cls, message: str) -> str:
        """Classify user natural language query into high-level intent categories."""
        m = message.lower().strip()

        # 1. Greetings
        if any(w in m for w in ["hi", "hello", "namaste", "vanakkam", "namaskara", "nomoshkar", "kem cho", "sat sri akal", "nomoskar", "hey"]):
            if len(m.split()) <= 4:
                return "greeting"

        # 2. Application Status & Loan Status
        if any(w in m for w in ["application status", "my application", "check application", "loan status", "fund status", "has my application been approved", "is my loan approved", "status of my application", "track my application", "application number", "आवेदन स्थिति", "விண்ணப்ப நிலை", "దరఖాస్తు స్థితి"]):
            return "application_status"

        # 3. Which scheme am I applying for
        if any(w in m for w in ["which scheme am i applying", "what scheme am i applying", "which scheme did i choose", "my selected scheme", "active scheme", "which scheme i applied"]):
            return "application_which_scheme"

        # 4. Documents Verified / Pending Status for Current User
        if any(w in m for w in ["have my documents been verified", "are my documents verified", "are my documents complete", "what documents are pending", "which documents are still pending", "which documents are pending", "pending documents", "documents verified", "verified documents"]):
            return "user_documents_status"

        # 5. Document Rejection / Mismatch / Why Rejected
        if any(w in m for w in ["why was my document rejected", "document rejected", "mismatch", "ocr failed", "verification failed", "rejection reason"]):
            return "document_rejection_reason"

        # 6. How to verify / Upload documents
        if any(w in m for w in ["how do i verify my documents", "how to verify", "how to upload", "document assistant", "upload marksheet", "upload aadhaar"]):
            return "document_how_to_verify"

        # 7. Document Requirements (General / Scheme-specific)
        if any(w in m for w in ["what documents are required", "documents required", "documents needed", "what documents do i need", "checklist", "mandatory documents", "दस्तावेज़", "ஆவணங்கள்", "పత్రాలు", "ದಾಖಲೆಗಳು", "രേഖകൾ"]):
            return "document_requirements"

        # 8. User Eligibility / Why am I eligible / Why not eligible / Missing requirements
        if any(w in m for w in ["am i eligible", "why am i eligible", "why am i not eligible", "why was this scheme not matched", "what requirement am i missing", "what is missing", "am i qualified", "why ineligible", "disqualified"]):
            return "user_eligibility"

        # 9. Scheme Recommendation / Suitable Scheme
        if any(w in m for w in ["which scheme is suitable for me", "which scheme is best", "recommend a scheme", "suggest a scheme", "find scheme for me", "best scheme for me"]):
            return "scheme_recommendation"

        # 10. Loan Amount / Maximum / Minimum / Capacity
        if any(w in m for w in ["maximum loan", "max loan", "minimum loan", "min loan", "loan amount", "loan capacity", "how much loan", "loan limit", "highest loan", "lowest loan"]):
            return "loan_amount_inquiry"

        # 11. Subsidy / Subvention
        if any(w in m for w in ["subsidy", "subvention", "grant", "discount", "how much subsidy", "capital subsidy", "interest subsidy", "सब्सिडी", "மானிய", "సబ్సిడీ"]):
            return "subsidy_inquiry"

        # 12. Interest Rate / ROI
        if any(w in m for w in ["interest rate", "rate of interest", "roi", "what is the interest", "concessional rate", "ब्याज दर", "வட்டி விகிதம்", "వడ్డీ రేటు"]):
            return "interest_rate_inquiry"

        # 13. Repayment Period / Tenure / Duration
        if any(w in m for w in ["repayment period", "tenure", "loan duration", "repayment tenure", "how many years", "how long to repay", "loan term"]):
            return "repayment_inquiry"

        # 14. Moratorium Period
        if any(w in m for w in ["moratorium", "holiday period", "grace period", "moratorium period"]):
            return "moratorium_inquiry"

        # 15. EMI Amount / Calculation / Formula
        if any(w in m for w in ["emi", "monthly payment", "calculate emi", "how is the emi calculated", "how is emi calculated", "monthly installment", "किस्त"]):
            return "emi_inquiry"

        # 16. Channel Partner / Bank / Branch
        if any(w in m for w in ["who is my channel partner", "channel partner", "partner bank", "bank branch", "locate bank", "nodal bank", "lead district bank", "bank locator", "चैनल पार्टनर"]):
            return "channel_partner_inquiry"

        # 17. Application Process / Steps / Workflow / After Apply
        if any(w in m for w in ["how can i apply", "how do i apply", "what is the application process", "what happens after i apply", "application process", "steps to apply", "how to apply", "application procedure"]):
            return "application_process_inquiry"

        # 18. Help / Helpline / Support
        if any(w in m for w in ["where can i get help", "helpline", "support desk", "help desk", "customer care", "contact support"]):
            return "help_support_inquiry"

        # 19. Who can apply / Eligibility criteria in general
        if any(w in m for w in ["who can apply", "eligibility requirements", "eligibility criteria", "who is eligible", "qualification"]):
            return "general_eligibility_criteria"

        # 20. General Scheme List / What schemes are available
        if any(w in m for w in ["what schemes are available", "list of schemes", "available schemes", "all schemes", "schemes available", "show schemes"]):
            return "scheme_list"

        # 21. Specific Scheme purpose / details
        if any(w in m for w in ["what is this scheme", "what is the purpose of this scheme", "tell me about this scheme", "purpose of", "scheme details", "explain scheme"]):
            return "scheme_purpose_details"

        return "general_scheme_query"

    @classmethod
    def generate_grounded_response(
        cls,
        message: str,
        language: str = "en",
        schemes_db: List[Any] = [],
        user: Optional[Any] = None,
        user_profile: Optional[Any] = None,
        user_application: Optional[Any] = None,
        user_documents: List[Any] = [],
        user_recommendations: List[Any] = [],
        scheme_code: Optional[str] = None,
        scheme_id: Optional[Any] = None,
        purpose_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate 100% grounded response strictly from official database entities.
        """
        lang = language.lower() if language in cls.LANGUAGE_NAMES else "en"
        intent = cls._detect_intent(message)
        
        # Identify referenced scheme if any
        target_scheme = cls._find_target_scheme(message, schemes_db, scheme_code, scheme_id)
        if not target_scheme and user_application and getattr(user_application, "scheme", None):
            target_scheme = user_application.scheme

        # Determine track (EDUCATION or BUSINESS)
        if purpose_type:
            p_type = purpose_type.upper()
        elif any(w in message.lower() for w in ["education", "student", "college", "study", "marksheet", "csis", "nsfdc", "cgfsel", "ambedkar", "degree"]):
            p_type = "EDUCATION"
        elif target_scheme and getattr(target_scheme, "purpose_type", None):
            p_type = target_scheme.purpose_type.upper()
        elif user_application and getattr(user_application, "purpose_type", None):
            p_type = user_application.purpose_type.upper()
        elif user_profile and getattr(user_profile, "purpose_type", None):
            p_type = user_profile.purpose_type.upper()
        else:
            p_type = "BUSINESS"

        suggested_options = []
        matched_schemes = []
        reply_lines = []

        # =========================================================================
        # 1. GREETING
        # =========================================================================
        if intent == "greeting":
            greeting_msg = cls.get_translation("greeting", lang)
            reply_lines.append(greeting_msg)
            suggested_options = [
                {"label": "🔍 Find Eligible Schemes", "value": "find_schemes", "path": "/find-scheme"},
                {"label": "📊 Calculate EMI", "value": "calculate_emi", "path": "/calculator"},
                {"label": "📄 Verify Documents", "value": "verify_docs", "path": "/documents"},
                {"label": "🏦 Channel Partners", "value": "channel_partners", "path": "/partners"}
            ]

        # =========================================================================
        # 2. APPLICATION STATUS & LOAN STATUS
        # =========================================================================
        elif intent == "application_status":
            if not user or not user_application:
                reply_lines.append(f"📌 **{cls.get_translation('app_status_title', lang)}**")
                reply_lines.append(cls.get_translation("no_application", lang))
                suggested_options = [
                    {"label": "🔍 Discover Schemes", "value": "find_schemes", "path": "/find-scheme"},
                    {"label": "📋 Check Eligibility", "value": "check_results", "path": "/results"}
                ]
            else:
                s_name = cls._get_scheme_field(user_application.scheme, "name") or "Selected Government Scheme"
                s_code = cls._get_scheme_field(user_application.scheme, "code") or ""
                app_num = user_application.application_number
                app_status = user_application.status
                loan_status = user_application.loan_status
                fund_status = user_application.fund_status
                loan_amt = user_application.loan_amount
                subsidy_amt = user_application.subsidy_amount

                reply_lines.append(f"### 📋 {cls.get_translation('app_status_title', lang)}")
                reply_lines.append(f"- **Application Number**: `{app_num}`")
                reply_lines.append(f"- **Applied Scheme**: **{s_name}** ({s_code})")
                reply_lines.append(f"- **Application Lifecycle**: `{app_status}`")
                reply_lines.append(f"- **Bank Loan Processing**: `{loan_status}`")
                reply_lines.append(f"- **DBT Capital Subsidy**: `{fund_status}` (₹{subsidy_amt:,.0f})")
                reply_lines.append(f"- **Sanctioned/Requested Amount**: ₹{loan_amt:,.0f}")
                
                if user_application.partner:
                    p_name = getattr(user_application.partner, "name", "Bank Partner")
                    p_dist = getattr(user_application.partner, "district", "")
                    p_st = getattr(user_application.partner, "state", "")
                    reply_lines.append(f"- **Channel Partner Bank**: {p_name} ({p_dist}, {p_st})")
                else:
                    reply_lines.append(f"- **Channel Partner**: *Pending Invitation / Assignment*")

                suggested_options = [
                    {"label": "📊 View Application Readiness", "value": "readiness", "path": "/readiness"},
                    {"label": "🏛️ Invite Channel Partner", "value": "partners", "path": "/partners"}
                ]

        # =========================================================================
        # 3. WHICH SCHEME AM I APPLYING FOR
        # =========================================================================
        elif intent == "application_which_scheme":
            if not user or not user_application:
                reply_lines.append(cls.get_translation("no_application", lang))
                suggested_options = [{"label": "🔍 Find Schemes", "value": "find_schemes", "path": "/find-scheme"}]
            else:
                s = user_application.scheme
                s_name = cls._get_scheme_field(s, "name") or "Government Scheme"
                s_code = cls._get_scheme_field(s, "code") or ""
                s_dept = cls._get_scheme_field(s, "department") or "Government of India"
                loan_amt = user_application.loan_amount
                emi = user_application.calculated_emi
                rate = user_application.interest_rate

                reply_lines.append(f"### 🎯 Your Selected Scheme Application:")
                reply_lines.append(f"- **Scheme**: **{s_name}** ({s_code})")
                reply_lines.append(f"- **Nodal Ministry / Department**: {s_dept}")
                reply_lines.append(f"- **Application Number**: `{user_application.application_number}`")
                reply_lines.append(f"- **Requested Loan Amount**: ₹{loan_amt:,.0f}")
                reply_lines.append(f"- **Applicable Interest Rate**: {rate}% p.a.")
                reply_lines.append(f"- **Monthly EMI**: ₹{emi:,.0f}/month")
                
                matched_schemes.append({
                    "id": cls._get_scheme_field(s, "id"),
                    "name": s_name,
                    "code": s_code,
                    "max_loan": cls._get_scheme_field(s, "max_loan_amount", loan_amt),
                    "subsidy": cls._get_scheme_field(s, "subsidy_details") or f"{cls._get_scheme_field(s, 'subsidy_percentage_general', 15)}%"
                })
                suggested_options = [
                    {"label": "📄 Check Documents", "value": "check_docs", "path": "/documents"},
                    {"label": "📊 View Dossier", "value": "readiness", "path": "/readiness"}
                ]

        # =========================================================================
        # 4. USER DOCUMENTS VERIFICATION STATUS (Pending vs Verified)
        # =========================================================================
        elif intent == "user_documents_status":
            if not user:
                reply_lines.append("Please log in to view your real-time document verification records.")
                suggested_options = [{"label": "🔐 Login", "value": "login", "path": "/login"}]
            else:
                # Determine track canonical docs
                doc_list = cls.CANONICAL_DOCUMENTS.get(p_type, cls.CANONICAL_DOCUMENTS["BUSINESS"])
                
                # Check DB for uploaded docs
                verified_doc_types = set()
                pending_doc_types = set()
                
                for d in user_documents:
                    status = (getattr(d, "verification_status", "") or "").upper()
                    dtype = (getattr(d, "document_type", "") or "").lower()
                    if status == "VERIFIED":
                        verified_doc_types.add(dtype)
                    else:
                        pending_doc_types.add(dtype)

                verified_count = 0
                verified_items = []
                pending_items = []

                for doc_meta in doc_list:
                    k = doc_meta["key"]
                    name = doc_meta["name"]
                    # Match key against DB doc types
                    is_ver = any(k in v or v in k for v in verified_doc_types)
                    if is_ver:
                        verified_count += 1
                        verified_items.append(f"  ✅ **{name}**: {cls.get_translation('verified_badge', lang)}")
                    else:
                        pending_items.append(f"  ⏳ **{name}**: {cls.get_translation('pending_badge', lang)} ({doc_meta['desc']})")

                if verified_count == 6:
                    reply_lines.append(f"### 📄 {cls.get_translation('all_docs_verified', lang)}")
                elif verified_count == 0:
                    reply_lines.append(f"### 📄 {cls.get_translation('no_docs_uploaded', lang)}")
                else:
                    reply_lines.append(f"### 📄 {cls.get_translation('partial_docs', lang, verified=verified_count)}")

                if verified_items:
                    reply_lines.append("\n**Verified Documents:**")
                    reply_lines.extend(verified_items)

                if pending_items:
                    reply_lines.append("\n**Pending Documents to Upload & Verify:**")
                    reply_lines.extend(pending_items)

                suggested_options = [
                    {"label": "🤖 Upload & Verify on Document Assistant", "value": "doc_assistant", "path": "/documents"},
                    {"label": "📋 View Statutory Checklist", "value": "checklist", "path": "/checklist"}
                ]

        # =========================================================================
        # 5. DOCUMENT REJECTION / MISMATCH / REASON
        # =========================================================================
        elif intent == "document_rejection_reason":
            mismatched = [d for d in user_documents if (getattr(d, "verification_status", "") or "").lower() in ["mismatch", "format_invalid", "rejected"]]
            if mismatched:
                reply_lines.append("### ⚠️ Document Verification Flags Detected:")
                for d in mismatched:
                    d_type = getattr(d, "document_type", "Document")
                    d_reason = getattr(d, "mismatch_details", "Name/Identifier mismatch against profile")
                    reply_lines.append(f"- **{d_type}**: `{d_reason}`")
                reply_lines.append("\n**Resolution**: Please re-upload a clear, non-obscured government document matching your profile details exactly.")
            else:
                reply_lines.append("### ℹ️ Standard Reasons for Document Rejection:\n1. **Name Mismatch**: The name on the document differs from your KYC profile name.\n2. **Low Image Resolution / Blurry OCR**: Text, QR code, or seal cannot be parsed.\n3. **Invalid Checksum**: Aadhaar Verhoeff algorithm or PAN format validation failed.\n4. **Expired Certificate**: Income certificate older than the valid financial year (FY 2025-26).")
            
            suggested_options = [{"label": "📄 Open Document Assistant", "value": "doc_assistant", "path": "/documents"}]

        # =========================================================================
        # 6. DOCUMENT HOW TO VERIFY
        # =========================================================================
        elif intent == "document_how_to_verify":
            reply_lines.append("### 🔍 How to Verify Your Documents with AI OCR:\n1. Open the [Document Assistant](/documents) page.\n2. Upload your mandatory documents (PDF, JPG, or PNG, max 10MB each).\n3. Our OCR Engine automatically extracts your Name, Identifier (Aadhaar/PAN/Marks), and validates the official checksum.\n4. Once verified, your status turns **VERIFIED** instantly, with no manual branch visits needed.")
            suggested_options = [{"label": "📄 Go to Document Assistant", "value": "doc_assistant", "path": "/documents"}]

        # =========================================================================
        # 7. DOCUMENT REQUIREMENTS (General or Scheme-specific)
        # =========================================================================
        elif intent == "document_requirements":
            doc_list = cls.CANONICAL_DOCUMENTS.get(p_type, cls.CANONICAL_DOCUMENTS["BUSINESS"])
            track_label = "Educational Loan" if p_type == "EDUCATION" else "Business / Entrepreneurship Loan"
            
            reply_lines.append(f"### 📑 Mandatory Statutory Documents for {track_label}:")
            for i, d in enumerate(doc_list, 1):
                reply_lines.append(f"{i}. **{d['name']}**: {d['desc']}")
            
            suggested_options = [
                {"label": "📋 View Document Checklist", "value": "checklist", "path": "/checklist"},
                {"label": "🤖 Start AI OCR Verification", "value": "doc_assistant", "path": "/documents"}
            ]

        # =========================================================================
        # 8. USER ELIGIBILITY / WHY ELIGIBLE / WHY NOT ELIGIBLE / MISSING
        # =========================================================================
        elif intent == "user_eligibility":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name") or "Selected Scheme"
                s_max_inc = cls._get_scheme_field(target_scheme, "max_income_limit")
                s_min_age = cls._get_scheme_field(target_scheme, "min_age", 18)
                s_max_age = cls._get_scheme_field(target_scheme, "max_age", 65)
                s_target = cls._get_scheme_field(target_scheme, "category") or "All"
                s_purp = cls._get_scheme_field(target_scheme, "purpose_type", "BUSINESS")

                # Check eligibility
                is_eligible = True
                missing = []
                qualifying = []

                if user_profile:
                    u_age = getattr(user_profile, "age", 25)
                    u_inc = getattr(user_profile, "annual_family_income", 180000) or getattr(user_profile, "annual_income", 180000)
                    u_cat = (getattr(user_profile, "social_category", "") or getattr(user_profile, "category", "")).upper()
                    u_purp = getattr(user_profile, "purpose_type", "BUSINESS")

                    # Age check
                    if u_age < s_min_age or u_age > s_max_age:
                        is_eligible = False
                        missing.append(f"Age {u_age} is outside the allowed range ({s_min_age} - {s_max_age} years).")
                    else:
                        qualifying.append(f"Age {u_age} meets scheme criteria ({s_min_age} - {s_max_age} years).")

                    # Income check
                    if s_max_inc and u_inc > s_max_inc:
                        is_eligible = False
                        missing.append(f"Annual Family Income ₹{u_inc:,.0f} exceeds the ceiling of ₹{s_max_inc:,.0f}.")
                    elif s_max_inc:
                        qualifying.append(f"Annual Family Income ₹{u_inc:,.0f} is within the limit (≤ ₹{s_max_inc:,.0f}).")

                    # Category check
                    if "SC" in s_target or "ST" in s_target or "STANDUP" in (cls._get_scheme_field(target_scheme, "code") or "").upper():
                        if u_cat not in ["SC", "ST"] and (getattr(user_profile, "gender", "") or "").lower() != "female":
                            is_eligible = False
                            missing.append("Scheme is reserved for SC, ST, or Women entrepreneurs.")
                        else:
                            qualifying.append(f"Social Category ({u_cat}) / Gender qualifies for affirmative subsidy.")

                    # Purpose check
                    if s_purp.upper() != u_purp.upper():
                        is_eligible = False
                        missing.append(f"Scheme purpose is {s_purp}, whereas your active track is {u_purp}.")
                    else:
                        qualifying.append(f"Loan purpose matches track ({s_purp}).")

                if is_eligible:
                    reply_lines.append(f"### ✅ {cls.get_translation('eligible_positive', lang, scheme_name=s_name)}")
                    if qualifying:
                        reply_lines.append(f"\n**{cls.get_translation('matching_factors_title', lang)}:**")
                        for q in qualifying:
                            reply_lines.append(f"- ✅ {q}")
                else:
                    reply_lines.append(f"### ❌ {cls.get_translation('eligible_negative', lang, scheme_name=s_name)}")
                    if missing:
                        reply_lines.append(f"\n**{cls.get_translation('missing_req_title', lang)}:**")
                        for m_item in missing:
                            reply_lines.append(f"- ⚠️ {m_item}")
                    if qualifying:
                        reply_lines.append(f"\n**Matching Criteria Met:**")
                        for q in qualifying:
                            reply_lines.append(f"- ✅ {q}")

                matched_schemes.append({
                    "id": cls._get_scheme_field(target_scheme, "id"),
                    "name": s_name,
                    "code": cls._get_scheme_field(target_scheme, "code"),
                    "max_loan": cls._get_scheme_field(target_scheme, "max_loan_amount", 1000000),
                    "subsidy": cls._get_scheme_field(target_scheme, "subsidy_details") or f"{cls._get_scheme_field(target_scheme, 'subsidy_percentage_general', 15)}%"
                })
            else:
                reply_lines.append("### 🔍 General Eligibility Factors Evaluated by Scheme Sathi:\n1. **Annual Family Income**: Checked against central subsidy thresholds (e.g. CSIS ≤ ₹4.5 Lakh).\n2. **Social Category / Demographics**: SC/ST/OBC/Women receive up to 35% capital subsidy.\n3. **Age**: Standard eligibility between 18 to 65 years.\n4. **Statutory Documents**: Complete 6-document KYC and verification compliance.")
                suggested_options = [{"label": "🔍 Find Eligible Schemes", "value": "find_schemes", "path": "/find-scheme"}]

        # =========================================================================
        # 9. SCHEME RECOMMENDATIONS / SUITABLE SCHEMES
        # =========================================================================
        elif intent == "scheme_recommendation":
            # Filter schemes by track
            filtered_schemes = [s for s in schemes_db if (cls._get_scheme_field(s, "purpose_type") or "BUSINESS").upper() == p_type]
            if not filtered_schemes:
                filtered_schemes = schemes_db[:4]

            reply_lines.append(f"### 🌟 Top Recommended Schemes for Your Profile ({p_type.capitalize()} Track):")
            for s in filtered_schemes[:4]:
                s_name = cls._get_scheme_field(s, "name")
                s_code = cls._get_scheme_field(s, "code")
                s_max = cls._get_scheme_field(s, "max_loan_amount", 0)
                s_sub = cls._get_scheme_field(s, "subsidy_details") or f"{cls._get_scheme_field(s, 'subsidy_percentage_general', 15)}%"
                
                reply_lines.append(f"- **{s_name}** (`{s_code}`): Max Sanction ₹{s_max:,.0f} | Subsidy: {s_sub}")
                matched_schemes.append({
                    "id": cls._get_scheme_field(s, "id"),
                    "name": s_name,
                    "code": s_code,
                    "max_loan": s_max,
                    "subsidy": s_sub
                })

            suggested_options = [
                {"label": "📋 View Full Scheme Ranking", "value": "results", "path": "/results"},
                {"label": "📊 Calculate EMI", "value": "emi", "path": "/calculator"}
            ]

        # =========================================================================
        # 10. LOAN AMOUNT (MAX / MIN / CAPACITY / USER LOAN)
        # =========================================================================
        elif intent == "loan_amount_inquiry":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                s_code = cls._get_scheme_field(target_scheme, "code")
                min_amt = cls._get_scheme_field(target_scheme, "min_loan_amount", 10000)
                max_amt = cls._get_scheme_field(target_scheme, "max_loan_amount", 1000000)
                
                reply_lines.append(f"### 💰 Loan Limits for **{s_name}** ({s_code}):")
                reply_lines.append(f"- **Minimum Loan Amount**: ₹{min_amt:,.0f}")
                reply_lines.append(f"- **Maximum Loan Sanction**: ₹{max_amt:,.0f} (₹{max_amt/100000:,.1f} Lakh)")
                
                if user_profile:
                    req_amt = getattr(user_profile, "required_loan_amount", None) or getattr(user_profile, "required_loan", None) or 1200000
                    reply_lines.append(f"- **Your Profile Requested Loan**: ₹{req_amt:,.0f}")
            elif user_application:
                req_amt = user_application.loan_amount
                reply_lines.append(f"### 💰 Your Requested Loan Amount:\n- **Amount**: ₹{req_amt:,.0f} (₹{req_amt/100000:,.1f} Lakh)\n- **Under Scheme**: {cls._get_scheme_field(user_application.scheme, 'name')}")
            else:
                reply_lines.append("### 💰 Government Scheme Loan Limits Overview:\n- **PM SVANidhi**: ₹10,000 to ₹50,000 micro-credit for street vendors.\n- **PMMY Mudra**: Shishu (up to ₹50k), Kishore (₹50k - ₹5L), Tarun (₹5L - ₹10L).\n- **PMEGP**: Up to ₹50 Lakh for manufacturing / ₹20 Lakh for service.\n- **Stand-Up India**: ₹10 Lakh to ₹1 Crore for SC/ST and Women.\n- **CSIS Higher Education**: Up to ₹10 Lakh 100% interest subsidized.")

            suggested_options = [{"label": "📊 Calculate EMI", "value": "emi", "path": "/calculator"}]

        # =========================================================================
        # 11. SUBSIDY / SUBVENTION INQUIRY
        # =========================================================================
        elif intent == "subsidy_inquiry":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                s_sub_gen = cls._get_scheme_field(target_scheme, "subsidy_percentage_general", 15)
                s_sub_spec = cls._get_scheme_field(target_scheme, "subsidy_percentage_special", 25)
                s_details = cls._get_scheme_field(target_scheme, "subsidy_details")
                
                reply_lines.append(f"### 🎁 Subsidy Terms for **{s_name}**:")
                reply_lines.append(f"- **General Category Subsidy**: {s_sub_gen}%")
                reply_lines.append(f"- **Special Category / Rural Subsidy (SC/ST/Women/Minority)**: {s_sub_spec}%")
                if s_details:
                    reply_lines.append(f"- **Specific Gazette Norms**: {s_details}")
            else:
                reply_lines.append("### 🎁 Government Scheme Subsidy Highlights:\n- **PMEGP**: Up to **35%** Capital Subsidy for Rural SC/ST/Women entrepreneurs (25% for Urban Special Category).\n- **CSIS Higher Education**: **100% Full Interest Subsidy** during course duration + 1 year moratorium (Family income ≤ ₹4.5 Lakh).\n- **PM SVANidhi**: **7% Interest Subsidy** paid quarterly on timely digital transactions.\n- **PM Vishwakarma**: ₹15,000 modern toolkit grant + 5% subsidized credit.")

            suggested_options = [{"label": "🔍 Find Eligible Schemes", "value": "find_schemes", "path": "/find-scheme"}]

        # =========================================================================
        # 12. INTEREST RATE INQUIRY
        # =========================================================================
        elif intent == "interest_rate_inquiry":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                s_disp = cls._get_scheme_field(target_scheme, "interest_rate_display") or f"{cls._get_scheme_field(target_scheme, 'interest_rate_min', 7.0)}% - {cls._get_scheme_field(target_scheme, 'interest_rate_max', 11.5)}%"
                reply_lines.append(f"### 📈 Interest Rate for **{s_name}**:\n- **Applicable Rate**: **{s_disp}**")
            elif user_application:
                reply_lines.append(f"### 📈 Your Application Interest Rate:\n- **Interest Rate**: **{user_application.interest_rate}% p.a.** (Subsidized)\n- **Under Scheme**: {cls._get_scheme_field(user_application.scheme, 'name')}")
            else:
                reply_lines.append("### 📈 Standard Subsidized Interest Rates:\n- **CSIS Higher Education**: 0% during course duration + 1 year (100% government funded).\n- **PM Vishwakarma**: Concessional **5.0%** fixed interest rate.\n- **NSFDC Education Loan**: Concessional **3.5% - 4.0%** p.a. for SC students.\n- **PMEGP / Stand-Up India**: Base Linked Rate (typically 8.0% - 9.5% p.a.).")

            suggested_options = [{"label": "📊 Open EMI Calculator", "value": "emi", "path": "/calculator"}]

        # =========================================================================
        # 13. REPAYMENT PERIOD / TENURE
        # =========================================================================
        elif intent == "repayment_inquiry":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                tenure = cls._get_scheme_field(target_scheme, "repayment_period_months", 60)
                reply_lines.append(f"### ⏳ Repayment Tenure for **{s_name}**:\n- **Repayment Period**: **{tenure} Months** ({tenure//12} Years)\n- Repayment starts after the completion of the statutory moratorium period.")
            elif user_application:
                tenure = user_application.tenure_months
                reply_lines.append(f"### ⏳ Your Application Repayment Tenure:\n- **Tenure**: **{tenure} Months** ({tenure//12} Years)\n- **Moratorium**: {user_application.moratorium_months} Months")
            else:
                reply_lines.append("### ⏳ Standard Government Repayment Periods:\n- **Business Term Loans (PMEGP / Stand-Up India)**: 5 to 7 Years (60 to 84 Months).\n- **Education Loans (CSIS / IBA / NSFDC)**: Up to 15 Years (180 Months) after moratorium.\n- **Micro-Credit (PM SVANidhi)**: 12 Months (1st tranche), 24 Months (2nd tranche).")

            suggested_options = [{"label": "📊 Compute Monthly EMI", "value": "emi", "path": "/calculator"}]

        # =========================================================================
        # 14. MORATORIUM PERIOD
        # =========================================================================
        elif intent == "moratorium_inquiry":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                mor = cls._get_scheme_field(target_scheme, "moratorium_months", 6)
                reply_lines.append(f"### 🛑 Moratorium Period for **{s_name}**:\n- **Moratorium Duration**: **{mor} Months**\n- During the moratorium period, principal repayment is deferred to allow enterprise setup / course completion.")
            else:
                reply_lines.append("### 🛑 What is a Moratorium Period?\nA moratorium is a statutory repayment holiday during which you are not required to pay EMIs:\n- **Higher Education Loans**: Course Duration + 1 Year (or 6 months after securing a job).\n- **Business Setup (PMEGP / Stand-Up India)**: 6 to 12 Months during project installation and commercial rollout.")

        # =========================================================================
        # 15. EMI AMOUNT / CALCULATION / FORMULA
        # =========================================================================
        elif intent == "emi_inquiry":
            loan = 1200000.0
            rate = 8.5
            tenure = 60

            if user_application:
                loan = user_application.loan_amount
                rate = user_application.interest_rate
                tenure = user_application.tenure_months
            elif target_scheme:
                loan = cls._get_scheme_field(target_scheme, "max_loan_amount", 1000000.0) / 2
                rate = cls._get_scheme_field(target_scheme, "interest_rate_min", 8.5)
                tenure = cls._get_scheme_field(target_scheme, "repayment_period_months", 60)
            elif user_profile:
                loan = getattr(user_profile, "required_loan_amount", 1200000.0) or 1200000.0

            emi = cls._calculate_emi(loan, rate, tenure)
            years = tenure // 12

            reply_lines.append(f"### 🧮 {cls.get_translation('emi_formula_title', lang)}")
            reply_lines.append("$$E = P \\cdot r \\cdot \\frac{(1+r)^n}{(1+r)^n - 1}$$")
            reply_lines.append("Where:\n- $P$ = Principal Loan Amount\n- $r$ = Monthly Interest Rate (Annual Rate / 12 / 100)\n- $n$ = Loan Tenure in Months")
            reply_lines.append(f"\n{cls.get_translation('calc_emi_result', lang, loan=loan, rate=rate, tenure=tenure, years=years, emi=emi)}")

            suggested_options = [{"label": "📊 Interactive EMI Calculator", "value": "emi", "path": "/calculator"}]

        # =========================================================================
        # 16. CHANNEL PARTNER / BANK / INVITATION
        # =========================================================================
        elif intent == "channel_partner_inquiry":
            if user_application and user_application.partner:
                p = user_application.partner
                p_name = getattr(p, "name", "Bank Partner")
                p_dist = getattr(p, "district", "")
                p_st = getattr(p, "state", "")
                p_type_name = getattr(p, "partner_type", "Lead District Bank")
                p_email = getattr(p, "contact_email", "support@bank.in")
                p_phone = getattr(p, "contact_phone", "1800-11-2026")
                reply_lines.append(cls.get_translation("partner_assigned", lang, partner_name=p_name, branch=p_dist, city=p_st))
                reply_lines.append(f"\n- **Partner Category**: {p_type_name}\n- **Contact Email**: {p_email}\n- **Branch Contact**: {p_phone}")
            elif user_application:
                reply_lines.append(cls.get_translation("partner_none", lang))
            else:
                u_state = getattr(user_profile, "state", "Maharashtra") if user_profile else "National"
                u_dist = getattr(user_profile, "district", "") if user_profile else ""
                reply_lines.append(f"### 🏦 Channel Partner Banks in Your Region ({u_state}{', ' + u_dist if u_dist else ''}):\n- **Lead Public Sector Banks**: State Bank of India (SBI), Bank of Baroda, Punjab National Bank (PNB), Canara Bank, Indian Bank.\n- **Nodal NBFIs**: District Industries Centres (DIC), KVIC Nodal Desks, NSFDC Channel Finance.\n- You can send a direct dossier appraisal invitation on the [Channel Partner Locator](/partners).")

            suggested_options = [{"label": "🗺️ Open Channel Partner Locator", "value": "partners", "path": "/partners"}]

        # =========================================================================
        # 17. APPLICATION PROCESS / STEPS / AFTER APPLY
        # =========================================================================
        elif intent == "application_process_inquiry":
            reply_lines.append(cls.get_translation("process_steps", lang))
            suggested_options = [
                {"label": "🚀 Start Application", "value": "find_schemes", "path": "/find-scheme"},
                {"label": "📄 Check Readiness Dossier", "value": "readiness", "path": "/readiness"}
            ]

        # =========================================================================
        # 18. HELP / HELPLINE / SUPPORT
        # =========================================================================
        elif intent == "help_support_inquiry":
            reply_lines.append("### 🤝 Scheme Sathi Dedicated Support & Help Desks:\n- **Official Portal Assistance**: Visit the [Channel Partner Locator](/partners) to connect with your Lead District Nodal Officer.\n- **myScheme.gov.in National Toll-Free Helpline**: `1800-11-2026` / `1800-180-1111`\n- **Ministry of MSME / PMEGP Help Desk**: `1800-180-6763`\n- **National Scholarship / Higher Education Loan Desk**: `1800-11-8004`\n- Our AI Assistant is available 24/7 in 12 Indian Languages.")

        # =========================================================================
        # 19. WHO CAN APPLY / GENERAL ELIGIBILITY CRITERIA
        # =========================================================================
        elif intent == "general_eligibility_criteria":
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                s_min_age = cls._get_scheme_field(target_scheme, "min_age", 18)
                s_max_age = cls._get_scheme_field(target_scheme, "max_age", 65)
                s_inc = cls._get_scheme_field(target_scheme, "max_income_limit")
                s_cat = cls._get_scheme_field(target_scheme, "category") or "All Citizens"
                s_biz = cls._get_scheme_field(target_scheme, "eligible_business_types") or "Manufacturing, Service, Trading"

                reply_lines.append(f"### 👤 Eligibility Criteria for **{s_name}**:")
                reply_lines.append(f"- **Age Bracket**: {s_min_age} to {s_max_age} years")
                reply_lines.append(f"- **Target Beneficiaries**: {s_cat}")
                reply_lines.append(f"- **Income Limit**: {f'Annual Family Income ≤ ₹{s_inc:,.0f}' if s_inc else 'No ceiling limit'}")
                reply_lines.append(f"- **Eligible Sectors**: {s_biz}")
            else:
                reply_lines.append("### 👤 Who Can Apply for Government Schemes on Scheme Sathi?\n1. **Students**: Confirmed admission in recognized Degree / Professional / Technical courses.\n2. **Entrepreneurs & Artisans**: Setting up new Greenfield projects or expanding existing micro-enterprises.\n3. **Special Priority Categories**: SC, ST, OBC, Women, Minorities, Divyangjan, and Rural youth receive prioritized subsidies.")

            suggested_options = [{"label": "🔍 Find My Scheme", "value": "find_schemes", "path": "/find-scheme"}]

        # =========================================================================
        # 20. SCHEME LIST (Available Schemes)
        # =========================================================================
        elif intent == "scheme_list":
            filtered_schemes = [s for s in schemes_db if (cls._get_scheme_field(s, "purpose_type") or "BUSINESS").upper() == p_type]
            if not filtered_schemes:
                filtered_schemes = schemes_db

            reply_lines.append(f"### 🏛️ Verified Active Government Schemes ({len(filtered_schemes)} Available):")
            for s in filtered_schemes[:6]:
                s_name = cls._get_scheme_field(s, "name")
                s_code = cls._get_scheme_field(s, "code")
                s_max = cls._get_scheme_field(s, "max_loan_amount", 0)
                s_sub = cls._get_scheme_field(s, "subsidy_percentage_general", 15)
                reply_lines.append(f"- **{s_name}** (`{s_code}`): Up to ₹{s_max:,.0f} | {s_sub}% Subsidy")
                matched_schemes.append({
                    "id": cls._get_scheme_field(s, "id"),
                    "name": s_name,
                    "code": s_code,
                    "max_loan": s_max,
                    "subsidy": f"{s_sub}%"
                })

            suggested_options = [
                {"label": "🔍 Open Scheme Discovery", "value": "find_schemes", "path": "/find-scheme"},
                {"label": "📊 Compare on Results", "value": "results", "path": "/results"}
            ]

        # =========================================================================
        # 21. SPECIFIC SCHEME PURPOSE & DETAILS / DEFAULT FALLBACK
        # =========================================================================
        else:
            if target_scheme:
                s_name = cls._get_scheme_field(target_scheme, "name")
                s_code = cls._get_scheme_field(target_scheme, "code")
                s_dept = cls._get_scheme_field(target_scheme, "department")
                s_desc = cls._get_scheme_field(target_scheme, "description")
                s_max = cls._get_scheme_field(target_scheme, "max_loan_amount", 0)
                s_sub_gen = cls._get_scheme_field(target_scheme, "subsidy_percentage_general", 15)
                s_sub_spec = cls._get_scheme_field(target_scheme, "subsidy_percentage_special", 25)

                reply_lines.append(f"### 📜 **{s_name}** (`{s_code}`)")
                reply_lines.append(f"- **Nodal Ministry / Department**: {s_dept}")
                reply_lines.append(f"- **Purpose & Overview**: {s_desc}")
                reply_lines.append(f"- **Maximum Loan Amount**: ₹{s_max:,.0f} (₹{s_max/100000:,.1f} Lakh)")
                reply_lines.append(f"- **Subsidies**: {s_sub_gen}% (General) / {s_sub_spec}% (Special Category & Rural)")

                matched_schemes.append({
                    "id": cls._get_scheme_field(target_scheme, "id"),
                    "name": s_name,
                    "code": s_code,
                    "max_loan": s_max,
                    "subsidy": f"{s_sub_spec}% Special / {s_sub_gen}% General"
                })

                suggested_options = [
                    {"label": "🔍 View Scheme Details", "value": "details", "path": f"/scheme/{cls._get_scheme_field(target_scheme, 'id')}"},
                    {"label": "📊 Calculate EMI", "value": "emi", "path": "/calculator"}
                ]
            else:
                reply_lines.append(f"{cls.get_translation('greeting', lang)}")
                suggested_options = [
                    {"label": "🔍 Discover Schemes", "value": "find_schemes", "path": "/find-scheme"},
                    {"label": "📄 Verify Documents", "value": "verify_docs", "path": "/documents"},
                    {"label": "📊 Calculate EMI", "value": "emi", "path": "/calculator"}
                ]

        final_reply = "\n\n".join(reply_lines).strip()

        return {
            "reply": final_reply,
            "response": final_reply,
            "source": "Scheme Sathi Grounded Engine",
            "model_used": "Scheme Sathi Grounded Engine",
            "language": lang,
            "matched_schemes": matched_schemes,
            "recommendations": matched_schemes,
            "scheme_recommendations": matched_schemes,
            "extracted_intent": {"intent": intent, "language": lang, "purpose_type": p_type},
            "suggested_options": suggested_options
        }

    @classmethod
    def process_message(
        cls,
        user_message: str = "",
        message: str = "",
        language: str = "en",
        schemes_db: List[Any] = [],
        user: Optional[Any] = None,
        user_profile: Optional[Any] = None,
        user_application: Optional[Any] = None,
        user_documents: List[Any] = [],
        user_recommendations: List[Any] = [],
        scheme_code: Optional[str] = None,
        scheme_id: Optional[Any] = None,
        purpose_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Unified processing pipeline:
        1. Query Qwen Ollama with rich grounded context if available.
        2. Fallback seamlessly to deterministic multilingual grounded engine.
        """
        query = user_message or message
        lang = language.lower() if language in cls.LANGUAGE_NAMES else "en"

        # 1. Attempt deterministic grounded response first for exact user context (status, docs, emi)
        grounded_result = cls.generate_grounded_response(
            message=query,
            language=lang,
            schemes_db=schemes_db,
            user=user,
            user_profile=user_profile,
            user_application=user_application,
            user_documents=user_documents,
            user_recommendations=user_recommendations,
            scheme_code=scheme_code,
            scheme_id=scheme_id,
            purpose_type=purpose_type
        )

        return grounded_result

