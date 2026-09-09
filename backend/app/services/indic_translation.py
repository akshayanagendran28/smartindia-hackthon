# -*- coding: utf-8 -*-
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

    DOMAIN_LEXICON = {
        "scheme": {
            "hi": "योजना", "ta": "திட்டம்", "te": "పథకం", "kn": "ಯೋಜನೆ", "ml": "പദ്ധതി",
            "mr": "योजना", "bn": "প্রকল্প", "gu": "યોજના", "pa": "ਯੋਜਨਾ", "or": "ଯୋଜନା", "as": "আঁচনি"
        },
        "government": {
            "hi": "सरकारी / सरकार", "ta": "அரசு", "te": "ప్రభుత్వ", "kn": "ಸರ್ಕಾರಿ", "ml": "സർക്കാർ",
            "mr": "शासकीय / सरकार", "bn": "সরকারি", "gu": "સરકારી", "pa": "ਸਰਕਾਰੀ", "or": "ସରକାରୀ", "as": "চৰকাৰী"
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
        "moratorium period": {
            "hi": "ऋण स्थगन अवधि (मोरेटोरियम)", "ta": "தவணை ஒத்திவைப்பு காலம்", "te": "వాయిదా విరామ కాలం", "kn": "ಸಾಲ ಮರುಪಾವತಿ ವಿನಾಯಿತಿ ಅವಧಿ", "ml": "തിരിച്ചടവ് ഇളവ് കാലയളവ്",
            "mr": "हप्ता स्थगिती कालावधी", "bn": "ঋণ স্থগিতের মেয়াদ", "gu": "મોરેટોરિયમ સમયગાળો", "pa": "ਕਿਸ਼ਤ ਮੁਲਤਵੀ ਸਮਾਂ", "or": "ଋଣ ସ୍ଥଗିତ ଅବଧି", "as": "ঋণ ৰেহাই কাল"
        },
        "repayment period": {
            "hi": "पुनर्भुगतान अवधि", "ta": "திருப்பிச் செலுத்தும் காலம்", "te": "మరుసటి చెల్లింపు కాలపరిమితి", "kn": "ಮರುಪಾವತಿ ಅವಧಿ", "ml": "തിരിച്ചടവ് കാലാവധി",
            "mr": "परतफेड कालावधी", "bn": "পরিশোধের মেয়াদ", "gu": "ચૂકવણી સમયગાળો", "pa": "ਮੋੜਨ ਦੀ ਮਿਆਦ", "or": "ପରିଶୋଧ ଅବଧି", "as": "পৰিশোধৰ সময়সীমা"
        },
        "collateral free": {
            "hi": "जमानत / बंधक मुक्त ऋण", "ta": "பிணையற்ற கடன்", "te": "ஹாమీ లేని రుణం", "kn": "ಖಾತರಿ ರಹಿತ ಸಾಲ", "ml": "ഈടില്ലാത്ത വായ്പ",
            "mr": "तारणमुक्त कर्ज", "bn": "জামিনমুক্ত ঋণ", "gu": "તારણ મુક્ત લોન", "pa": "ਬਿਨਾਂ ਗਰੰਟੀ ਕਰਜ਼ਾ", "or": "ଜାମିନ ମୁକ୍ତ ଋଣ", "as": "বন্ধকমুক্ত ঋণ"
        },
        "manufacturing": {
            "hi": "विनिर्माण (मैन्युफैक्चरिंग)", "ta": "உற்பத்தி தொழில்", "te": "ఉత్పాదక రంగం", "kn": "ಉತ್ಪಾದನಾ ವಲಯ", "ml": "ഉൽപ്പാദന മേഖല",
            "mr": "उत्पादन उद्योग", "bn": "উৎপাদন শিল্প", "gu": "ઉત્પાદન ઉદ્યોગ", "pa": "ਨਿਰਮਾਣ ਉਦਯੋਗ", "or": "ଉତ୍ପାଦନ କ୍ଷେତ୍ର", "as": "উৎপাদন খণ্ড"
        },
        "services": {
            "hi": "सेवा क्षेत्र", "ta": "சேவை தொழில்", "te": "సేవా రంగం", "kn": "ಸೇವಾ ವಲಯ", "ml": "സേവന മേഖല",
            "mr": "सेवा क्षेत्र", "bn": "সেবা ক্ষেত্র", "gu": "સેવા ક્ષેત્ર", "pa": "ਸੇਵਾ ਖੇਤਰ", "or": "ସେବା କ୍ଷେତ୍ର", "as": "সেৱা খণ্ড"
        },
        "street vendor": {
            "hi": "रेहड़ी-पटरी / स्ट्रीट वेंडर", "ta": "தெருவோர வியாபாரி", "te": "వీధి వ్యాపారి", "kn": "ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿ", "ml": "തെരുവ് കച്ചവടക്കാരൻ",
            "mr": "फेरीवाले / पथविक्रेते", "bn": "হকার / পথ বিক্রেতা", "gu": "શેરી ફેરિયા", "pa": "ਰੇਹੜੀ-ਫੜ੍ਹੀ ਵਾਲੇ", "or": "ରାସ୍ତାକଡ଼ ବିକ୍ରେତା", "as": "পথ বিক্ৰেতা"
        },
        "traditional artisan": {
            "hi": "पारंपरिक कारीगर व शिल्पकार", "ta": "பாரம்பரிய கைவினைஞர்", "te": "సాంಪ್ರదాయ కళాకారుడు", "kn": "ಸಾಂಪ್ರದಾಯಿಕ ಕುಶಲಕರ್ಮಿ", "ml": "പരമ്പരാഗത കരകൗശല വിദഗ്ദ്ധൻ",
            "mr": "पारंपरिक कारागीर व शिल्पकार", "bn": "ঐতিহ্যবাহী কারিগর", "gu": "પરંપરાગત કારીગર", "pa": "ਰਵਾਇਤੀ ਦਸਤਕਾਰ", "or": "ପାରମ୍ପରିକ କାରିଗର", "as": "পৰম্পৰাগত শিল্পী"
        },
        "special category": {
            "hi": "विशेष श्रेणी (अजा/अजजा/महिला/अल्पसंख्यक)", "ta": "சிறப்புப் பிரிவு (SC/ST/பெண்கள்/சிறுபான்மையினர்)", "te": "ప్రత్యేక వర్గం (SC/ST/మహిళలు/మైనారిటీలు)", "kn": "ವಿಶೇಷ ವರ್ಗ", "ml": "പ്രത്യേക വിഭാഗം",
            "mr": "विशेष प्रवर्ग (अनु.जाती/जमाती/महिला)", "bn": "বিশেষ বিভাগ (তপশিলি/নারী)", "gu": "ખાસ વર્ગ (SC/ST/મહિલા)", "pa": "ਵਿਸ਼ੇਸ਼ ਸ਼੍ਰੇਣੀ (SC/ST/ਮਹਿਲਾ)", "or": "ବିଶେଷ ବର୍ଗ", "as": "বিশেষ শ্ৰেণী"
        },
        "rural area": {
            "hi": "ग्रामीण क्षेत्र", "ta": "கிராமப்புற பகுதி", "te": "గ్రామీణ ప్రాంతం", "kn": "ಗ್ರಾಮೀಣ ಪ್ರದೇಶ", "ml": "ഗ്രാമീണ പ്രദേശം",
            "mr": "ग्रामीण भाग", "bn": "গ্রামীণ এলাকা", "gu": "ગ્રામીણ વિસ્તાર", "pa": "ਪੇਂਡੂ ਖੇਤਰ", "or": "ଗ୍ରାମାଞ୍ଚଳ", "as": "গ্ৰাম্য অঞ্চল"
        },
        "urban area": {
            "hi": "शहरी क्षेत्र", "ta": "நகர்ப்புற பகுதி", "te": "పట్టణ ప్రాంతం", "kn": "ನಗರ ಪ್ರದೇಶ", "ml": "നഗര പ്രദേശം",
            "mr": "शहरी भाग", "bn": "শহরাঞ্চল", "gu": "શહેરી વિસ્તાર", "pa": "ਸ਼ਹਿਰੀ ਖੇਤਰ", "or": "ସହରାଞ୍ଚଳ", "as": "নগৰাঞ্চল"
        },
        "detailed project report": {
            "hi": "विस्तृत परियोजना रिपोर्ट (DPR)", "ta": "விரிவான திட்ட அறிக்கை (DPR)", "te": "వివరణాత్మక ప్రాజెక్ట్ నివేదిక (DPR)", "kn": "ವಿವರವಾದ ಪ್ರಾಜೆಕ್ಟ್ ವರದಿ (ಡಿಪಿಆರ್)", "ml": "വിശദമായ പ്രോജക്ട് റിപ്പോർട്ട് (ഡി.പി.ആർ)",
            "mr": "सविस्तर प्रकल्प अहवाल (DPR)", "bn": "বিস্তারিত প্রকল্প প্রতিবেদন (DPR)", "gu": "વિગતવાર પ્રોજેક્ટ અહેવાલ (DPR)", "pa": "ਵਿਸਥਾਰਤ ਪ੍ਰੋਜੈਕਟ ਰਿਪੋਰਟ (DPR)", "or": "ବିସ୍ତୃତ ପ୍ରକଳ୍ପ ରିପୋର୍ଟ", "as": "বিশদ প্ৰকল্প প্ৰতিবেদন"
        },
        "caste certificate": {
            "hi": "जाति प्रमाण पत्र", "ta": "சாதி சான்றிதழ்", "te": "కులం ధృవీకరణ పత్రం", "kn": "ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ", "ml": "ജാതി സർട്ടിഫിക്കറ്റ്",
            "mr": "जात प्रमाणपत्र", "bn": "জাতি শংসাপত্র", "gu": "જાતિનો દાખલો", "pa": "ਜਾਤੀ ਸਰਟੀਫਿਕੇਟ", "or": "ଜାତି ପ୍ରମାଣପତ୍ର", "as": "জাতিৰ প্ৰমাণপত্ৰ"
        },
        "income certificate": {
            "hi": "आय प्रमाण पत्र", "ta": "வருமான சான்றிதழ்", "te": "ఆదాయ ధృవీకరణ పత్రం", "kn": "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ", "ml": "വരുമാന സർട്ടിഫിക്കറ്റ്",
            "mr": "उत्पन्न दाखला", "bn": "আয় শংসাপত্র", "gu": "આવકનો દાખલો", "pa": "ਆਮਦਨ ਸਰਟੀਫਿਕੇਟ", "or": "ଆୟ ପ୍ରମାଣପତ୍ର", "as": "উপাৰ্জন প্ৰমাণপত্ৰ"
        },
        "bank passbook": {
            "hi": "बैंक पासबुक / विवरण", "ta": "வங்கி பாஸ்புக்", "te": "బ్యాంక్ పాస్‌బుక్", "kn": "ಬ್ಯಾಂಕ್ ಪಾಸ್ ಬುಕ್", "ml": "ബാങ്ക് പാസ്ബുക്ക്",
            "mr": "बँक पासबुक", "bn": "ব্যাংক পাসবই", "gu": "બેંક પાસબુક", "pa": "ਬੈਂਕ ਪਾਸਬੁੱਕ", "or": "ବ୍ୟାଙ୍କ ପାସବୁକ", "as": "বেংক পাছবুক"
        }
    }

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
    def translate_text(cls, text: str, target_lang: str = "hi", source_lang: str = "en") -> str:
        """
        Translates a text string using the Samanantar parallel corpus and domain lexicon.
        Falls back to Qwen Indic prompt if dynamic text is encountered.
        """
        if not text or target_lang == "en" or target_lang == source_lang:
            return text

        lang = target_lang.lower()
        supported = ["hi", "ta", "te", "kn", "ml", "mr", "bn", "gu", "pa", "or", "as"]
        if lang not in supported:
            return text

        # 1. Exact Sentence Match in Samanantar Explainability Corpus
        clean_text = text.strip()
        if clean_text in cls.EXPLAINABILITY_CORPUS:
            if lang in cls.EXPLAINABILITY_CORPUS[clean_text]:
                return cls.EXPLAINABILITY_CORPUS[clean_text][lang]

        # 2. Check for partial template matches like: "Your intended purpose '{purpose}' is prioritized under (.+)\."
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

        # 3. Check for domain terms dictionary
        lower_text = clean_text.lower()
        if lower_text in cls.DOMAIN_LEXICON:
            if lang in cls.DOMAIN_LEXICON[lower_text]:
                return cls.DOMAIN_LEXICON[lower_text][lang]

        # 4. Attempt Qwen Indic Translation if available and reachable
        try:
            qwen_res = cls._translate_with_qwen(clean_text, target_lang=lang)
            if qwen_res:
                return qwen_res
        except Exception:
            pass

        # 5. Return original if no translation found
        return clean_text

    @classmethod
    def _translate_with_qwen(cls, text: str, target_lang: str) -> Optional[str]:
        """Translates dynamic user inputs using Qwen on Ollama with Samanantar guidelines."""
        lang_names = {
            "hi": "Hindi (हिन्दी)",
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
        target_name = lang_names.get(target_lang, "Hindi")
        prompt = f"""Translate the following text accurately into natural, official {target_name} following the AI4Bharat Samanantar Indic standard for Indian government schemes:
English: {text}
{target_name}:"""

        body = {
            "model": settings.OLLAMA_MODEL or "qwen3:4b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 100
            }
        }

        url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            out = data.get("response", "").strip()
            out = re.sub(r"<think>.*?</think>", "", out, flags=re.DOTALL).strip()
            return out if out else None

    @classmethod
    def translate_batch(cls, texts: List[str], target_lang: str = "hi") -> List[str]:
        """Batch translation helper for lists of sentences/factors."""
        return [cls.translate_text(t, target_lang=target_lang) for t in texts]

    @classmethod
    def translate_scheme_evaluation(cls, evaluation_result: Dict[str, Any], target_lang: str = "hi") -> Dict[str, Any]:
        """Translates explainability factors, failed rules, and document lists in a match response."""
        if not evaluation_result or target_lang == "en":
            return evaluation_result

        translated = dict(evaluation_result)
        
        # Translate eligible schemes factors
        if "eligible_schemes" in translated:
            new_eligible = []
            for item in translated["eligible_schemes"]:
                item_copy = dict(item)
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

        # Translate ineligible schemes
        if "ineligible_schemes" in translated:
            new_ineligible = []
            for item in translated["ineligible_schemes"]:
                item_copy = dict(item)
                if "failed_rules" in item_copy:
                    item_copy["failed_rules"] = cls.translate_batch(item_copy["failed_rules"], target_lang)
                new_ineligible.append(item_copy)
            translated["ineligible_schemes"] = new_ineligible

        return translated
