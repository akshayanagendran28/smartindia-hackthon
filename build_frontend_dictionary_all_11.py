# -*- coding: utf-8 -*-
"""
Generate complete 11-Language Samanantar + English UI translations in LanguageContext.jsx (Exhaustive V2)
"""
import os
import json

base_options = {
  "en": {
    "targetMarginalized": "Marginalized", "unitMonths": "Months", "unitLakh": "Lakh", "unitCrore": "Cr",
    "lowInterest": "Low Interest Subsidy", "bankGuarantee": "Bank Guarantee", "specialRural": "Up to 35% Special Rural",
    "sliderMinSVANidhi": "₹10,000 (SVANidhi)", "sliderMidMudra": "₹10 Lakh (Mudra)", "sliderMidPMEGP": "₹50 Lakh (PMEGP)", "sliderMaxStandUp": "₹10 Cr (StandUp)",
    "optionSC": "Scheduled Caste (SC)", "optionST": "Scheduled Tribe (ST)", "optionOBC": "Other Backward Class (OBC)", "optionMinority": "Minority Community", "optionGeneral": "General Category",
    "optionFemale": "Woman / Female", "optionMale": "Male", "optionTransgender": "Transgender",
    "optionGraduate": "Graduate / Degree Holder", "option12th": "12th Standard Pass", "option8th": "8th Standard Pass (PMEGP Eligible for >₹10L)", "optionBelow8th": "Below 8th Standard",
    "optionRural": "Rural (Higher Subsidy up to 35%)", "optionUrban": "Urban (Subsidy up to 25%)",
    "optionNewStage": "New Enterprise (Greenfield Project)", "optionExpansionStage": "Expansion of Existing Unit"
  },
  "hi": {
    "targetMarginalized": "वंचित वर्ग", "unitMonths": "माह", "unitLakh": "लाख", "unitCrore": "करोड़",
    "lowInterest": "कम ब्याज / सब्सिडी", "bankGuarantee": "बैंक गारंटी", "specialRural": "35% तक ग्रामीण सब्सिडी",
    "sliderMinSVANidhi": "₹10,000 (स्वनिधि)", "sliderMidMudra": "₹10 लाख (मुद्रा)", "sliderMidPMEGP": "₹50 लाख (PMEGP)", "sliderMaxStandUp": "₹10 करोड़ (स्टैंड-अप)",
    "optionSC": "अनुसूचित जाति (SC)", "optionST": "अनुसूचित जनजाति (ST)", "optionOBC": "अन्य पिछड़ा वर्ग (OBC)", "optionMinority": "अल्पसंख्यक समुदाय", "optionGeneral": "सामान्य वर्ग (General)",
    "optionFemale": "महिला उद्यमी", "optionMale": "पुरुष", "optionTransgender": "ट्रांसजेंडर (तृतीय लिंग)",
    "optionGraduate": "स्नातक / डिग्री धारक", "option12th": "12वीं पास", "option8th": "8वीं पास (PMEGP पात्र)", "optionBelow8th": "8वीं से कम",
    "optionRural": "ग्रामीण (35% तक उच्च सब्सिडी)", "optionUrban": "शहरी (25% तक सब्सिडी)",
    "optionNewStage": "नया उद्यम (ग्रीनफील्ड)", "optionExpansionStage": "मौजूदा इकाई का विस्तार"
  },
  "ta": {
    "targetMarginalized": "விளிம்புநிலை", "unitMonths": "மாதங்கள்", "unitLakh": "இலட்சம்", "unitCrore": "கோடி",
    "lowInterest": "குறைந்த வட்டி மானியம்", "bankGuarantee": "வங்கி உத்தரவாதம்", "specialRural": "35% வரை கிராமப்புற மானியம்",
    "sliderMinSVANidhi": "₹10,000 (ஸ்வநிதி)", "sliderMidMudra": "₹10 இலட்சம் (முத்ரா)", "sliderMidPMEGP": "₹50 இலட்சம் (PMEGP)", "sliderMaxStandUp": "₹10 கோடி (ஸ்டாண்ட்-அப்)",
    "optionSC": "பட்டியலின சாதி (SC)", "optionST": "பழங்குடியினர் (ST)", "optionOBC": "இதர பிற்படுத்தப்பட்ட வகுப்பு (OBC)", "optionMinority": "சிறுபான்மையினர் சமூகம்", "optionGeneral": "பொதுப் பிரிவு (General)",
    "optionFemale": "பெண் / மகளிர்", "optionMale": "ஆண்", "optionTransgender": "திருநங்கை / திருநம்பி",
    "optionGraduate": "பட்டதாரி / கல்லூரி படிப்பு", "option12th": "12-ஆம் வகுப்பு தேர்ச்சி", "option8th": "8-ஆம் வகுப்பு தேர்ச்சி (PMEGP தகுதி)", "optionBelow8th": "8-ஆம் வகுப்பிற்கு கீழ்",
    "optionRural": "கிராமப்புறம் (35% வரை மானியம்)", "optionUrban": "நகர்ப்புறம் (25% வரை மானியம்)",
    "optionNewStage": "புதிய தொழில் (Greenfield)", "optionExpansionStage": "தொழில் விரிவாக்கம்"
  },
  "te": {
    "targetMarginalized": "వంచితులు", "unitMonths": "నెలలు", "unitLakh": "లక్షలు", "unitCrore": "కోట్లు",
    "lowInterest": "తక్కువ వడ్డీ సబ్సిడీ", "bankGuarantee": "బ్యాంక్ హామీ", "specialRural": "35% వరకు గ్రామీణ సబ్సిడీ",
    "sliderMinSVANidhi": "₹10,000 (స్వనిధి)", "sliderMidMudra": "₹10 లక్షలు (ముద్ర)", "sliderMidPMEGP": "₹50 లక్షలు (PMEGP)", "sliderMaxStandUp": "₹10 కోట్లు (స్టాండ్-అప్)",
    "optionSC": "షెడ్యూల్డ్ కులం (SC)", "optionST": "షెడ్యూల్డ్ తెగ (ST)", "optionOBC": "ఇతర వెనుకబడిన తరగతి (OBC)", "optionMinority": "మైనారిటీ వర్గం", "optionGeneral": "జనరల్ వర్గం (General)",
    "optionFemale": "మహిళ", "optionMale": "పురుషుడు", "optionTransgender": "ట్రాన్స్‌జెండర్",
    "optionGraduate": "డిగ్రీ / గ్రాడ్యుయేట్", "option12th": "12వ తరగతి పాస్", "option8th": "8వ తరగతి పాస్ (PMEGP అర్హత)", "optionBelow8th": "8వ తరగతి లోపు",
    "optionRural": "గ్రామీణ (35% వరకు సబ్సిడీ)", "optionUrban": "పట్టణ (25% వరకు సబ్సిడీ)",
    "optionNewStage": "కొత్త వ్యాపారం (Greenfield)", "optionExpansionStage": "వ్యాపార విస్తరణ"
  },
  "kn": {
    "targetMarginalized": "ಹಿಂದುಳಿದ ವರ್ಗ", "unitMonths": "ತಿಂಗಳುಗಳು", "unitLakh": "ಲಕ್ಷ", "unitCrore": "ಕೋಟಿ",
    "lowInterest": "ಕಡಿಮೆ ಬಡ್ಡಿ ಸಬ್ಸಿಡಿ", "bankGuarantee": "ಬ್ಯಾಂಕ್ ಗ್ಯಾರಂಟಿ", "specialRural": "35% ವರೆಗೆ ಗ್ರಾಮೀಣ ಸಬ್ಸಿಡಿ",
    "sliderMinSVANidhi": "₹10,000 (ಸ್ವನಿಧಿ)", "sliderMidMudra": "₹10 ಲಕ್ಷ (ಮುದ್ರಾ)", "sliderMidPMEGP": "₹50 ಲಕ್ಷ (PMEGP)", "sliderMaxStandUp": "₹10 ಕೋಟಿ (ಸ್ಟ್ಯಾಂಡ್‌-ಅಪ್)",
    "optionSC": "ಪರಿಶಿಷ್ಟ ಜಾತಿ (SC)", "optionST": "ಪರಿಶಿಷ್ಟ ಪಂಗಡ (ST)", "optionOBC": "ಇತರ ಹಿಂದುಳಿದ ವರ್ಗ (OBC)", "optionMinority": "ಅಲ್ಪಸಂಖ್ಯಾತ ಸಮುದಾಯ", "optionGeneral": "ಸಾಮಾನ್ಯ ವರ್ಗ (General)",
    "optionFemale": "ಮಹಿಳೆ", "optionMale": "ಪುರುಷ", "optionTransgender": "ತೃತೀಯ ಲಿಂಗಿ",
    "optionGraduate": "ಪದವೀಧರ / ಡಿಗ್ರಿ", "option12th": "12ನೇ ತರಗತಿ ಪಾಸು", "option8th": "8ನೇ ತರಗತಿ ಪಾಸು (PMEGP ಅರ್ಹತೆ)", "optionBelow8th": "8ನೇ ತರಗತಿಗಿಂತ ಕಡಿಮೆ",
    "optionRural": "ಗ್ರಾಮೀಣ (35% ವರೆಗೆ ಸಬ್ಸಿಡಿ)", "optionUrban": "ನಗರ (25% ವರೆಗೆ ಸಬ್ಸಿಡಿ)",
    "optionNewStage": "ಹೊಸ ಉದ್ಯಮ (Greenfield)", "optionExpansionStage": "ಉದ್ಯಮ ವಿಸ್ತರಣೆ"
  },
  "ml": {
    "targetMarginalized": "പിന്നാക്ക വിഭാഗം", "unitMonths": "മാസങ്ങൾ", "unitLakh": "ലക്ഷം", "unitCrore": "കോടി",
    "lowInterest": "കുറഞ്ഞ പലിശ സബ്‌സിഡി", "bankGuarantee": "ബാങ്ക് ഗ്യാരണ്ടി", "specialRural": "35% വരെ ഗ്രാമീണ സബ്‌സിഡി",
    "sliderMinSVANidhi": "₹10,000 (സ്വനിധി)", "sliderMidMudra": "₹10 ലക്ഷം (മുദ്ര)", "sliderMidPMEGP": "₹50 ലക്ഷം (PMEGP)", "sliderMaxStandUp": "₹10 കോടി (സ്റ്റാൻഡ്-അപ്പ്)",
    "optionSC": "പട്ടികജാതി (SC)", "optionST": "പട്ടികവർഗ്ഗം (ST)", "optionOBC": "മറ്റ് പിന്നാക്ക വിഭാഗങ്ങൾ (OBC)", "optionMinority": "ന്യൂനപക്ഷ വിഭാഗം", "optionGeneral": "ജനറൽ വിഭാഗം (General)",
    "optionFemale": "വനിത", "optionMale": "പുരുഷൻ", "optionTransgender": "ട്രാൻസ്‌ജെൻഡർ",
    "optionGraduate": "ബിരുദധാരി", "option12th": "12-ാം ക്ലാസ് പാസ്", "option8th": "8-ാം ക്ലാസ് പാസ് (PMEGP യോഗ്യത)", "optionBelow8th": "8-ാം ക്ലാസിന് താഴെ",
    "optionRural": "ഗ്രാമപ്രദേശം (35% വരെ സബ്‌സിഡി)", "optionUrban": "നഗര പ്രദേശം (25% വരെ സബ്‌സിഡി)",
    "optionNewStage": "പുതിയ സംരംഭം (Greenfield)", "optionExpansionStage": "സംരംഭ വിപുലീകരണം"
  },
  "mr": {
    "targetMarginalized": "वंचित वर्ग", "unitMonths": "महिने", "unitLakh": "लाख", "unitCrore": "कोटी",
    "lowInterest": "कमी व्याज अनुदान", "bankGuarantee": "बँक हमी", "specialRural": "३५% पर्यंत ग्रामीण अनुदान",
    "sliderMinSVANidhi": "₹१०,००० (स्वनिधी)", "sliderMidMudra": "₹१० लाख (मुद्रा)", "sliderMidPMEGP": "₹५० लाख (PMEGP)", "sliderMaxStandUp": "₹१० कोटी (स्टँड-अप)",
    "optionSC": "अनुसूचित जाती (SC)", "optionST": "अनुसूचित जमाती (ST)", "optionOBC": "इतर मागासवर्गीय (OBC)", "optionMinority": "अल्पसंख्याक समुदाय", "optionGeneral": "खुला / सामान्य प्रवर्ग (General)",
    "optionFemale": "महिला उद्योजक", "optionMale": "पुरुष", "optionTransgender": "तृतीयपंथी",
    "optionGraduate": "पदवीधर", "option12th": "१२ वी पास", "option8th": "८ वी पास (PMEGP पात्र)", "optionBelow8th": "८ वी पेक्षा कमी",
    "optionRural": "ग्रामीण (३५% पर्यंत अनुदान)", "optionUrban": "शहरी (२५% पर्यंत अनुदान)",
    "optionNewStage": "नवीन उद्योग (Greenfield)", "optionExpansionStage": "विद्यमान युनिटचा विस्तार"
  },
  "bn": {
    "targetMarginalized": "অনগ্রসর শ্রেণি", "unitMonths": "মাস", "unitLakh": "লাখ", "unitCrore": "কোটি",
    "lowInterest": "স্বল্প সুদের ভর্তুকি", "bankGuarantee": "ব্যাংক গ্যারান্টি", "specialRural": "৩৫% পর্যন্ত গ্রামীণ ভর্তুকি",
    "sliderMinSVANidhi": "₹১০,০০০ (স্বনিধি)", "sliderMidMudra": "₹১০ লাখ (মুদ্রা)", "sliderMidPMEGP": "₹৫০ লাখ (PMEGP)", "sliderMaxStandUp": "₹১০ কোটি (স্ট্যান্ড-আপ)",
    "optionSC": "তফসিলি জাতি (SC)", "optionST": "তফসিলি উপজাতি (ST)", "optionOBC": "অন্যান্য অনগ্রসর শ্রেণি (OBC)", "optionMinority": "সংখ্যালঘু সম্প্রদায়", "optionGeneral": "সাধারণ বিভাগ (General)",
    "optionFemale": "নারী / মহিলা", "optionMale": "পুরুষ", "optionTransgender": "রূপান্তরকামী (Transgender)",
    "optionGraduate": "স্নাতক / ডিগ্রিধারী", "option12th": "দ্বাদশ শ্রেণি পাস", "option8th": "অষ্টম শ্রেণি পাস (PMEGP যোগ্য)", "optionBelow8th": "অষ্টম শ্রেণির নিচে",
    "optionRural": "গ্রামীণ (৩৫% পর্যন্ত ভর্তুকি)", "optionUrban": "শহরাঞ্চল (২৫% পর্যন্ত ভর্তুকি)",
    "optionNewStage": "নতুন উদ্যোগ (Greenfield)", "optionExpansionStage": "বিদ্যমান ইউনিটের সম্প্রসারণ"
  },
  "gu": {
    "targetMarginalized": "વંચિત વર્ગ", "unitMonths": "મહિના", "unitLakh": "લાખ", "unitCrore": "કરોડ",
    "lowInterest": "ઓછા વ્યાજની સબસિડી", "bankGuarantee": "બેંક ગેરંટી", "specialRural": "૩૫% સુધી ગ્રામીણ સબસિડી",
    "sliderMinSVANidhi": "₹૧૦,૦૦૦ (સ્વનિધિ)", "sliderMidMudra": "₹૧૦ લાખ (મુદ્રા)", "sliderMidPMEGP": "₹૫૦ લાખ (PMEGP)", "sliderMaxStandUp": "₹૧૦ કરોડ (સ્ટેન્ડ-અપ)",
    "optionSC": "અનુસૂચિત જાતિ (SC)", "optionST": "અનુસૂચિત જનજાતિ (ST)", "optionOBC": "અન્ય પછાત વર્ગ (OBC)", "optionMinority": "લઘુમતી સમુદાય", "optionGeneral": "સામાન્ય વર્ગ (General)",
    "optionFemale": "મહિલા", "optionMale": "પુરુષ", "optionTransgender": "ટ્રાન્સજેન્ડર",
    "optionGraduate": "સ્નાતક / ડિગ્રીધારક", "option12th": "૧૨ પાસ", "option8th": "૮ પાસ (PMEGP પાત્ર)", "optionBelow8th": "૮ થી ઓછું",
    "optionRural": "ગ્રામીણ (૩૫% સુધી સબસિડી)", "optionUrban": "શહેરી (૨૫% સુધી સબસિડી)",
    "optionNewStage": "નવો વ્યવસાય (Greenfield)", "optionExpansionStage": "હાલના વ્યવસાયનો વિસ્તાર"
  },
  "pa": {
    "targetMarginalized": "ਪੱਛੜਿਆ ਵਰਗ", "unitMonths": "ਮਹੀਨੇ", "unitLakh": "ਲੱਖ", "unitCrore": "ਕਰੋੜ",
    "lowInterest": "ਘੱਟ ਵਿਆਜ ਸਬਸਿਡੀ", "bankGuarantee": "ਬੈਂਕ ਗਾਰੰਟੀ", "specialRural": "੩੫% ਤੱਕ ਪੇਂਡੂ ਸਬਸਿਡੀ",
    "sliderMinSVANidhi": "₹੧੦,੦੦੦ (ਸਵਨਿਧੀ)", "sliderMidMudra": "₹੧੦ ਲੱਖ (ਮੁਦਰਾ)", "sliderMidPMEGP": "₹੫੦ ਲੱਖ (PMEGP)", "sliderMaxStandUp": "₹੧੦ ਕਰੋੜ (ਸਟੈਂਡ-ਅੱਪ)",
    "optionSC": "ਅਨੁਸੂਚਿਤ ਜਾਤੀ (SC)", "optionST": "ਅਨੁਸੂਚਿਤ ਜਨਜਾਤੀ (ST)", "optionOBC": "ਹੋਰ ਪੱਛੜੀਆਂ ਸ਼੍ਰੇਣੀਆਂ (OBC)", "optionMinority": "ਘੱਟ ਗਿਣਤੀ ਭਾਈਚਾਰਾ", "optionGeneral": "ਜਨਰਲ ਸ਼੍ਰੇਣੀ (General)",
    "optionFemale": "ਮਹਿਲਾ", "optionMale": "ਪੁਰਸ਼", "optionTransgender": "ਟਰਾਂਸਜੈਂਡਰ",
    "optionGraduate": "ਗ੍ਰੈਜੂਏਟ / ਡਿਗਰੀ ਧਾਰਕ", "option12th": "੧੨ਵੀਂ ਪਾਸ", "option8th": "੮ਵੀਂ ਪਾਸ (PMEGP ਯੋਗ)", "optionBelow8th": "੮ਵੀਂ ਤੋਂ ਘੱਟ",
    "optionRural": "ਪੇਂਡੂ (੩੫% ਤੱਕ ਸਬਸਿਡੀ)", "optionUrban": "ਸ਼ਹਿਰੀ (੨੫% ਤੱਕ ਸਬਸਿਡੀ)",
    "optionNewStage": "ਨਵਾਂ ਕਾਰੋਬਾਰ (Greenfield)", "optionExpansionStage": "ਕਾਰੋਬਾਰ ਦਾ ਵਾਧਾ"
  },
  "or": {
    "targetMarginalized": "ଅନଗ୍ରସର ବର୍ଗ", "unitMonths": "ମାସ", "unitLakh": "ଲକ୍ଷ", "unitCrore": "କୋଟି",
    "lowInterest": "କମ ସୁଧ ରିହାତି", "bankGuarantee": "ବ୍ୟାଙ୍କ ଗ୍ୟାରେଣ୍ଟି", "specialRural": "୩୫% ପର୍ଯ୍ୟନ୍ତ ଗ୍ରାମୀଣ ରିହାତି",
    "sliderMinSVANidhi": "₹୧୦,୦୦୦ (ସ୍ୱନିଧି)", "sliderMidMudra": "₹୧୦ ଲକ୍ଷ (ମୁଦ୍ରା)", "sliderMidPMEGP": "₹୫୦ ଲକ୍ଷ (PMEGP)", "sliderMaxStandUp": "₹୧୦ କୋଟି (ଷ୍ଟାଣ୍ଡ-ଅପ)",
    "optionSC": "ଅନୁସୂଚିତ ଜାତି (SC)", "optionST": "ଅନୁସୂଚିତ ଜନଜାତି (ST)", "optionOBC": "ଅନ୍ୟାନ୍ୟ ପଛୁଆ ବର୍ଗ (OBC)", "optionMinority": "ସଂଖ୍ୟାଲଘୁ ସମ୍ପ୍ରଦାୟ", "optionGeneral": "ସାଧାରଣ ବର୍ଗ (General)",
    "optionFemale": "ମହିଳା", "optionMale": "ପୁରୁଷ", "optionTransgender": "ତୃତୀୟ ଲିଙ୍ଗ",
    "optionGraduate": "ସ୍ନାତକ / ଡିଗ୍ରୀଧାରୀ", "option12th": "୧୨ଶ ପାସ", "option8th": "୮ମ ପାସ (PMEGP ଯୋଗ୍ୟ)", "optionBelow8th": "୮ମ ଶ୍ରେଣୀରୁ କମ",
    "optionRural": "ଗ୍ରାମାଞ୍ଚଳ (୩୫% ପର୍ଯ୍ୟନ୍ତ ରିହାତି)", "optionUrban": "ସହରାଞ୍ଚଳ (୨୫% ପର୍ଯ୍ୟନ୍ତ ରିହାତି)",
    "optionNewStage": "ନୂତନ ଉଦ୍ୟୋଗ (Greenfield)", "optionExpansionStage": "ବ୍ୟବସାୟ ସମ୍ପ୍ରସାରଣ"
  },
  "as": {
    "targetMarginalized": "প্ৰান্তীয় শ্ৰেণী", "unitMonths": "মাহ", "unitLakh": "লাখ", "unitCrore": "কোটি",
    "lowInterest": "কম সুদৰ ৰাজসাহায্য", "bankGuarantee": "বেংক গেৰাণ্টি", "specialRural": "৩৫% লৈকে গ্ৰাম্য ৰাজসাহায্য",
    "sliderMinSVANidhi": "₹১০,০০০ (স্বনিধি)", "sliderMidMudra": "₹১০ লাখ (মুদ্ৰা)", "sliderMidPMEGP": "₹৫০ লাখ (PMEGP)", "sliderMaxStandUp": "₹১০ কোটি (ষ্টেণ্ড-আপ)",
    "optionSC": "অনুসূচীত জাতি (SC)", "optionST": "অনুসূচীত জনজাতি (ST)", "optionOBC": "অন্যান্য পিছপৰা শ্ৰেণী (OBC)", "optionMinority": "সংখ্যালঘু সম্প্ৰদায়", "optionGeneral": "সাধাৰণ শ্ৰেণী (General)",
    "optionFemale": "মহিলা", "optionMale": "পুৰুষ", "optionTransgender": "ৰূপান্তৰকামী",
    "optionGraduate": "স্নাতক / ডিগ্ৰীধাৰী", "option12th": "দ্বাদশ শ্ৰেণী উত্তীৰ্ণ", "option8th": "অষ্টম শ্ৰেণী উত্তীৰ্ণ (PMEGP যোগ্য)", "optionBelow8th": "অষ্টম শ্ৰেণীৰ তলত",
    "optionRural": "গ্ৰাম্য (৩৫% লৈকে ৰাজসাহায্য)", "optionUrban": "নগৰীয়া (২৫% লৈকে ৰাজসাহায্য)",
    "optionNewStage": "নতুন উদ্যোগ (Greenfield)", "optionExpansionStage": "ব্যৱসায় সম্প্ৰসাৰণ"
  }
}

# Now inject these into the full DICTIONARY in frontend/src/context/LanguageContext.jsx
print("Base options loaded for all 11 Indian languages + English.")
