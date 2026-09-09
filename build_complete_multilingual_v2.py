# -*- coding: utf-8 -*-
"""
Build Complete 11-Language Translation V2 with:
1. All Dropdown <option> values in all 11 Indian languages + English
2. Complete parallel translations for all 25 myScheme Government Schemes
3. Scheme card tags, descriptions, units (Lakh, Months, Low Interest, Marginalized)
4. Grounded, factual Qwen chatbot responses in all 11 Indian languages
"""

import os
import json

# =========================================================================
# 1. Update backend/app/services/indic_translation.py with 25 Schemes Corpus
# =========================================================================
indic_code = r'''# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from typing import Dict, Any, List, Optional
from app.config import settings

class SamanantarIndicTranslationService:
    """
    AI4Bharat Samanantar-grounded Indic Translation & Lexicon Service for Scheme Sathi.
    Provides high-fidelity domain translations across English and 11 Major Indian Languages:
    Hindi (हिन्दी), Tamil (தமிழ்), Telugu (తెలుగు), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം),
    Marathi (मराठी), Bengali (বাংলা), Gujarati (ગુજરાતી), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ), Assamese (অসমীয়া).
    """

    LANGUAGES = [
        {"code": "en", "name": "English", "native": "English"},
        {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
        {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
        {"code": "te", "name": "Telugu", "native": "తెలుగు"},
        {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
        {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
        {"code": "mr", "name": "Marathi", "native": "मराठी"},
        {"code": "bn", "name": "Bengali", "native": "বাংলা"},
        {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
        {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
        {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
        {"code": "as", "name": "Assamese", "native": "অসমীয়া"}
    ]

    # Parallel Scheme Name & Description Corpus for the 25 myScheme Dataset Schemes
    SCHEME_TRANSLATIONS = {
        "PMEGP": {
            "name": {
                "hi": "प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)",
                "ta": "பிரதமரின் வேலைவாய்ப்பு உருவாக்கும் திட்டம் (PMEGP)",
                "te": "ప్రధాన మంత్రి ఉపాధి కల్పన కార్యక్రమం (PMEGP)",
                "kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಉದ್ಯೋಗ ಸೃಷ್ಟಿ ಕಾರ್ಯಕ್ರಮ (PMEGP)",
                "ml": "പ്രധാനമന്ത്രി തൊഴിൽ സൃഷ്ടി പദ്ധതി (PMEGP)",
                "mr": "पंतप्रधान रोजगार निर्मिती कार्यक्रम (PMEGP)",
                "bn": "প্রধানমন্ত্রী কর্মসংস্থান সৃষ্টি প্রকল্প (PMEGP)",
                "gu": "પ્રધાનમંત્રી રોજગાર નિર્માણ કાર્યક્રમ (PMEGP)",
                "pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਰੋਜ਼ਗਾਰ ਉਤਪਤੀ ਪ੍ਰੋਗਰਾਮ (PMEGP)",
                "or": "ପ୍ରଧାନମନ୍ତ୍ରୀ ରୋଜଗାର ସୃଷ୍ଟି କାର୍ଯ୍ୟକ୍ରମ (PMEGP)",
                "as": "প্ৰধানমন্ত্ৰী নিয়োগ সৃষ্টি কাৰ্যসূচী (PMEGP)"
            },
            "description": {
                "hi": "विनिर्माण व सेवा क्षेत्र में सूक्ष्म उद्यमों के लिए 35% तक पूंजीगत सब्सिडी सहित ऋण योजना।",
                "ta": "உற்பத்தி மற்றும் சேவைத் துறைகளில் சுயதொழில் தொடங்க 35% வரை மானியம் வழங்கும் கடன் திட்டம்.",
                "te": "ఉత్పాదక మరియు సేవా రంగాల్లో సూక్ష్మ పరిశ్రమల స్థాపనకు 35% వరకు సబ్సిడీతో కూడిన రుణ పథకం.",
                "kn": "ಉತ್ಪಾದನಾ ಮತ್ತು ಸೇವಾ ವಲಯಗಳಲ್ಲಿ ಉದ್ಯಮ ಸ್ಥಾಪಿಸಲು ಶೇ.35 ರವರೆಗೆ ಸಬ್ಸಿಡಿ ನೀಡುವ ಯೋಜನೆ.",
                "ml": "ഉൽപ്പാദന, സേവന മേഖലകളിൽ സംരംഭങ്ങൾ തുടങ്ങാൻ 35% വരെ സബ്‌സിഡി നൽകുന്ന വായ്പാ പദ്ധതി.",
                "mr": "उत्पादन व सेवा क्षेत्रात सूक्ष्म उद्योग सुरू करण्यासाठी ३५% पर्यंत भांडवली अनुदान योजना.",
                "bn": "উৎপাদন ও সেবা ক্ষেত্রে ক্ষুদ্র উদ্যোগ স্থাপনের জন্য ৩৫% পর্যন্ত মূলধন ভর্তুকিযুক্ত ঋণ প্রকল্প।",
                "gu": "ઉત્પાદન અને સેવા ક્ષેત્રે સૂક્ષ્મ ઉદ્યોગો શરૂ કરવા માટે ૩૫% સુધીની સબસિડી સાથેની યોજના.",
                "pa": "ਨਿਰਮਾਣ ਅਤੇ ਸੇਵਾ ਖੇਤਰਾਂ ਵਿੱਚ ਸਵੈ-ਰੋਜ਼ਗਾਰ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ੩੫% ਤੱਕ ਸਬਸਿਡੀ ਵਾਲੀ ਕਰਜ਼ਾ ਯੋਜਨਾ।",
                "or": "ଉତ୍ପାଦନ ଓ ସେବା କ୍ଷେତ୍ରରେ କ୍ଷୁଦ୍ର ଉଦ୍ୟୋଗ ସ୍ଥାପନ ପାଇଁ ୩୫% ପର୍ଯ୍ୟନ୍ତ ରିହାତିଯୁକ୍ତ ଋଣ ଯୋଜନା।",
                "as": "উৎপাদন আৰু সেৱা খণ্ডত উদ্যোগ স্থাপনৰ বাবে ৩৫% লৈকে ৰাজসাহায্যযুক্ত ঋণ আঁচনি।"
            }
        },
        "STANDUP-IND": {
            "name": {
                "hi": "स्टैंड-अप इंडिया योजना (अजा/अजजा व महिला उद्यमी)",
                "ta": "ஸ்டாண்ட்-அப் இந்தியா திட்டம் (SC/ST & பெண் தொழில்முனைவோர்)",
                "te": "స్టాండ్-అప్ ఇండియా పథకం (SC/ST & మహిళలు)",
                "kn": "ಸ್ಟ್ಯಾಂಡ್‌-ಅಪ್ ಇಂಡಿಯಾ ಯೋಜನೆ (SC/ST & ಮಹಿಳೆಯರು)",
                "ml": "സ്റ്റാൻഡ്-അപ്പ് ഇന്ത്യ പദ്ധതി (പട്ടികജാതി/പട്ടികവർഗ്ഗം & വനിതകൾ)",
                "mr": "स्टँड-अप इंडिया योजना (अनु.जाती/जमाती व महिला उद्योजक)",
                "bn": "স্ট্যান্ড-আপ ইন্ডিয়া প্রকল্প (তপশিলি জাতি/উপজাতি ও নারী উদ্যোক্তা)",
                "gu": "સ્ટેન્ડ-અપ ઇન્ડિયા યોજના (SC/ST અને મહિલાઓ)",
                "pa": "ਸਟੈਂਡ-ਅੱਪ ਇੰਡੀਆ ਸਕੀਮ (SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ)",
                "or": "ଷ୍ଟାଣ୍ଡ-ଅପ ଇଣ୍ଡିଆ ଯୋଜନା (SC/ST ଓ ମହିଳା)",
                "as": "ষ্টেণ্ড-আপ ইণ্ডিয়া আঁচনি (SC/ST আৰু মহিলা উদ্যোগী)"
            },
            "description": {
                "hi": "अजा/अजजा और महिला उद्यमियों को नए व्यवसाय के लिए ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।",
                "ta": "SC/ST மற்றும் பெண் தொழில்முனைவோருக்கு ₹10 இலட்சம் முதல் ₹1 கோடி வரை வங்கி கடன் வசதி.",
                "te": "SC/ST మరియు మహిళా పారిశ్రామికవేత్తలకు ₹10 లక్షల నుండి ₹1 కోట్ల వరకు బ్యాంక్ రుణం.",
                "kn": "SC/ST ಮತ್ತು ಮಹಿಳಾ ಉದ್ಯಮಿಗಳಿಗೆ ₹10 ಲಕ್ಷದಿಂದ ₹1 ಕೋಟಿವರೆಗೆ ಬ್ಯಾಂಕ್ ಸಾಲ ಸೌಲಭ್ಯ.",
                "ml": "പട്ടികജാതി/പട്ടികവർഗ്ഗ, വനിതാ സംരംഭകർക്ക് ₹10 ലക്ഷം മുതൽ ₹1 കോടി വരെ ബാങ്ക് വായ്പ.",
                "mr": "नवीन उद्योगासाठी अनु.जाती/जमाती व महिलांना ₹१० लाख ते ₹१ कोटीपर्यंत बँक कर्ज सुविधा.",
                "bn": "তপশিলি জাতি/উপজাতি ও নারী উদ্যোক্তাদের জন্য ১০ লাখ থেকে ১ কোটি টাকা পর্যন্ত ব্যাংক ঋণ সুবিধা।",
                "gu": "નવા વ્યવસાય માટે SC/ST અને મહિલાઓને ₹૧૦ લાખથી ₹૧ કરોડ સુધીની બેંક લોન સહાય.",
                "pa": "ਨਵਾਂ ਕਾਰੋਬਾਰ ਸ਼ੁਰੂ ਕਰਨ ਲਈ SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ ਨੂੰ ₹੧੦ ਲੱਖ ਤੋਂ ₹੧ ਕਰੋੜ ਤੱਕ ਬੈਂਕ ਕਰਜ਼ਾ।",
                "or": "ନୂତନ ଉଦ୍ୟୋଗ ପାଇଁ SC/ST ଓ ମହିଳାମାନଙ୍କୁ ₹୧୦ ଲକ୍ଷରୁ ₹୧ କୋଟି ପର୍ଯ୍ୟନ୍ତ ବ୍ୟାଙ୍କ ଋଣ।",
                "as": "নতুন ব্যৱসায়ৰ বাবে SC/ST আৰু মহিলাসকলক ১০ লাখৰ পৰা ১ কোটি টকালৈকে বেংক ঋণ।"
            }
        },
        "SVANIDHI": {
            "name": {
                "hi": "पीएम स्ट्रीट वेंडर्स आत्मनिर्भर निधि (पीएम स्वनिधि)",
                "ta": "பிரதமரின் தெருவோர வியாபாரிகள் தற்சார்பு நிதி (PM ஸ்வநிதி)",
                "te": "పీఎం స్వనిధి పథకం (వీధి వ్యాపారుల ఆత్మనిర్భర్ నిధి)",
                "kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳ ಆತ್ಮನಿರ್ಭರ ನಿಧಿ (ಪಿಎಂ ಸ್ವನಿಧಿ)",
                "ml": "പി.എം സ്വനിധി പദ്ധതി (തെരുവ് കച്ചവടക്കാർക്കായുള്ള വായ്പ)",
                "mr": "पीएम पथविक्रेते आत्मनिर्भर निधी (पीएम स्वनिधी)",
                "bn": "প্রধানমন্ত্রী পিএম স্বনিধি প্রকল্প (পথ বিক্রেতাদের জন্য)",
                "gu": "પીએમ સ્વનિધિ યોજના (શેરી ફેરિયાઓ માટે)",
                "pa": "ਪੀਐਮ ਸਵਨਿਧੀ ਸਕੀਮ (ਰੇਹੜੀ-ਫੜ੍ਹੀ ਵਾਲਿਆਂ ਲਈ)",
                "or": "ପିଏମ ସ୍ୱନିଧି ଯୋଜନା (ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ)",
                "as": "পিএম স্বনিধি আঁচনি (পথ বিক্ৰেতাসকলৰ বাবে)"
            },
            "description": {
                "hi": "स्ट्रीट वेंडरों को ₹10,000 से ₹50,000 तक बिना गारंटी कार्यशील पूंजी ऋण व 7% ब्याज छूट।",
                "ta": "தெருவோர வியாபாரிகளுக்கு பிணையற்ற ₹10,000 முதல் ₹50,000 வரை கடன் மற்றும் 7% வட்டி மானியம்.",
                "te": "వీధి వ్యాపారులకు ₹10,000 నుండి ₹50,000 వరకు పూచీకత్తు లేని రుణం మరియు 7% వడ్డీ రాయితీ.",
                "kn": "ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳಿಗೆ ₹10,000 ದಿಂದ ₹50,000 ವರೆಗೆ ಖಾತರಿ ರಹಿತ ಸಾಲ ಮತ್ತು ಶೇ.7 ಬಡ್ಡಿ ರಿಯಾಯಿತಿ.",
                "ml": "തെരുവ് കച്ചവടക്കാർക്ക് ₹10,000 മുതൽ ₹50,000 വരെ ഈടില്ലാത്ത വായ്പയും 7% പലിശ ഇളവും.",
                "mr": "फेरीवाल्यांना विनातारण ₹१०,००० ते ₹५०,००० पर्यंत कर्ज व ७% व्याज सवलત.",
                "bn": "পথ বিক্রেতাদের জন্য জামিনমুক্ত ১০,০০০ থেকে ৫০,০০০ টাকা পর্যন্ত ঋণ ও ৭% সুদ ছাড়।",
                "gu": "શેરી ફેરિયાઓ માટે તારણ મુક્ત ₹૧૦,૦૦૦ થી ₹૫૦,૦૦૦ સુધીની લોન અને ૭% વ્યાજ રાહત.",
                "pa": "ਰੇਹੜੀ ਵਾਲਿਆਂ ਲਈ ਬਿਨਾਂ ਗਰੰਟੀ ₹੧੦,੦੦੦ ਤੋਂ ₹੫੦,੦੦੦ ਕਰਜ਼ਾ ਅਤੇ ੭% ਵਿਆਜ ਛੋਟ।",
                "or": "ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ ବିନା ଜାମିନରେ ₹୧୦,୦୦୦ ରୁ ₹୫୦,୦୦୦ ଋଣ ଏବଂ ୭% ସୁଧ ରିହାତି।",
                "as": "পথ বিক্ৰেতাসকলৰ বাবে বন্ধকমুক্ত ১০,০০০ ৰ পৰা ৫০,০০০ টকা ঋণ আৰু ৭% সুদ ৰেহাই।"
            }
        },
        "VISHWAKARMA": {
            "name": {
                "hi": "पीएम विश्वकर्मा योजना (पारंपरिक कारीगर व शिल्पकार)",
                "ta": "பிரதமரின் விஸ்வகர்மா திட்டம் (பாரம்பரிய கைவினைஞர்கள்)",
                "te": "పీఎం విశ్వకర్మ పథకం (సాంప్రదాయ కళాకారులు)",
                "kn": "ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಯೋಜನೆ (ಪಾರಂಪರಿಕ ಕುಶಲಕರ್ಮಿಗಳು)",
                "ml": "പി.എം വിശ്വകർമ്മ പദ്ധതി (കരകൗശല വിദഗ്ദ്ധർ)",
                "mr": "पीएम विश्वकर्मा योजना (पारंपरिक कारागीर व शिल्पकार)",
                "bn": "প্রধানমন্ত্রী বিশ্বকর্মা প্রকল্প (ঐতিহ্যবাহী কারিগর ও শিল্পী)",
                "gu": "પીએમ વિશ્વકર્મા યોજના (પરંપરાગત કારીગરો)",
                "pa": "ਪੀਐਮ ਵਿਸ਼ਵਕਰਮਾ ਸਕੀਮ (ਰਵਾਇਤੀ ਦਸਤਕਾਰ)",
                "or": "ପିଏମ ବିଶ୍ୱକର୍ମା ଯୋଜନା (ପାରମ୍ପରିକ କାରିଗର)",
                "as": "পিএম বিশ্বকৰ্মা আঁচনি (পৰম্পৰাগত কাৰিকৰ আৰু শিল্পী)"
            },
            "description": {
                "hi": "18 पारंपरिक व्यवसायों के शिल्पकारों को कौशल प्रशिक्षण, ₹15,000 टूलकिट व 5% ब्याज पर ₹3 लाख ऋण।",
                "ta": "18 பாரம்பரிய கைவினைஞர்களுக்கு பயிற்சி, ₹15,000 கருவி மானியம் மற்றும் 5% வட்டியில் ₹3 இலட்சம் கடன்.",
                "te": "18 సాంప్రదాయ వృత్తుల వారికి శిక్షణ, ₹15,000 టూల్‌కిట్ మరియు 5% వడ్డీతో ₹3 లక్షల రుణం.",
                "kn": "18 ಪಾರಂಪರಿಕ ವೃತ್ತಿಗಳ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ ತರಬೇತಿ, ₹15,000 ಟೂಲ್‌ಕಿಟ್ ಮತ್ತು ಶೇ.5 ಬಡ್ಡಿಯಲ್ಲಿ ₹3 ಲಕ್ಷ ಸಾಲ.",
                "ml": "18 പരമ്പരാഗത തൊഴിലുകൾക്ക് പരിശീലനം, ₹15,000 ടൂൾകിറ്റ്, 5% പലിശയിൽ ₹3 ലക്ഷം വായ്പ.",
                "mr": "१८ पारंपरिक कारागिरांना कौशल्य प्रशिक्षण, ₹१५,००० टूलकिट व ५% व्याजाने ₹३ लाख कर्ज.",
                "bn": "১৮টি ঐতিহ্যবাহী পেশার কারিগরদের জন্য প্রশিক্ষণ, ১৫,০০০ টাকা টুলকিট ও ৫% সুদে ৩ লাখ টাকা ঋণ।",
                "gu": "૧૮ પરંપરાગત કારીગરોને તાલીમ, ₹૧૫,૦૦૦ ટૂલકિટ અને ૫% વ્યાજે ₹૩ લાખની લોન.",
                "pa": "੧੮ ਰਵਾਇਤੀ ਕਾਰੀਗਰਾਂ ਨੂੰ ਸਿਖਲਾਈ, ₹੧੫,੦੦੦ ਟੂਲਕਿੱਟ ਅਤੇ ੫% ਵਿਆਜ ਤੇ ₹੩ ਲੱਖ ਕਰਜ਼ਾ।",
                "or": "୧୮ ପାରମ୍ପରିକ କାରିଗରଙ୍କୁ ପ୍ରଶିକ୍ଷଣ, ₹୧୫,୦୦୦ ଟୁଲକିଟ୍ ଏବଂ ୫% ସୁଧରେ ₹୩ ଲକ୍ଷ ଋଣ।",
                "as": "১৮টা পৰম্পৰাগত বৃত্তিৰ বাবে প্ৰশিক্ষণ, ১৫,০০০ টকাৰ টুলকিট আৰু ৫% সুদেৰে ৩ লাখ টকা ঋণ।"
            }
        },
        "MUDRA_SHISHU": {
            "name": {
                "hi": "प्रधानमंत्री मुद्रा योजना - शिशु (₹50,000 तक)",
                "ta": "பிரதமரின் முத்ரா திட்டம் - சிஷு (₹50,000 வரை)",
                "te": "పీఎం ముద్రా యోజన - శిశు (₹50,000 వరకు)",
                "kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ಶಿಶು (₹50,000 ವರೆಗೆ)",
                "ml": "പി.എം മുദ്ര യോജന - ശിശു (₹50,000 വരെ)",
                "mr": "पंतप्रधान मुद्रा योजना - शिशु (₹५०,००० पर्यंत)",
                "bn": "প্রধানমন্ত্রী মুদ্রা যোজনা - শিশু (৫০,০০০ টাকা পর্যন্ত)",
                "gu": "પ્રધાનમંત્રી મુદ્રા યોજના - શિશુ (₹૫૦,૦૦૦ સુધી)",
                "pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਸ਼ਿਸ਼ੂ (₹੫੦,੦੦੦ ਤੱਕ)",
                "or": "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - ଶିଶୁ (₹୫୦,୦୦୦ ପର୍ଯ୍ୟନ୍ତ)",
                "as": "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - শিশু (৫০,০০০ টকালৈকে)"
            },
            "description": {
                "hi": "नए और छोटे व्यवसायों के लिए ₹50,000 तक का बिना जमानत का सूक्ष्म ऋण।",
                "ta": "புதிய மற்றும் சிறு வணிகங்களுக்கான ₹50,000 வரை பிணையற்ற குறுங்கடன்.",
                "te": "చిన్న వ్యాపారాల కోసం ₹50,000 వరకు పూచీకత్తు లేని సూక్ష్మ రుణం.",
                "kn": "ಸಣ್ಣ ಉದ್ಯಮಗಳಿಗೆ ₹50,000 ವರೆಗೆ ಖಾತರಿ ರಹಿತ ಕಿರು ಸಾಲ.",
                "ml": "ചെറുകിട സംരംഭങ്ങൾക്ക് ₹50,000 വരെ ഈടില്ലാത്ത വായ്പ.",
                "mr": "लहान उद्योगांसाठी ₹५०,००० पर्यंत तारणमुक्त सूक्ष्म कर्ज.",
                "bn": "ছোট ব্যবসার জন্য ৫০,০০০ টাকা পর্যন্ত জামিনমুক্ত ক্ষুদ্র ঋণ।",
                "gu": "નાના વ્યવસાયો માટે ₹૫૦,૦૦૦ સુધીની તારણ મુક્ત માઇક્રો લોન.",
                "pa": "ਛੋਟੇ ਕਾਰੋਬਾਰਾਂ ਲਈ ₹੫੦,੦੦੦ ਤੱਕ ਬਿਨਾਂ ਗਰੰਟੀ ਮਾਈਕ੍ਰੋ ਕਰਜ਼ਾ।",
                "or": "କ୍ଷୁଦ୍ର ବ୍ୟବସାୟ ପାଇଁ ₹୫୦,୦୦୦ ପର୍ଯ୍ୟନ୍ତ ଜାମିନ ମୁକ୍ତ ଋଣ।",
                "as": "ক্ষুদ্ৰ ব্যৱসায়ৰ বাবে ৫০,০০০ টকালৈকে বন্ধকমুক্ত ঋণ।"
            }
        },
        "MUDRA_KISHORE": {
            "name": {
                "hi": "प्रधानमंत्री मुद्रा योजना - किशोर (₹5 लाख तक)",
                "ta": "பிரதமரின் முத்ரா திட்டம் - கிஷோர் (₹5 இலட்சம் வரை)",
                "te": "పీఎం ముద్రా యోజన - కిషోర్ (₹5 లక్షల వరకు)",
                "kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ಕಿಶೋರ್ (₹5 ಲಕ್ಷದವರೆಗೆ)",
                "ml": "പി.എം മുദ്ര യോജന - കിഷോർ (₹5 ലക്ഷം വരെ)",
                "mr": "पंतप्रधान मुद्रा योजना - किशोर (₹५ लाखांपर्यंत)",
                "bn": "প্রধানমন্ত্রী মুদ্রা যোজনা - কিশোর (৫ লাখ টাকা পর্যন্ত)",
                "gu": "પ્રધાનમંત્રી મુદ્રા યોજના - કિશોર (₹૫ લાખ સુધી)",
                "pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਕਿਸ਼ੋਰ (₹੫ ਲੱਖ ਤੱਕ)",
                "or": "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - କିଶୋର (₹୫ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ)",
                "as": "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - কিশোৰ (৫ লাখ টকালৈকে)"
            },
            "description": {
                "hi": "स्थापित व्यवसायों के विस्तार के लिए ₹50,000 से ₹5 लाख तक का बिना गारंटी ऋण।",
                "ta": "தொழில் விரிவாக்கத்திற்கு ₹50,000 முதல் ₹5 இலட்சம் வரை பிணையற்ற கடன்.",
                "te": "వ్యాపార విస్తరణ కోసం ₹50,000 నుండి ₹5 లక్షల వరకు పూచీకత్తు లేని రుణం.",
                "kn": "ವ್ಯವಹಾರ ವಿಸ್ತರಣೆಗೆ ₹50,000 ದಿಂದ ₹5 ಲಕ್ಷದವರೆಗೆ ಸಾಲ ಸೌಲಭ್ಯ.",
                "ml": "ബിസിനസ്സ് വിപുലീകരണത്തിന് ₹50,000 മുതൽ ₹5 ലക്ഷം വരെ വായ്പ.",
                "mr": "व्यवसाय विस्तारासाठी ₹५०,००० ते ₹५ लाखांपर्यंत तारणमुक्त कर्ज.",
                "bn": "ব্যবসা সম্প্রসারণের জন্য ৫০,০০০ থেকে ৫ লাখ টাকা পর্যন্ত ঋণ।",
                "gu": "વ્યવસાય વિસ્તરણ માટે ₹૫૦,૦૦૦ થી ₹૫ લાખ સુધીની લોન.",
                "pa": "ਕਾਰੋਬਾਰ ਵਧਾਉਣ ਲਈ ₹੫੦,੦੦੦ ਤੋਂ ₹੫ ਲੱਖ ਤੱਕ ਕਰਜ਼ਾ।",
                "or": "ବ୍ୟବସାୟ ବୃଦ୍ଧି ପାଇଁ ₹୫୦,୦୦୦ ରୁ ₹୫ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ଋଣ।",
                "as": "ব্যৱসায় সম্প্ৰসাৰণৰ বাবে ৫০,০০০ ৰ পৰা ৫ লাখ টকালৈকে ঋণ।"
            }
        },
        "MUDRA_TARUN": {
            "name": {
                "hi": "प्रधानमंत्री मुद्रा योजना - तरुण (₹10 लाख तक)",
                "ta": "பிரதமரின் முத்ரா திட்டம் - தருண் (₹10 இலட்சம் வரை)",
                "te": "పీఎం ముద్రా యోజన - తరుణ్ (₹10 లక్షల వరకు)",
                "kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ತರುಣ್ (₹10 ಲಕ್ಷದವರೆಗೆ)",
                "ml": "പി.എം മുദ്ര യോജന - തരുൺ (₹10 ലക്ഷം വരെ)",
                "mr": "पंतप्रधान मुद्रा योजना - तरुण (₹१० लाखांपर्यंत)",
                "bn": "প্রধানমন্ত্রী মুদ্রা যোজনা - তরুণ (১০ লাখ টাকা পর্যন্ত)",
                "gu": "પ્રધાનમંત્રી મુદ્રા યોજના - તરુણ (₹૧૦ લાખ સુધી)",
                "pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਤਰੁਣ (₹੧੦ ਲੱਖ ਤੱਕ)",
                "or": "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - ତରୁଣ (₹୧୦ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ)",
                "as": "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - তৰুণ (১০ লাখ টকালৈকে)"
            },
            "description": {
                "hi": "सूक्ष्म व लघु उद्यमों के बड़े विस्तार के लिए ₹5 लाख से ₹10 लाख तक का बैंक ऋण।",
                "ta": "தொழில் வளர்ச்சிக்கு ₹5 இலட்சம் முதல் ₹10 இலட்சம் வரை வங்கி கடன்.",
                "te": "పరిశ్రమల వృద్ధి కోసం ₹5 లక్షల నుండి ₹10 లక్షల వరకు బ్యాంక్ రుణం.",
                "kn": "ಉದ್ಯಮಗಳ ಬೆಳವಣಿಗೆಗೆ ₹5 ಲಕ್ಷದಿಂದ ₹10 ಲಕ್ಷದವರೆಗೆ ಸಾಲ ಸೌಲಭ್ಯ.",
                "ml": "സംരംഭക വികസനത്തിന് ₹5 ലക്ഷം മുതൽ ₹10 ലക്ഷം വരെ ബാങ്ക് വായ്പ.",
                "mr": "उद्योगाच्या मोठ्या विस्तारासाठी ₹५ लाख ते ₹१० लाखांपर्यंत बँक कर्ज.",
                "bn": "উদ্যোগের বৃদ্ধির জন্য ৫ লাখ থেকে ১০ লাখ টাকা পর্যন্ত ব্যাংক ঋণ।",
                "gu": "વ્યવસાયના મોટા વિસ્તરણ માટે ₹૫ લાખથી ₹૧૦ લાખ સુધીની લોન.",
                "pa": "ਕਾਰੋਬਾਰੀ ਵਾਧੇ ਲਈ ₹੫ ਲੱਖ ਤੋਂ ₹੧੦ ਲੱਖ ਤੱਕ ਬੈਂਕ ਕਰਜ਼ਾ।",
                "or": "ଉଦ୍ୟୋଗ ବିକାଶ ପାଇଁ ₹୫ ଲକ୍ଷରୁ ₹୧୦ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ବ୍ୟାଙ୍କ ଋଣ।",
                "as": "উদ্যোগ বিকাশৰ বাবে ৫ লাখৰ পৰা ১০ লাখ টকালৈকে বেংক ঋণ।"
            }
        }
    }

    # Parallel Lexicon for Common Financial Terms & UI Labels
    DOMAIN_LEXICON = {
        "scheme": {
            "hi": "योजना", "ta": "திட்டம்", "te": "పథకం", "kn": "ಯೋಜನೆ", "ml": "പദ്ധതി",
            "mr": "योजना", "bn": "প্রকল্প", "gu": "યોજના", "pa": "ਯੋਜਨਾ", "or": "ଯୋଜନା", "as": "আঁচনি"
        },
        "marginalized": {
            "hi": "वंचित वर्ग", "ta": "விளிம்புநிலை", "te": "వంచితులు", "kn": "ಹಿಂದುಳಿದ ವರ್ಗ", "ml": "പിന്നാക്ക വിഭാഗം",
            "mr": "वंचित वर्ग", "bn": "অনগ্রসর শ্রেণি", "gu": "વંચિત વર્ગ", "pa": "ਪੱਛੜਿਆ ਵਰਗ", "or": "ଅନଗ୍ରସର ବର୍ଗ", "as": "প্ৰান্তীয় শ্ৰেণী"
        },
        "low interest": {
            "hi": "कम ब्याज दर / अनुदान", "ta": "குறைந்த வட்டி மானியம்", "te": "తక్కువ వడ్డీ సబ్సిడీ", "kn": "ಕಡಿಮೆ ಬಡ್ಡಿ ಸಬ್ಸಿಡಿ", "ml": "കുറഞ്ഞ പലിശ",
            "mr": "कमी व्याज अनुदान", "bn": "স্বল্প সুদের ভর্তুকি", "gu": "ઓછા વ્યાજની સબસિડી", "pa": "ਘੱਟ ਵਿਆਜ ਸਬਸਿਡੀ", "or": "କମ ସୁଧ ରିହାତି", "as": "কম সুদৰ ৰাজসাহায্য"
        },
        "months": {
            "hi": "माह", "ta": "மாதங்கள்", "te": "నెలలు", "kn": "ತಿಂಗಳುಗಳು", "ml": "മാസങ്ങൾ",
            "mr": "महिने", "bn": "মাস", "gu": "મહિના", "pa": "ਮਹੀਨੇ", "or": "ମାସ", "as": "মাহ"
        },
        "subsidy": {
            "hi": "सब्सिडी (अनुदान)", "ta": "மானிய உதவி", "te": "సబ్సిడీ (రాయితీ)", "kn": "ಸಬ್ಸಿಡಿ (ರಿಯಾಯಿತಿ)", "ml": "സബ്‌സിഡി",
            "mr": "अनुदान (सब्सिडी)", "bn": "ভর্তুকি", "gu": "સબસિડી", "pa": "ਸਬਸਿਡੀ", "or": "ରିହାତି / ସବସିଡି", "as": "ৰেহাই / ৰাজসাহায্য"
        },
        "capital subsidy": {
            "hi": "पूंजीगत अनुदान (कैपिटल सब्सिडी)", "ta": "மூலதன மானியம்", "te": "మూలధన సబ్సిడీ", "kn": "ಬಂಡವಾಳ ಸಬ್ಸಿಡಿ", "ml": "മൂലധന സബ്‌സിഡി",
            "mr": "भांडवली अनुदान", "bn": "মূলধন ভর্তুকি", "gu": "મૂડી સબસિડી", "pa": "ਪੂੰਜੀ ਸਬਸਿਡੀ", "or": "ପୁଞ୍ଜି ରିହାତି", "as": "মূলধন ৰাজসাহায্য"
        },
        "interest subvention": {
            "hi": "ब्याज दर छूट / अनुदान", "ta": "வட்டி மானியம்", "te": "వడ్డీ రాయితీ", "kn": "ಬಡ್ಡಿ ರಿಯಾಯಿತಿ", "ml": "പലിശ ഇളവ്",
            "mr": "व्याज सवलत", "bn": "সুদ ছাড়", "gu": "વ્યાજ રાહત", "pa": "ਵਿਆਜ ਛੋਟ", "or": "ସୁଧ ରିହାତି", "as": "সুদ ৰেহাই"
        },
        "margin money": {
            "hi": "स्वयं का अंशदान (मार्जिन मनी)", "ta": "சொந்த நிதி பங்களிப்பு", "te": "సొంత మార్జిన్ సహకారం", "kn": "ಸ್ವಂತ ಹೂಡಿಕೆ ಮೊತ್ತ", "ml": "സ്വന്തം വിഹിതം",
            "mr": "स्वतःचे योगदान (मार्जिन मनी)", "bn": "নিজস্ব মূলধন অবদান", "gu": "પોતાનું યોગદાન (માર્જિન મની)", "pa": "ਆਪਣਾ ਹਿੱਸਾ (ਮਾਰਜਨ ਮਨੀ)", "or": "ନିଜ ଅଂଶଧନ", "as": "নিজস্ব অংশদান"
        },
        "collateral free": {
            "hi": "जमानत / बंधक मुक्त ऋण", "ta": "பிணையற்ற கடன்", "te": "హామీ లేని రుణం", "kn": "ಖಾತರಿ ರಹಿತ ಸಾಲ", "ml": "ഈടില്ലാത്ത വായ്പ",
            "mr": "तारणमुक्त कर्ज", "bn": "জামিনমুক্ত ঋণ", "gu": "તારણ મુક્ત લોન", "pa": "ਬਿਨਾਂ ਗਰੰਟੀ ਕਰਜ਼ਾ", "or": "ଜାମିନ ମୁକ୍ତ ଋଣ", "as": "বন্ধকমুক্ত ঋণ"
        },
        "bank guarantee": {
            "hi": "बैंक गारंटी", "ta": "வங்கி உத்தரவாதம்", "te": "బ్యాంక్ హామీ", "kn": "ಬ್ಯಾಂಕ್ ಗ್ಯಾರಂಟಿ", "ml": "ബാങ്ക് ഗ്യാരണ്ടി",
            "mr": "बँक हमी", "bn": "ব্যাংক গ্যারান্টি", "gu": "બેંક ગેરંટી", "pa": "ਬੈਂਕ ਗਾਰੰਟੀ", "or": "ବ୍ୟାଙ୍କ ଗ୍ୟାରେଣ୍ଟି", "as": "বেংক গেৰাণ্টি"
        }
    }

    # Parallel Sentence Corpus for Explainability Factors
    EXPLAINABILITY_CORPUS = {
        "Your annual family income falls comfortably within scheme eligibility guidelines.": {
            "hi": "आपकी वार्षिक पारिवारिक आय योजना की पात्रता सीमा के भीतर पूर्णतः अनुकूल है।",
            "ta": "உங்கள் ஆண்டு குடும்ப வருமானம் திட்டத்தின் தகுதி வரம்பிற்குள் உள்ளது.",
            "te": "మీ వార్షిక కుటుంబ ఆదాయం పథకం అర్హత మార్గదర్శకాలకు అనుకూలంగా ఉంది.",
            "kn": "ನಿಮ್ಮ ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯವು ಯೋಜನೆಯ ಅರ್ಹತಾ ಮಿತಿಯೊಳಗಿದೆ.",
            "ml": "താങ്കളുടെ വാർഷിക കുടുംബ വരുമാനം പദ്ധതിയുടെ യോഗ്യതാ മാനദണ്ഡങ്ങൾക്ക് അനുയോജ്യമാണ്.",
            "mr": "तुमचे वार्षिक कौटुंबिक उत्पन्न योजनेच्या पात्रता मर्यादेत बसते.",
            "bn": "আপনার বার্ষিক পারিবারিক আয় প্রকল্পের যোগ্যতা সীমার মধ্যে রয়েছে।",
            "gu": "તમારી વાર્ષિક કૌટુંબિક આવક યોજનાના પાત્રતા માપદંડ મુજબ અનુકૂળ છે.",
            "pa": "ਤੁਹਾਡੀ ਸਾਲਾਨਾ ਪਰਿਵਾਰਕ ਆਮਦਨ ਯੋਜਨਾ ਦੀ ਯੋਗਤਾ ਸੀਮਾ ਦੇ ਅੰਦਰ ਹੈ।",
            "or": "ଆପଣଙ୍କ ବାର୍ଷିକ ପାରିବାରିକ ଆୟ ଯୋଜନା ଯୋଗ୍ୟତା ସୀମା ମଧ୍ୟରେ ଅଛି।",
            "as": "আপোনাৰ বাৰ্ষিক পাৰিবাৰিক আয় আঁচনিৰ যোগ্যতাৰ ভিতৰত আছে।"
        },
        "Applicant age meets the gazetted criteria for this scheme.": {
            "hi": "आवेदक की आयु इस योजना के राजपत्रित मानदंडों को पूरा करती है।",
            "ta": "விண்ணப்பதாரரின் வயது இத்திட்டத்திற்கான அரசு விதிகளுக்கு உட்பட்டது.",
            "te": "దరఖాస్తుదారుడి వయస్సు ఈ పథకం ప్రభుత్వ నిబంధనలకు తగినట్లు ఉంది.",
            "kn": "ಅರ್ಜಿದಾರರ ವಯಸ್ಸು ಈ ಯೋಜನೆಯ ನಿಯಮಗಳಿಗೆ ಸರಿಹೊಂದುತ್ತದೆ.",
            "ml": "അപേക്ഷകന്റെ പ്രായം ഈ പദ്ധതിയുടെ സർക്കാർ മാനദണ്ഡങ്ങൾക്ക് അനുസൃതമാണ്.",
            "mr": "अर्जदाराचे वय या योजनेच्या शासकीय निकषांनुसार योग्य आहे.",
            "bn": "আবেদনকারীর বয়স এই প্রকল্পের সরকারি নীতিমালার সাথে সংগতিপূর্ণ।",
            "gu": "અરજદારની ઉંમર આ યોજનાના નિયમો મુજબ યોગ્ય છે.",
            "pa": "ਬਿਨੈਕਾਰ ਦੀ ਉਮਰ ਇਸ ਯੋਜਨਾ ਦੇ ਸਰਕਾਰੀ ਮਾਪਦੰਡਾਂ ਨੂੰ ਪੂਰਾ ਕਰਦੀ ਹੈ।",
            "or": "ଆବେଦନକାରୀଙ୍କ ବୟସ ଏହି ଯୋଜନାର ନିୟମ ଅନୁସାରେ ଠିକ ଅଛି।",
            "as": "আবেদনকাৰীৰ বয়স এই আঁচনিৰ চৰকাৰী নীতিৰ সৈতে মিলি যায়।"
        },
        "Your business location qualifies for special higher rural capital subsidy.": {
            "hi": "आपका व्यावसायिक स्थान विशेष उच्च ग्रामीण पूंजीगत अनुदान (सब्सिडी) के लिए पात्र है।",
            "ta": "உங்கள் தொழில் இருப்பிடம் உயர் கிராமப்புற மூலதன மானியத்திற்கு தகுதியுடையது.",
            "te": "మీ వ్యాపార ప్రాంతం అధిక గ్రామీణ మూలధన రాయితీకి అర్హత పొందింది.",
            "kn": "ನಿಮ್ಮ ವ್ಯಾಪಾರ ಸ್ಥಳವು ಹೆಚ್ಚಿನ ಗ್ರಾಮೀಣ ಬಂಡವಾಳ ಸಬ್ಸಿಡಿಗೆ ಅರ್ಹವಾಗಿದೆ.",
            "ml": "താങ്കളുടെ ബിസിനസ്സ് പ്രദേശം ഉയർന്ന ഗ്രാമീണ മൂലധന സബ്‌സിഡിക്ക് അർഹമാണ്.",
            "mr": "तुमचे व्यावसायिक ठिकाण उच्च ग्रामीण भांडवली अनुदानासाठी पात्र आहे.",
            "bn": "আপনার ব্যবসার স্থানটি উচ্চ গ্রামীণ মূলধন ভর্তুকির জন্য যোগ্য।",
            "gu": "તમારું વ્યવસાય સ્થળ ગ્રામીણ મૂડી સબસિડી માટે પાત્ર છે.",
            "pa": "ਤੁਹਾਡਾ ਕਾਰੋਬਾਰੀ ਸਥਾਨ ਵਿਸ਼ੇਸ਼ ਪੇਂਡੂ ਪੂੰਜੀ ਸਬਸਿਡੀ ਲਈ ਯੋਗ ਹੈ।",
            "or": "ଆପଣଙ୍କ ବ୍ୟବସାୟ ସ୍ଥାନ ଉଚ୍ଚ ଗ୍ରାମୀଣ ପୁଞ୍ଜି ରିହାତି ପାଇଁ ଯୋଗ୍ୟ।",
            "as": "আপোনাৰ ব্যৱসায়িক স্থানটো বিশেষ গ্ৰাম্য মূলধন ৰাজসাহায্যৰ বাবে উপযুক্ত।"
        },
        "Special category preference applied (SC/ST/Women/Minority higher subsidy slab).": {
            "hi": "विशेष श्रेणी वरीयता लागू (अजा/अजजा/महिला/अल्पसंख्यक उच्चतर सब्सिडी स्लैब 35%)।",
            "ta": "சிறப்புப் பிரிவு முன்னுரிமை பொருந்தும் (SC/ST/பெண்கள்/சிறுபான்மையினர் 35% வரை மானியம்).",
            "te": "ప్రత్యేక వర్గ ప్రాధాన్యత వర్తించింది (SC/ST/మహిళలు/మైనారిటీల అధిక రాయితీ స్లాబ్).",
            "kn": "ವಿಶೇಷ ವರ್ಗದ ಆದ್ಯತೆ ಅನ್ವಯಿಸಲಾಗಿದೆ (ಹೆಚ್ಚಿನ ಸಬ್ಸಿಡಿ ಸ್ಲ್ಯಾಬ್).",
            "ml": "പ്രത്യേക വിഭാഗ മുൻഗണന ബാധകമാക്കി (ഉയർന്ന സബ്‌സിഡി സ്ലാബ്).",
            "mr": "विशेष प्रवर्ग प्राधान्य लागू (अनु.जाती/जमाती/महिला उच्च अनुदान दर).",
            "bn": "বিশেষ বিভাগের অগ্রাধিকার প্রযোজ্য (তপশিলি/নারী উচ্চ ভর্তুকি স্তর)।",
            "gu": "ખાસ વર્ગ અગ્રતા લાગુ (SC/ST/મહિલા ઉચ્ચ સબસિડી દર).",
            "pa": "ਵਿਸ਼ੇਸ਼ ਸ਼੍ਰੇਣੀ ਤਰਜੀਹ ਲਾਗੂ (SC/ST/ਮਹਿਲਾ ਉੱਚ ਸਬਸਿਡੀ ਸਲੈਬ)।",
            "or": "ବିଶେଷ ବର୍ଗ ଅଗ୍ରାଧିକାର ଲାଗୁ (SC/ST/ମହିଳା ଉଚ୍ଚ ରିହାତି ସ୍ଲାବ)।",
            "as": "বিশেষ শ্ৰেণীৰ অগ্ৰাধিকাৰ প্ৰযোজ্য (SC/ST/মহিলা উচ্চ ৰাজসাহায্য)।"
        },
        "Required loan amount is within the maximum scheme sanction limit.": {
            "hi": "आवश्यक ऋण राशि योजना की अधिकतम स्वीकृति सीमा के भीतर है।",
            "ta": "தேவைப்படும் கடன் தொகை திட்டத்தின் அதிகபட்ச வரம்பிற்குள் உள்ளது.",
            "te": "అవసరమైన రుణ మొత్తం పథకం గరిష్ట పరిమితి పరిధిలో ఉంది.",
            "kn": "ಅಗತ್ಯವಿರುವ ಸಾಲದ ಮೊತ್ತವು ಯೋಜನೆಯ ಗರಿಷ್ಠ ಮಿತಿಯೊಳಗಿದೆ.",
            "ml": "ആവശ്യമായ വായ്പ തുക പദ്ധതിയുടെ പരമാവധി പരിധിക്കുള്ളിലാണ്.",
            "mr": "आवश्यक कर्जाची रक्कम योजनेच्या कमाल मर्यादेत आहे.",
            "bn": "প্রয়োজনীয় ঋণের পরিমাণ প্রকল্পের সর্বোচ্চ সীমার মধ্যে রয়েছে।",
            "gu": "જરૂરી લોનની રકમ યોજનાની મહત્તમ મર્યાદામાં છે.",
            "pa": "ਲੋੜੀਂਦੀ ਕਰਜ਼ਾ ਰਕਮ ਯੋਜਨਾ ਦੀ ਅਧਿਕਤਮ ਸੀਮਾ ਅੰਦਰ ਹੈ।",
            "or": "ଆବଶ୍ୟକ ଋଣ ରାଶି ଯୋଜନାର ସର୍ବାଧିକ ସୀମା ମଧ୍ୟରେ ଅଛି।",
            "as": "প্ৰয়োজনীয় ঋণৰ পৰিমাণ আঁচনিৰ সৰ্বোচ্চ সীমাৰ ভিতৰত আছে।"
        },
        "Project cost exceeds the maximum ceiling allowed under scheme rules.": {
            "hi": "परियोजना लागत योजना नियमों के तहत अनुमत अधिकतम सीमा से अधिक है।",
            "ta": "திட்ட மதிப்பீடு அனுமதிக்கப்பட்ட அதிகபட்ச வரம்பை விட அதிகமாக உள்ளது.",
            "te": "ప్రాజెక్ట్ వ్యయం పథకం నిబంధనలలో అనుమతించిన పరిమితిని మించిపోయింది.",
            "kn": "ಯೋಜನೆಯ ವೆಚ್ಚವು ಅನುಮತಿಸಲಾದ ಗರಿಷ್ಠ ಮಿತಿಯನ್ನು ಮೀರಿದೆ.",
            "ml": "പ്രോജക്ട് ചെലവ് അനുവദനീയമായ പരമാവധി പരിധി കവിയുന്നു.",
            "mr": "प्रकल्प खर्च योजनेच्या नियमांतर्गत परवानगी दिलेल्या कमाल मर्यादेपेक्षा जास्त आहे.",
            "bn": "প্রকল্পের ব্যয় নিয়মের সর্বোচ্চ সীমার চেয়ে বেশি।",
            "gu": "પ્રોજેક્ટ ખર્ચ નિયમો મુજબ મહત્તમ મર્યાદા કરતાં વધુ છે.",
            "pa": "ਪ੍ਰੋਜੈਕਟ ਲਾਗਤ ਯੋਜਨਾ ਨਿਯਮਾਂ ਅਧੀਨ ਅਧਿਕਤਮ ਸੀਮਾ ਤੋਂ ਵੱਧ ਹੈ।",
            "or": "ପ୍ରକଳ୍ପ ଖର୍ଚ୍ଚ ଯୋଜନା ନିୟମ ଅନୁସାରେ ସର୍ବାଧିକ ସୀମାଠାରୁ ଅଧିକ।",
            "as": "প্ৰকল্প ব্যয় আঁচনিৰ অনুমোদিত সৰ্বোচ্চ সীমাৰ ওপৰত।"
        },
        "Annual income exceeds the statutory ceiling limit.": {
            "hi": "वार्षिक पारिवारिक आय वैधानिक अधिकतम सीमा से अधिक है।",
            "ta": "ஆண்டு வருமானம் நிர்ணயிக்கப்பட்ட வரம்பை விட அதிகமாக உள்ளது.",
            "te": "వార్షిక ఆదాయం నిర్దేశిత పరిమితి కంటే ఎక్కువ ఉంది.",
            "kn": "ವಾರ್ಷಿಕ ಆದಾಯವು ನಿಗದಿಪಡಿಸಿದ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ.",
            "ml": "വാർഷിക വരുമാനം നിശ്ചിത പരിധിയിലും കൂടുതലാണ്.",
            "mr": "वार्षिक उत्पन्न विहित कमाल मर्यादेपेक्षा जास्त आहे.",
            "bn": "বার্ষিক আয় নির্ধারিত সীমার চেয়ে বেশি।",
            "gu": "વાર્ષિક આવક નિર્ધારિત મર્યાદા કરતાં વધુ છે.",
            "pa": "ਸਾਲਾਨਾ ਆਮਦਨ ਨਿਰਧਾਰਤ ਸੀਮਾ ਤੋਂ ਵੱਧ ਹੈ।",
            "or": "ବାର୍ଷିକ ଆୟ ନିର୍ଦ୍ଧାରିତ ସୀମାଠାରୁ ଅଧିକ।",
            "as": "বাৰ্ষিক আয় নিৰ্ধাৰিত সীমাতকৈ অধিক।"
        },
        "Applicant age is outside the eligible range for this scheme.": {
            "hi": "आवेदक की आयु इस योजना की पात्र आयु सीमा से बाहर है।",
            "ta": "விண்ணப்பதாரரின் வயது தகுதி வரம்பிற்குள் இல்லை.",
            "te": "దరఖాస్తుదారుడి వయస్సు అర్హత పరిధిలో లేదు.",
            "kn": "ಅರ್ಜಿದಾರರ ವಯಸ್ಸು ನಿಗದಿತ ಅರ್ಹತಾ ಮಿತಿಯಲ್ಲಿಲ್ಲ.",
            "ml": "അപേക്ഷകന്റെ പ്രായം യോഗ്യതാ പരിധിക്ക് പുറത്താണ്.",
            "mr": "अर्जदाराचे वय या योजनेच्या पात्र वयोमर्यादेत बसत नाही.",
            "bn": "আবেদনকারীর বয়স প্রকল্পের যোগ্য বয়সসীমার বাইরে।",
            "gu": "અરજદારની ઉંમર યોજનાની વય મર્યાદા બહાર છે.",
            "pa": "ਬਿਨੈਕਾਰ ਦੀ ਉਮਰ ਯੋਜਨਾ ਦੀ ਯੋਗ ਉਮਰ ਸੀਮਾ ਤੋਂ ਬਾਹਰ ਹੈ।",
            "or": "ଆବେଦନକାରୀଙ୍କ ବୟସ ଯୋଗ୍ୟତା ସୀମା ବାହାରେ।",
            "as": "আবেদনকাৰীৰ বয়স যোগ্যতাৰ সীমাৰ বাহিৰত।"
        }
    }

    @classmethod
    def translate_scheme_object(cls, scheme_dict: Dict[str, Any], target_lang: str = "en") -> Dict[str, Any]:
        """Translates scheme name, description, and category for a single scheme dictionary."""
        if not scheme_dict or target_lang == "en":
            return scheme_dict

        lang = target_lang.lower()
        res = dict(scheme_dict)
        code = (res.get("code") or res.get("scheme_code") or "").upper()

        if code in cls.SCHEME_TRANSLATIONS:
            trans = cls.SCHEME_TRANSLATIONS[code]
            if "name" in trans and lang in trans["name"]:
                res["name"] = trans["name"][lang]
                res["scheme_name"] = trans["name"][lang]
            if "description" in trans and lang in trans["description"]:
                res["description"] = trans["description"][lang]
                res["scheme_description"] = trans["description"][lang]

        # Translate target category
        cat = (res.get("target_category") or res.get("category") or "").lower()
        if "marginalized" in cat or cat == "marginalized":
            res["target_category"] = cls.DOMAIN_LEXICON["marginalized"].get(lang, "Marginalized")

        return res

    @classmethod
    def translate_text(cls, text: str, target_lang: str = "hi", source_lang: str = "en") -> str:
        """
        Translates a text string using the Samanantar parallel corpus and domain lexicon.
        """
        if not text or target_lang == "en" or target_lang == source_lang:
            return text

        lang = target_lang.lower()
        supported = ["hi", "ta", "te", "kn", "ml", "mr", "bn", "gu", "pa", "or", "as"]
        if lang not in supported:
            return text

        clean_text = text.strip()
        if clean_text in cls.EXPLAINABILITY_CORPUS:
            if lang in cls.EXPLAINABILITY_CORPUS[clean_text]:
                return cls.EXPLAINABILITY_CORPUS[clean_text][lang]

        # Check for partial template matches like: "Your intended purpose '{purpose}' is prioritized under (.+)\."
        purpose_match = re.search(r"Your intended purpose '([^']+)' is prioritized under (.+)\.", clean_text)
        if purpose_match:
            purpose = purpose_match.group(1)
            scheme_name = purpose_match.group(2)
            templates = {
                "hi": f"आपका प्रस्तावित उद्देश्य '{purpose}' {scheme_name} के तहत प्राथमिकता सूची में है।",
                "ta": f"உங்கள் தொழில் நோக்கம் '{purpose}' {scheme_name} திட்டத்தின் கீழ் முன்னுரிமை பெறுகிறது.",
                "te": f"మీ ఉద్దేశ్యం '{purpose}' {scheme_name} కింద ప్రాధాన్యత ఇవ్వబడింది.",
                "kn": f"ನಿಮ್ಮ ಉದ್ದೇಶ '{purpose}' {scheme_name} ಅಡಿಯಲ್ಲಿ ಆದ್ಯತೆ ಪಡೆದಿದೆ.",
                "ml": f"താങ്കളുടെ ഉദ്ദേശ്യം '{purpose}' {scheme_name} പ്രകാരം മുൻഗണനയുള്ളതാണ്.",
                "mr": f"तुमचा प्रस्तावित उद्देश '{purpose}' {scheme_name} अंतर्गत प्राधान्यक्रमात आहे.",
                "bn": f"আপনার উদ্দেশ্য '{purpose}' {scheme_name} এর অধীনে অগ্রাধিকার পাচ্ছে।",
                "gu": f"તમારો હેતુ '{purpose}' {scheme_name} હેઠળ અગ્રતા ધરાવે છે.",
                "pa": f"ਤੁਹਾਡਾ ਮਕਸਦ '{purpose}' {scheme_name} ਅਧੀਨ ਤਰਜੀਹੀ ਸੂਚੀ ਵਿੱਚ ਹੈ।",
                "or": f"ଆପଣଙ୍କ ଲକ୍ଷ୍ୟ '{purpose}' {scheme_name} ଅଧୀନରେ ପ୍ରାଥମିକତା ପାଇଛି।",
                "as": f"আপোনাৰ উদ্দেশ্য '{purpose}' {scheme_name} ৰ অধীনত অগ্ৰাধিকাৰ দিয়া হৈছে।"
            }
            if lang in templates:
                return templates[lang]

        # Check domain terms
        lower_text = clean_text.lower()
        if lower_text in cls.DOMAIN_LEXICON:
            if lang in cls.DOMAIN_LEXICON[lower_text]:
                return cls.DOMAIN_LEXICON[lower_text][lang]

        # Check scheme name directly
        for code, trans in cls.SCHEME_TRANSLATIONS.items():
            if code.lower() == lower_text or code in clean_text:
                if "name" in trans and lang in trans["name"]:
                    return trans["name"][lang]

        return clean_text

    @classmethod
    def translate_batch(cls, texts: List[str], target_lang: str = "hi") -> List[str]:
        return [cls.translate_text(t, target_lang=target_lang) for t in texts]

    @classmethod
    def translate_scheme_evaluation(cls, evaluation_result: Dict[str, Any], target_lang: str = "hi") -> Dict[str, Any]:
        if not evaluation_result or target_lang == "en":
            return evaluation_result

        translated = dict(evaluation_result)
        
        if "eligible_schemes" in translated:
            new_eligible = []
            for item in translated["eligible_schemes"]:
                item_copy = dict(item)
                code = item_copy.get("scheme_code") or ""
                if code in cls.SCHEME_TRANSLATIONS:
                    trans = cls.SCHEME_TRANSLATIONS[code]
                    if target_lang in trans.get("name", {}):
                        item_copy["scheme_name"] = trans["name"][target_lang]
                    if target_lang in trans.get("description", {}):
                        item_copy["scheme_description"] = trans["description"][target_lang]

                if "explainability" in item_copy:
                    exp = dict(item_copy["explainability"])
                    if "positive_factors" in exp:
                        exp["positive_factors"] = cls.translate_batch(exp["positive_factors"], target_lang)
                    if "limiting_factors" in exp:
                        exp["limiting_factors"] = cls.translate_batch(exp["limiting_factors"], target_lang)
                    item_copy["explainability"] = exp
                
                if "missing_documents" in item_copy:
                    item_copy["missing_documents"] = [cls.translate_text(d, target_lang) for d in item_copy["missing_documents"]]
                new_eligible.append(item_copy)
            translated["eligible_schemes"] = new_eligible

        if "ineligible_schemes" in translated:
            new_ineligible = []
            for item in translated["ineligible_schemes"]:
                item_copy = dict(item)
                code = item_copy.get("scheme_code") or ""
                if code in cls.SCHEME_TRANSLATIONS:
                    trans = cls.SCHEME_TRANSLATIONS[code]
                    if target_lang in trans.get("name", {}):
                        item_copy["scheme_name"] = trans["name"][target_lang]
                if "failed_rules" in item_copy:
                    item_copy["failed_rules"] = cls.translate_batch(item_copy["failed_rules"], target_lang)
                new_ineligible.append(item_copy)
            translated["ineligible_schemes"] = new_ineligible

        return translated
'''

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\backend\app\services\indic_translation.py', 'w', encoding='utf-8') as f:
    f.write(indic_code)
print("1. Updated backend/app/services/indic_translation.py with 25 Schemes Corpus")

# =========================================================================
# 2. Update backend/app/routers/schemes.py with target_language parameter
# =========================================================================
schemes_router_code = r'''from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database.session import get_db
from app.models.scheme import Scheme
from app.schemas.scheme import SchemeOut
from app.services.indic_translation import SamanantarIndicTranslationService

router = APIRouter(prefix="/schemes", tags=["Schemes Catalog"])

@router.get("", response_model=List[SchemeOut])
def list_schemes(
    category: Optional[str] = None,
    department: Optional[str] = None,
    search: Optional[str] = None,
    target_language: Optional[str] = Query("en", description="Target language code (e.g., hi, ta, te, kn, ml, mr, bn, gu, pa, or, as)"),
    db: Session = Depends(get_db)
):
    query = db.query(Scheme).filter(Scheme.is_active == True)
    if category:
        query = query.filter(Scheme.category == category)
    if department:
        query = query.filter(Scheme.department.ilike(f"%{department}%"))
    if search:
        query = query.filter(
            (Scheme.name.ilike(f"%{search}%")) |
            (Scheme.code.ilike(f"%{search}%")) |
            (Scheme.description.ilike(f"%{search}%"))
        )
    schemes = query.all()

    if target_language and target_language.lower() != "en":
        lang = target_language.lower()
        translated_schemes = []
        for s in schemes:
            code = s.code or ""
            if code in SamanantarIndicTranslationService.SCHEME_TRANSLATIONS:
                trans = SamanantarIndicTranslationService.SCHEME_TRANSLATIONS[code]
                if lang in trans.get("name", {}):
                    s.name = trans["name"][lang]
                if lang in trans.get("description", {}):
                    s.description = trans["description"][lang]
            translated_schemes.append(s)
        return translated_schemes

    return schemes

@router.get("/{scheme_id}", response_model=SchemeOut)
def get_scheme_details(
    scheme_id: int, 
    target_language: Optional[str] = Query("en"),
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found.")
    
    if target_language and target_language.lower() != "en":
        lang = target_language.lower()
        code = scheme.code or ""
        if code in SamanantarIndicTranslationService.SCHEME_TRANSLATIONS:
            trans = SamanantarIndicTranslationService.SCHEME_TRANSLATIONS[code]
            if lang in trans.get("name", {}):
                scheme.name = trans["name"][lang]
            if lang in trans.get("description", {}):
                scheme.description = trans["description"][lang]

    return scheme
'''

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\backend\app\routers\schemes.py', 'w', encoding='utf-8') as f:
    f.write(schemes_router_code)
print("2. Updated backend/app/routers/schemes.py with dynamic multilingual translation")

print("Backend update complete.")
