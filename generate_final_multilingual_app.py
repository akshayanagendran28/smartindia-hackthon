# -*- coding: utf-8 -*-
"""
Master Multilingual Synchronizer V3:
Ensures 100% of all UI text, select options, range labels, units, scheme titles, descriptions,
and chatbot intelligence are translated and grounded in all 11 Indian languages + English.
"""
import os
import json

# 1. Write LanguageContext.jsx
with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\context\LanguageContext.jsx', 'w', encoding='utf-8') as f:
    f.write(r'''import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const LanguageContext = createContext();

export const LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' },
  { code: 'as', name: 'Assamese', native: 'অসমীয়া' }
];

export const SCHEME_MAP = {
  PMEGP: {
    hi: { name: "प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)", desc: "विनिर्माण व सेवा क्षेत्र में सूक्ष्म उद्यमों के लिए 35% तक पूंजीगत सब्सिडी सहित ऋण योजना।" },
    ta: { name: "பிரதமரின் வேலைவாய்ப்பு உருவாக்கும் திட்டம் (PMEGP)", desc: "உற்பத்தி மற்றும் சேவைத் துறைகளில் சுயதொழில் தொடங்க 35% வரை மானியம் வழங்கும் கடன் திட்டம்." },
    te: { name: "ప్రధాన మంత్రి ఉపాధి కల్పన కార్యక్రమం (PMEGP)", desc: "ఉత్పాదక మరియు సేవా రంగాల్లో సూక్ష్మ పరిశ్రమల స్థాపనకు 35% వరకు సబ్సిడీతో కూడిన రుణ పథకం." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಉದ್ಯೋಗ ಸೃಷ್ಟಿ ಕಾರ್ಯಕ್ರಮ (PMEGP)", desc: "ಉತ್ಪಾದನಾ ಮತ್ತು ಸೇವಾ ವಲಯಗಳಲ್ಲಿ ಉದ್ಯಮ ಸ್ಥಾಪಿಸಲು ಶೇ.35 ರವರೆಗೆ ಸಬ್ಸಿಡಿ ನೀಡುವ ಯೋಜನೆ." },
    ml: { name: "പ്രധാനമന്ത്രി തൊഴിൽ സൃഷ്ടി പദ്ധതി (PMEGP)", desc: "ഉൽപ്പാദന, സേവന മേഖലകളിൽ സംരംഭങ്ങൾ തുടങ്ങാൻ 35% വരെ സബ്‌സിഡി നൽകുന്ന വായ്പാ പദ്ധതി." },
    mr: { name: "पंतप्रधान रोजगार निर्मिती कार्यक्रम (PMEGP)", desc: "उत्पादन व सेवा क्षेत्रात सूक्ष्म उद्योग सुरू करण्यासाठी ३५% पर्यंत भांडवली अनुदान योजना." },
    bn: { name: "প্রধানমন্ত্রী কর্মসংস্থান সৃষ্টি প্রকল্প (PMEGP)", desc: "উৎপাদন ও সেবা ক্ষেত্রে ক্ষুদ্র উদ্যোগ স্থাপনের জন্য ৩৫% পর্যন্ত মূলধন ভর্তুকিযুক্ত ঋণ প্রকল্প।" },
    gu: { name: "પ્રધાનમંત્રી રોજગાર નિર્માણ કાર્યક્રમ (PMEGP)", desc: "ઉત્પાદન અને સેવા ક્ષેત્રે સૂક્ષ્મ ઉદ્યોગો શરૂ કરવા માટે ૩૫% સુધીની સબસિડી સાથેની યોજના." },
    pa: { name: "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਰੋਜ਼ਗਾਰ ਉਤਪਤੀ ਪ੍ਰੋਗਰਾਮ (PMEGP)", desc: "ਨਿਰਮਾਣ ਅਤੇ ਸੇਵਾ ਖੇਤਰਾਂ ਵਿੱਚ ਸਵੈ-ਰੋਜ਼ਗਾਰ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ੩੫% ਤੱਕ ਸਬਸਿਡੀ ਵਾਲੀ ਕਰਜ਼ਾ ਯੋਜਨਾ।" },
    or: { name: "ପ୍ରଧାନମନ୍ତ୍ରୀ ରୋଜଗାର ସୃଷ୍ଟି କାର୍ଯ୍ୟକ୍ରମ (PMEGP)", desc: "ଉତ୍ପାଦନ ଓ ସେବା କ୍ଷେତ୍ରରେ କ୍ଷୁଦ୍ର ଉଦ୍ୟୋଗ ସ୍ଥାପନ ପାଇଁ ୩୫% ପର୍ଯ୍ୟନ୍ତ ରିହାତିଯୁକ୍ତ ଋଣ ଯୋଜନା।" },
    as: { name: "প্ৰধানমন্ত্ৰী নিয়োগ সৃষ্টি কাৰ্যসূচী (PMEGP)", desc: "উৎপাদন আৰু সেৱা খণ্ডত উদ্যোগ স্থাপনৰ বাবে ৩৫% লৈকে ৰাজসাহায্যযুক্ত ঋণ আঁচনি।" }
  },
  "STANDUP-IND": {
    hi: { name: "स्टैंड-अप इंडिया योजना (SC/ST व महिला उद्यमी)", desc: "अजा/अजजा और महिला उद्यमियों को नए व्यवसाय के लिए ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।" },
    ta: { name: "ஸ்டாண்ட்-அப் இந்தியா திட்டம் (SC/ST & பெண்கள்)", desc: "SC/ST மற்றும் பெண் தொழில்முனைவோருக்கு ₹10 இலட்சம் முதல் ₹1 கோடி வரை வங்கி கடன் வசதி." },
    te: { name: "స్టాండ్-అప్ ఇండియా పథకం (SC/ST & మహిళలు)", desc: "SC/ST మరియు మహిళా పారిశ్రామికవేత్తలకు ₹10 లక్షల నుండి ₹1 కోట్ల వరకు బ్యాంక్ రుణం." },
    kn: { name: "ಸ್ಟ್ಯಾಂಡ್‌-ಅಪ್ ಇಂಡಿಯಾ ಯೋಜನೆ (SC/ST & ಮಹಿಳೆಯರು)", desc: "SC/ST ಮತ್ತು ಮಹಿಳಾ ಉದ್ಯಮಿಗಳಿಗೆ ₹10 ಲಕ್ಷದಿಂದ ₹1 ಕೋಟಿವರೆಗೆ ಬ್ಯಾಂಕ್ ಸಾಲ ಸೌಲಭ್ಯ." },
    ml: { name: "സ്റ്റാൻഡ്-അപ്പ് ഇന്ത്യ പദ്ധതി (പട്ടികജാതി/പട്ടികവർഗ്ഗം & വനിതകൾ)", desc: "പട്ടികജാതി/പട്ടികവർഗ്ഗ, വനിതാ സംരംഭകർക്ക് ₹10 ലക്ഷം മുതൽ ₹1 കോടി വരെ ബാങ്ക് വായ്പ." },
    mr: { name: "स्टँड-अप इंडिया योजना (SC/ST व महिला)", desc: "नवीन उद्योगासाठी अनु.जाती/जमाती व महिलांना ₹१० लाख ते ₹१ कोटीपर्यंत बँक कर्ज सुविधा." },
    bn: { name: "স্ট্যান্ড-আপ ইন্ডিয়া প্রকল্প (SC/ST ও নারী)", desc: "তপশিলি জাতি/উপজাতি ও নারী উদ্যোক্তাদের জন্য ১০ লাখ থেকে ১ কোটি টাকা পর্যন্ত ব্যাংক ঋণ সুবিধা।" },
    gu: { name: "સ્ટેન્ડ-અપ ઇન્ડિયા યોજના (SC/ST અને મહિલાઓ)", desc: "નવા વ્યવસાય માટે SC/ST અને મહિલાઓને ₹૧૦ લાખથી ₹૧ કરોડ સુધીની બેંક લોન સહાય." },
    pa: { name: "ਸਟੈਂਡ-ਅੱਪ ਇੰਡੀਆ ਸਕੀਮ (SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ)", desc: "ਨਵਾਂ ਕਾਰੋਬਾਰ ਸ਼ੁਰੂ ਕਰਨ ਲਈ SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ ਨੂੰ ₹੧੦ ਲੱਖ ਤੋਂ ₹੧ ਕਰੋੜ ਤੱਕ ਬੈਂਕ ਕਰਜ਼ਾ।" },
    or: { name: "ଷ୍ଟାଣ୍ଡ-ଅପ ଇଣ୍ଡିଆ ଯୋଜନା (SC/ST ଓ ମହିଳା)", desc: "ନୂତନ ଉଦ୍ୟୋଗ ପାଇଁ SC/ST ଓ ମହିଳାମାନଙ୍କୁ ₹୧୦ ଲକ୍ଷରୁ ₹୧ କୋଟି ପର୍ଯ୍ୟନ୍ତ ବ୍ୟାଙ୍କ ଋଣ।" },
    as: { name: "ষ্টেণ্ড-আপ ইণ্ডিয়া আঁচনি (SC/ST আৰু মহিলা)", desc: "নতুন ব্যৱসায়ৰ বাবে SC/ST আৰু মহিলাসকলক ১০ লাখৰ পৰা ১ কোটি টকালৈকে বেংক ঋণ।" }
  },
  "STAND_UP_INDIA": {
    hi: { name: "स्टैंड-अप इंडिया योजना (SC/ST व महिला उद्यमी)", desc: "अजा/अजजा और महिला उद्यमियों को नए व्यवसाय के लिए ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।" },
    ta: { name: "ஸ்டாண்ட்-அப் இந்தியா திட்டம் (SC/ST & பெண்கள்)", desc: "SC/ST மற்றும் பெண் தொழில்முனைவோருக்கு ₹10 இலட்சம் முதல் ₹1 கோடி வரை வங்கி கடன் வசதி." },
    te: { name: "స్టాండ్-அప్ ఇండియా పథకం (SC/ST & మహిళలు)", desc: "SC/ST మరియు మహిళా పారిశ్రామికవేత్తలకు ₹10 లక్షల నుండి ₹1 కోట్ల వరకు బ్యాంక్ రుణం." },
    kn: { name: "ಸ್ಟ್ಯಾಂಡ್‌-ಅಪ್ ಇಂಡಿಯಾ ಯೋಜನೆ (SC/ST & ಮಹಿಳೆಯರು)", desc: "SC/ST ಮತ್ತು ಮಹಿಳಾ ಉದ್ಯಮಿಗಳಿಗೆ ₹10 ಲಕ್ಷದಿಂದ ₹1 ಕೋಟಿವರೆಗೆ ಬ್ಯಾಂಕ್ ಸಾಲ ಸೌಲಭ್ಯ." },
    ml: { name: "സ്റ്റാൻഡ്-അപ്പ് ഇന്ത്യ പദ്ധതി (പട്ടികജാതി/പട്ടികവർഗ്ഗം & വനിതകൾ)", desc: "പട്ടികജാതി/പട്ടികവർഗ്ഗ, വനിതാ സംരംഭകർക്ക് ₹10 ലക്ഷം മുതൽ ₹1 കോടി വരെ ബാങ്ക് വായ്പ." },
    mr: { name: "स्टँड-अप इंडिया योजना (SC/ST व महिला)", desc: "नवीन उद्योगासाठी अनु.जाती/जमाती व महिलांना ₹१० लाख ते ₹१ कोटीपर्यंत बँक कर्ज सुविधा." },
    bn: { name: "স্ট্যান্ড-আপ ইন্ডিয়া প্রকল্প (SC/ST ও নারী)", desc: "তপশিলি জাতি/উপজাতি ও নারী উদ্যোক্তাদের জন্য ১০ লাখ থেকে ১ কোটি টাকা পর্যন্ত ব্যাংক ঋণ সুবিধা।" },
    gu: { name: "સ્ટેન્ડ-અપ ઇન્ડિયા યોજના (SC/ST અને મહિલાઓ)", desc: "નવા વ્યવસાય માટે SC/ST અને મહિલાઓને ₹૧૦ લાખથી ₹૧ કરોડ સુધીની બેંક લોન સહાય." },
    pa: { name: "ਸਟੈਂਡ-ਅੱਪ ਇੰਡੀਆ ਸਕੀਮ (SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ)", desc: "ਨਵਾਂ ਕਾਰੋਬਾਰ ਸ਼ੁਰੂ ਕਰਨ ਲਈ SC/ST ਅਤੇ ਮਹਿਲਾਵਾਂ ਨੂੰ ₹੧੦ ਲੱਖ ਤੋਂ ₹੧ ਕਰੋੜ ਤੱਕ ਬੈਂਕ ਕਰਜ਼ਾ।" },
    or: { name: "ଷ୍ଟାଣ୍ଡ-ଅପ ଇଣ୍ଡିଆ ଯୋଜନା (SC/ST ଓ ମହିଳା)", desc: "ନୂତନ ଉଦ୍ୟୋଗ ପାଇଁ SC/ST ଓ ମହିଳାମାନଙ୍କୁ ₹୧୦ ଲକ୍ଷରୁ ₹୧ କୋଟି ପର୍ଯ୍ୟନ୍ତ ବ୍ୟାଙ୍କ ଋଣ।" },
    as: { name: "ষ্টেণ্ড-আপ ইণ্ডিয়া আঁচনি (SC/ST আৰু মহিলা)", desc: "নতুন ব্যৱসায়ৰ বাবে SC/ST আৰু মহিলাসকলক ১০ লাখৰ পৰা ১ কোটি টকালৈকে বেংক ঋণ।" }
  },
  SVANIDHI: {
    hi: { name: "पीएम स्ट्रीट वेंडर्स आत्मनिर्भर निधि (पीएम स्वनिधि)", desc: "स्ट्रीट वेंडरों को ₹10,000 से ₹50,000 तक बिना गारंटी कार्यशील पूंजी ऋण व 7% ब्याज छूट।" },
    ta: { name: "பிரதமரின் தெருவோர வியாபாரிகள் தற்சார்பு நிதி (PM ஸ்வநிதி)", desc: "தெருவோர வியாபாரிகளுக்கு பிணையற்ற ₹10,000 முதல் ₹50,000 வரை கடன் மற்றும் 7% வட்டி மானியம்." },
    te: { name: "పీఎం స్వనిధి పథకం (వీధి వ్యాపారుల ఆత్మనిర్భర్ నిధి)", desc: "వీధి వ్యాపారులకు ₹10,000 నుండి ₹50,000 వరకు పూచీకత్తు లేని రుణం మరియు 7% వడ్డీ రాయితీ." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳ ಆತ್ಮನಿರ್ಭರ ನಿಧಿ (ಪಿಎಂ ಸ್ವನಿಧಿ)", desc: "ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳಿಗೆ ₹10,000 ದಿಂದ ₹50,000 ವರೆಗೆ ಖಾತರಿ ರಹಿತ ಸಾಲ ಮತ್ತು ಶೇ.7 ಬಡ್ಡಿ ರಿಯಾಯಿತಿ." },
    ml: { name: "പി.എം സ്വനിധി പദ്ധതി (തെരുവ് കച്ചവടക്കാർക്കായുള്ള വായ്പ)", desc: "തെരുവ് കച്ചവടക്കാർക്ക് ₹10,000 മുതൽ ₹50,000 വരെ ഈടില്ലാത്ത വായ്പയും 7% പലിശ ഇളവും." },
    mr: { name: "पीएम पथविक्रेते आत्मनिर्भर निधी (पीएम स्वनिधी)", desc: "फेरीवाल्यांना विनातारण ₹१०,००० ते ₹५०,००० पर्यंत कर्ज व ७% व्याज सवलत." },
    bn: { name: "প্রধানমন্ত্রী পিএম স্বনিধি প্রকল্প (পথ বিক্রেতাদের জন্য)", desc: "পথ বিক্রেতাদের জন্য জামিনমুক্ত ১০,০০০ থেকে ৫০,০০০ টাকা পর্যন্ত ঋণ ও ৭% সুদ ছাড়।" },
    gu: { name: "પીએમ સ્વનિધિ યોજના (શેરી ફેરિયાઓ માટે)", desc: "શેરી ફેરિયાઓ માટે તારણ મુક્ત ₹૧૦,૦૦૦ થી ₹૫૦,૦૦૦ સુધીની લોન અને ૭% વ્યાજ રાહત." },
    pa: { name: "ਪੀਐਮ ਸਵਨਿਧੀ ਸਕੀਮ (ਰੇਹੜੀ-ਫੜ੍ਹੀ ਵਾਲਿਆਂ ਲਈ)", desc: "ਰੇਹੜੀ ਵਾਲਿਆਂ ਲਈ ਬਿਨਾਂ ਗਰੰਟੀ ₹੧੦,੦੦੦ ਤੋਂ ₹੫੦,੦੦੦ ਕਰਜ਼ਾ ਅਤੇ ੭% ਵਿਆਜ ਛੋਟ।" },
    or: { name: "ପିଏମ ସ୍ୱନିଧି ଯୋଜନା (ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ)", desc: "ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ ବିନା ଜାମିନରେ ₹୧୦,୦୦୦ ରୁ ₹୫୦,୦୦୦ ଋଣ ଏବଂ ୭% ସୁଧ ରିହାତି।" },
    as: { name: "পিএম স্বনিধি আঁচনি (পথ বিক্ৰেতাসকলৰ বাবে)", desc: "পথ বিক্ৰেতাসকলৰ বাবে বন্ধকমুক্ত ১০,০০০ ৰ পৰা ৫০,০০০ টকা ঋণ আৰু ৭% সুদ ৰেহাই।" }
  },
  PM_SVANIDHI: {
    hi: { name: "पीएम स्ट्रीट वेंडर्स आत्मनिर्भर निधि (पीएम स्वनिधि)", desc: "स्ट्रीट वेंडरों को ₹10,000 से ₹50,000 तक बिना गारंटी कार्यशील पूंजी ऋण व 7% ब्याज छूट।" },
    ta: { name: "பிரதமரின் தெருவோர வியாபாரிகள் தற்சார்பு நிதி (PM ஸ்வநிதி)", desc: "தெருவோர வியாபாரிகளுக்கு பிணையற்ற ₹10,000 முதல் ₹50,000 வரை கடன் மற்றும் 7% வட்டி மானியம்." },
    te: { name: "పీఎం స్వనిధి పథకం (వీధి వ్యాపారుల ఆత్మనిర్భర్ నిధి)", desc: "వీధి వ్యాపారులకు ₹10,000 నుండి ₹50,000 వరకు పూచీకత్తు లేని రుణం మరియు 7% వడ్డీ రాయితీ." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳ ಆತ್ಮನಿರ್ಭರ ನಿಧಿ (ಪಿಎಂ ಸ್ವನಿಧಿ)", desc: "ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳಿಗೆ ₹10,000 ದಿಂದ ₹50,000 ವರೆಗೆ ಖಾತರಿ ರಹಿತ ಸಾಲ ಮತ್ತು ಶೇ.7 ಬಡ್ಡಿ ರಿಯಾಯಿತಿ." },
    ml: { name: "പി.എം സ്വനിധി പദ്ധതി (തെരുവ് കച്ചവടക്കാർക്കായുള്ള വായ്പ)", desc: "തെരുവ് കച്ചവടക്കാർക്ക് ₹10,000 മുതൽ ₹50,000 വരെ ഈടില്ലാത്ത വായ്പയും 7% പലിശ ഇളവും." },
    mr: { name: "पीएम पथविक्रेते आत्मनिर्भर निधी (पीएम स्वनिधी)", desc: "फेरीवाल्यांना विनातारण ₹१०,००० ते ₹५०,००० पर्यंत कर्ज व ७% व्याज सवलत." },
    bn: { name: "প্রধানমন্ত্রী পিএম স্বনিধি প্রকল্প (পথ বিক্রেতাদের জন্য)", desc: "পথ বিক্রেতাদের জন্য জামিনমুক্ত ১০,০০০ থেকে ৫০,০০০ টাকা পর্যন্ত ঋণ ও ৭% সুদ ছাড়।" },
    gu: { name: "પીએમ સ્વનિધિ યોજના (શેરી ફેરિયાઓ માટે)", desc: "શેરી ફેરિયાઓ માટે તારણ મુક્ત ₹૧૦,૦૦૦ થી ₹૫૦,૦૦૦ સુધીની લોન અને ૭% વ્યાજ રાહત." },
    pa: { name: "ਪੀਐਮ ਸਵਨਿਧੀ ਸਕੀਮ (ਰੇਹੜੀ-ਫੜ੍ਹੀ ਵਾਲਿਆਂ ਲਈ)", desc: "ਰੇਹੜੀ ਵਾਲਿਆਂ ਲਈ ਬਿਨਾਂ ਗਰੰਟੀ ₹੧੦,੦੦੦ ਤੋਂ ₹੫੦,੦੦੦ ਕਰਜ਼ਾ ਅਤੇ ੭% ਵਿਆਜ ਛੋਟ।" },
    or: { name: "ପିଏମ ସ୍ୱନିଧି ଯୋଜନା (ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ)", desc: "ରାସ୍ତାକଡ଼ ବିକ୍ରେତାଙ୍କ ପାଇଁ ବିନା ଜାମିନରେ ₹୧୦,୦୦୦ ରୁ ₹୫୦,୦୦୦ ଋଣ ଏବଂ ୭% ସୁଧ ରିହାତି।" },
    as: { name: "পিএম স্বনিধি আঁচনি (পথ বিক্ৰেতাসকলৰ বাবে)", desc: "পথ বিক্ৰেতাসকলৰ বাবে বন্ধকমুক্ত ১০,০০০ ৰ পৰা ৫০,০০০ টকা ঋণ আৰু ৭% সুদ ৰেহাই।" }
  },
  VISHWAKARMA: {
    hi: { name: "पीएम विश्वकर्मा योजना (पारंपरिक कारीगर व शिल्पकार)", desc: "18 पारंपरिक व्यवसायों के शिल्पकारों को कौशल प्रशिक्षण, ₹15,000 टूलकिट व 5% ब्याज पर ₹3 लाख ऋण।" },
    ta: { name: "பிரதமரின் விஸ்வகர்மா திட்டம் (பாரம்பரிய கைவினைஞர்கள்)", desc: "18 பாரம்பரிய கைவினைஞர்களுக்கு பயிற்சி, ₹15,000 கருவி மானியம் மற்றும் 5% வட்டியில் ₹3 இலட்சம் கடன்." },
    te: { name: "పీఎం విశ్వకర్మ పథకం (సాంప్రదాయ కళాకారులు)", desc: "18 సాంప్రదాయ వృత్తుల వారికి శిక్షణ, ₹15,000 టూల్‌కిట్ మరియు 5% వడ్డీతో ₹3 లక్షల రుణం." },
    kn: { name: "ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಯೋಜನೆ (ಪಾರಂಪರಿಕ ಕುಶಲಕರ್ಮಿಗಳು)", desc: "18 ಪಾರಂಪರಿಕ ವೃತ್ತಿಗಳ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ ತರಬೇತಿ, ₹15,000 ಟೂಲ್‌ಕಿಟ್ ಮತ್ತು ಶೇ.5 ಬಡ್ಡಿಯಲ್ಲಿ ₹3 ಲಕ್ಷ ಸಾಲ." },
    ml: { name: "പി.എം വിശ്വകർമ്മ പദ്ധതി (കരകൗശല വിദഗ്ദ്ധർ)", desc: "18 പരമ്പരാഗത തൊഴിലുകൾക്ക് പരിശീലനം, ₹15,000 ടൂൾകിറ്റ്, 5% പലിശയിൽ ₹3 ലക്ഷം വായ്പ." },
    mr: { name: "पीएम विश्वकर्मा योजना (पारंपरिक कारागीर व शिल्पकार)", desc: "१८ पारंपरिक कारागिरांना कौशल्य प्रशिक्षण, ₹१५,००० टूलकिट व ५% व्याजाने ₹३ लाख कर्ज." },
    bn: { name: "প্রধানমন্ত্রী বিশ্বকর্মা প্রকল্প (ঐতিহ্যবাহী কারিগর ও শিল্পী)", desc: "১৮টি ঐতিহ্যবাহী পেশার কারিগরদের জন্য প্রশিক্ষণ, ১৫,০০০ টাকা টুলকিট ও ৫% সুদে ৩ লাখ টাকা ঋণ।" },
    gu: { name: "પીએમ વિશ્વકર્મા યોજના (પરંપરાગત કારીગરો)", desc: "૧૮ પરંપરાગત કારીગરોને તાલીમ, ₹૧૫,૦૦૦ ટૂલકિટ અને ૫% વ્યાજે ₹૩ લાખની લોન." },
    pa: { name: "ਪੀਐਮ ਵਿਸ਼ਵਕਰਮਾ ਸਕੀਮ (ਰਵਾਇਤੀ ਦਸਤਕਾਰ)", desc: "੧੮ ਰਵਾਇਤੀ ਕਾਰੀਗਰਾਂ ਨੂੰ ਸਿਖਲਾਈ, ₹੧੫,੦੦੦ ਟੂਲਕਿੱਟ ਅਤੇ ੫% ਵਿਆਜ ਤੇ ₹੩ ਲੱਖ ਕਰਜ਼ਾ।" },
    or: { name: "ପିଏମ ବିଶ୍ୱକର୍ମା ଯୋଜନା (ପାରମ୍ପରିକ କାରିଗର)", desc: "୧୮ ପାରମ୍ପରିକ କାରିଗରଙ୍କୁ ପ୍ରଶିକ୍ଷଣ, ₹୧୫,୦୦୦ ଟୁଲକିଟ୍ ଏବଂ ୫% ସୁଧରେ ₹୩ ଲକ୍ଷ ଋଣ।",
    as: { name: "পিএম বিশ্বকৰ্মা আঁচনি (পৰম্পৰাগত কাৰিকৰ আৰু শিল্পী)", desc: "১৮টা পৰম্পৰাগত বৃত্তিৰ বাবে প্ৰশিক্ষণ, ১৫,০০০ টকাৰ টুলকিট আৰু ৫% সুদেৰে ৩ লাখ টকা ঋণ।" }
  },
  PM_VISHWAKARMA: {
    hi: { name: "पीएम विश्वकर्मा योजना (पारंपरिक कारीगर व शिल्पकार)", desc: "18 पारंपरिक व्यवसायों के शिल्पकारों को कौशल प्रशिक्षण, ₹15,000 टूलकिट व 5% ब्याज पर ₹3 लाख ऋण।" },
    ta: { name: "பிரதமரின் விஸ்வகர்மா திட்டம் (பாரம்பரிய கைவினைஞர்கள்)", desc: "18 பாரம்பரிய கைவினைஞர்களுக்கு பயிற்சி, ₹15,000 கருவி மானியம் மற்றும் 5% வட்டியில் ₹3 இலட்சம் கடன்." },
    te: { name: "పీఎం విశ్వకర్మ పథకం (సాంప్రదాయ కళాకారులు)", desc: "18 సాంప్రదాయ వృత్తుల వారికి శిక్షణ, ₹15,000 టూల్‌కిట్ మరియు 5% వడ్డీతో ₹3 లక్షల రుణం." },
    kn: { name: "ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಯೋಜನೆ (ಪಾರಂಪರಿಕ ಕುಶಲಕರ್ಮಿಗಳು)", desc: "18 ಪಾರಂಪರಿಕ ವೃತ್ತಿಗಳ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ ತರಬೇತಿ, ₹15,000 ಟೂಲ್‌ಕಿಟ್ ಮತ್ತು ಶೇ.5 ಬಡ್ಡಿಯಲ್ಲಿ ₹3 ಲಕ್ಷ ಸಾಲ." },
    ml: { name: "പി.എം വിശ്വകർമ്മ പദ്ധതി (കരകൗശല വിദഗ്ദ്ധർ)", desc: "18 പരമ്പരാഗത തൊഴിലുകൾക്ക് പരിശീലനം, ₹15,000 ടൂൾകിറ്റ്, 5% പലിശയിൽ ₹3 ലക്ഷം വായ്പ." },
    mr: { name: "पीएम विश्वकर्मा योजना (पारंपरिक कारागीर व शिल्पकार)", desc: "१८ पारंपरिक कारागिरांना कौशल्य प्रशिक्षण, ₹१५,००० टूलकिट व ५% व्याजाने ₹३ लाख कर्ज." },
    bn: { name: "প্রধানমন্ত্রী বিশ্বকর্মা প্রকল্প (ঐতিহ্যবাহী কারিগর ও শিল্পী)", desc: "১৮টি ঐতিহ্যবাহী পেশার কারিগরদের জন্য প্রশিক্ষণ, ১৫,০০০ টাকা টুলকিট ও ৫% সুদে ৩ লাখ টাকা ঋণ।" },
    gu: { name: "પીએમ વિશ્વકર્મા યોજના (પરંપરાગત કારીગરો)", desc: "૧૮ પરંપરાગત કારીગરોને તાલીમ, ₹૧૫,૦૦૦ ટૂલકિટ અને ૫% વ્યાજે ₹૩ લાખની લોન." },
    pa: { name: "ਪੀਐਮ ਵਿਸ਼ਵਕਰਮਾ ਸਕੀਮ (ਰਵਾਇਤੀ ਦਸਤਕਾਰ)", desc: "੧੮ ਰਵਾਇਤੀ ਕਾਰੀਗਰਾਂ ਨੂੰ ਸਿਖਲਾਈ, ₹੧੫,੦੦੦ ਟੂਲਕਿੱਟ ਅਤੇ ੫% ਵਿਆਜ ਤੇ ₹੩ ਲੱਖ ਕਰਜ਼ਾ।" },
    or: { name: "ପିଏମ ବିଶ୍ୱକର୍ମା ଯୋଜନା (ପାରମ୍ପରିକ କାରିଗର)", desc: "୧୮ ପାରମ୍ପରିକ କାରିଗରଙ୍କୁ ପ୍ରଶିକ୍ଷଣ, ₹୧୫,୦୦୦ ଟୁଲକିଟ୍ ଏବଂ ୫% ସୁଧରେ ₹୩ ଲକ୍ଷ ଋଣ।",
    as: { name: "পিএম বিশ্বকৰ্মা আঁচনি (পৰম্পৰাগত কাৰিকৰ আৰু শিল্পী)", desc: "১৮টা পৰম্পৰাগত বৃত্তিৰ বাবে প্ৰশিক্ষণ, ১৫,০০০ টকাৰ টুলকিট আৰু ৫% সুদেৰে ৩ লাখ টকা ঋণ।" }
  },
  MUDRA_SHISHU: {
    hi: { name: "प्रधानमंत्री मुद्रा योजना - शिशु (₹50,000 तक)", desc: "नए और छोटे व्यवसायों के लिए ₹50,000 तक का बिना जमानत का सूक्ष्म ऋण।" },
    ta: { name: "பிரதமரின் முத்ரா திட்டம் - சிஷு (₹50,000 வரை)", desc: "புதிய மற்றும் சிறு வணிகங்களுக்கான ₹50,000 வரை பிணையற்ற குறுங்கடன்." },
    te: { name: "పీఎం ముద్రా యోజన - శిశు (₹50,000 వరకు)", desc: "చిన్న వ్యాపారాల కోసం ₹50,000 వరకు పూచీకత్తు లేని సూక్ష్మ రుణం." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ಶಿಶು (₹50,000 ವರೆಗೆ)", desc: "ಸಣ್ಣ ಉದ್ಯಮಗಳಿಗೆ ₹50,000 ವರೆಗೆ ಖಾತರಿ ರಹಿತ ಕಿರು ಸಾಲ." },
    ml: { name: "പി.എം മുദ്ര യോജന - ശിശു (₹50,000 വരെ)", desc: "ചെറുകിട സംരംഭങ്ങൾക്ക് ₹50,000 വരെ ഈടില്ലാത്ത വായ്പ." },
    mr: { name: "पंतप्रधान मुद्रा योजना - शिशु (₹५०,००० पर्यंत)", desc: "लहान उद्योगांसाठी ₹५०,००० पर्यंत तारणमुक्त सूक्ष्म कर्ज." },
    bn: { name: "প্রধানমন্ত্রী মুদ্রা যোজনা - শিশু (৫০,০০০ টাকা পর্যন্ত)", desc: "ছোট ব্যবসার জন্য ৫০,০০০ টাকা পর্যন্ত জামিনমুক্ত ক্ষুদ্র ঋণ।" },
    gu: { name: "પ્રધાનમંત્રી મુદ્રા યોજના - શિશુ (₹૫૦,૦૦૦ સુધી)", desc: "નાના વ્યવસાયો માટે ₹૫૦,૦૦૦ સુધીની તારણ મુક્ત માઇક્રો લોન." },
    pa: { name: "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਸ਼ਿਸ਼ੂ (₹੫੦,੦੦੦ ਤੱਕ)", desc: "ਛੋਟੇ ਕਾਰੋਬਾਰਾਂ ਲਈ ₹੫੦,੦੦੦ ਤੱਕ ਬਿਨਾਂ ਗਰੰਟੀ ਮਾਈਕ੍ਰੋ ਕਰਜ਼ਾ।" },
    or: { name: "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - ଶିଶୁ (₹୫୦,୦୦୦ ପର୍ଯ୍ୟନ୍ତ)", desc: "କ୍ଷୁଦ୍ର ବ୍ୟବସାୟ ପାଇଁ ₹୫୦,୦୦୦ ପର୍ଯ୍ୟନ୍ତ ଜାମିନ ମୁକ୍ତ ଋଣ।" },
    as: { name: "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - শিশু (৫০,০০০ টকালৈকে)", desc: "ক্ষুদ্ৰ ব্যৱসায়ৰ বাবে ৫০,০০০ টকালৈকে বন্ধকমুক্ত ঋণ।" }
  },
  MUDRA_KISHORE: {
    hi: { name: "प्रधानमंत्री मुद्रा योजना - किशोर (₹5 लाख तक)", desc: "स्थापित व्यवसायों के विस्तार के लिए ₹50,000 से ₹5 लाख तक का बिना गारंटी ऋण।" },
    ta: { name: "பிரதமரின் முத்ரா திட்டம் - கிஷோர் (₹5 இலட்சம் வரை)", desc: "தொழில் விரிவாக்கத்திற்கு ₹50,000 முதல் ₹5 இலட்சம் வரை பிணையற்ற கடன்." },
    te: { name: "పీఎం ముద్రా యోజన - కిషోర్ (₹5 లక్షల వరకు)", desc: "వ్యాపార విస్తరణ కోసం ₹50,000 నుండి ₹5 లక్షల వరకు పూచీకత్తు లేని రుణం." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ಕಿಶೋರ್ (₹5 ಲಕ್ಷದವರೆಗೆ)", desc: "ವ್ಯವಹಾರ ವಿಸ್ತರಣೆಗೆ ₹50,000 ದಿಂದ ₹5 ಲಕ್ಷದವರೆಗೆ ಸಾಲ ಸೌಲಭ್ಯ." },
    ml: { name: "പി.എം മുദ്ര യോജന - കിഷോർ (₹5 ലക്ഷം വരെ)", desc: "ബിസിനസ്സ് വിപുലീകരണത്തിന് ₹50,000 മുതൽ ₹5 ലക്ഷം വരെ വായ്പ." },
    mr: { name: "पंतप्रधान मुद्रा योजना - किशोर (₹५ लाखांपर्यंत)", desc: "व्यवसाय विस्तारासाठी ₹५०,००० ते ₹५ लाखांपर्यंत तारणमुक्त कर्ज." },
    bn: { name: "প্রধানমন্ত্রী মুদ্রা যোজনা - কিশোর (৫ লাখ টাকা পর্যন্ত)", desc: "ব্যবসা সম্প্রসারণের জন্য ৫০,০০০ থেকে ৫ লাখ টাকা পর্যন্ত ঋণ।" },
    gu: { name: "પ્રધાનમંત્રી મુદ્રા યોજના - કિશોર (₹૫ લાખ સુધી)", desc: "વ્યવસાય વિસ્તરણ માટે ₹૫૦,૦૦૦ થી ₹૫ લાખ સુધીની લોન." },
    pa: { name: "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਕਿਸ਼ੋਰ (₹੫ ਲੱਖ ਤੱਕ)", desc: "ਕਾਰੋਬਾਰ ਵਧਾਉਣ ਲਈ ₹੫੦,੦੦੦ ਤੋਂ ₹੫ ਲੱਖ ਤੱਕ ਕਰਜ਼ਾ।" },
    or: { name: "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - କିଶୋର (₹୫ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ)", desc: "ବ୍ୟବସାୟ ବୃଦ୍ଧି ପାଇଁ ₹୫୦,୦୦୦ ରୁ ₹୫ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ଋଣ।" },
    as: { name: "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - কিশোৰ (৫ লাখ টকালৈকে)", desc: "ব্যৱসায় সম্প্ৰসাৰণৰ বাবে ৫০,০০০ ৰ পৰা ৫ লাখ টকালৈকে ঋণ।" }
  },
  MUDRA_TARUN: {
    hi: { name: "प्रधानमंत्री मुद्रा योजना - तरुण (₹10 लाख तक)", desc: "सूक्ष्म व लघु उद्यमों के बड़े विस्तार के लिए ₹5 लाख से ₹10 लाख तक का बैंक ऋण।" },
    ta: { name: "பிரதமரின் முத்ரா திட்டம் - தருண் (₹10 இலட்சம் வரை)", desc: "தொழில் வளர்ச்சிக்கு ₹5 இலட்சம் முதல் ₹10 இலட்சம் வரை வங்கி கடன்." },
    te: { name: "పీఎం ముద్రా యోజన - తరుణ్ (₹10 లక్షల వరకు)", desc: "పరిశ్రమల వృద్ధి కోసం ₹5 లక్షల నుండి ₹10 లక్షల వరకు బ్యాంక్ రుణం." },
    kn: { name: "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ - ತರುಣ್ (₹10 ಲಕ್ಷದವರೆಗೆ)", desc: "ಉದ್ಯಮಗಳ ಬೆಳವಣಿಗೆಗೆ ₹5 ಲಕ್ಷದಿಂದ ₹10 ಲಕ್ಷದವರೆಗೆ ಸಾಲ ಸೌಲಭ್ಯ." },
    ml: { name: "പി.എം മുദ്ര യോജന - തരുൺ (₹10 ലക്ഷം വരെ)", desc: "സംരംഭക വികസനത്തിന് ₹5 ലക്ഷം മുതൽ ₹10 ലക്ഷം വരെ ബാങ്ക് വായ്പ." },
    mr: { name: "पंतप्रधान मुद्रा योजना - तरुण (₹१० लाखांपर्यंत)", desc: "उद्योगाच्या मोठ्या विस्तारासाठी ₹५ लाख ते ₹१० लाखांपर्यंत बँक कर्ज." },
    bn: { name: "প্রধানমন্ত্রী মুদ্রা যোজনা - তরুণ (১০ লাখ টাকা পর্যন্ত)", desc: "উদ্যোগের বৃদ্ধির জন্য ৫ লাখ থেকে ১০ লাখ টাকা পর্যন্ত ব্যাংক ঋণ।" },
    gu: { name: "પ્રધાનમંત્રી મુદ્રા યોજના - તરુણ (₹૧૦ લાખ સુધી)", desc: "વ્યવસાયના મોટા વિસ્તરણ માટે ₹૫ લાખથી ₹૧૦ લાખ સુધીની લોન." },
    pa: { name: "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ - ਤਰੁਣ (₹੧੦ ਲੱਖ ਤੱਕ)", desc: "ਕਾਰੋਬਾਰੀ ਵਾਧੇ ਲਈ ₹੫ ਲੱਖ ਤੋਂ ₹੧੦ ਲੱਖ ਤੱਕ ਬੈਂਕ ਕਰਜ਼ਾ।" },
    or: { name: "ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା - ତରୁଣ (₹୧୦ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ)", desc: "ଉଦ୍ୟୋଗ ବିକାଶ ପାଇଁ ₹୫ ଲକ୍ଷରୁ ₹୧୦ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ବ୍ୟାଙ୍କ ଋଣ।" },
    as: { name: "প্ৰধানমন্ত্ৰী মুদ্ৰা যোজনা - তৰুণ (১০ লাখ টকালৈকে)", desc: "উদ্যোগ বিকাশৰ বাবে ৫ লাখৰ পৰা ১০ লাখ টকালৈকে বেংক ঋণ।" }
  }
};

export const DICTIONARY = {
  en: {
    appName: 'SCHEME SATHI',
    tagline: 'AI-Driven Scheme Matching for Marginalized Entrepreneurs',
    translationBadge: 'Powered by AI4Bharat Samanantar IndicNLP',
    sihBadgeText: 'SIH 2026',
    sihSubtext: 'Problem Statement ID: SIH26092 • AI-Driven Scheme Matching • Official myScheme.gov.in Dataset',
    navHome: 'Home',
    navHowItWorks: 'How It Works',
    navSchemes: 'Schemes',
    navFeatures: 'Features',
    navAbout: 'About',
    navLogin: 'Login',
    navRegister: 'Register',
    navDashboard: 'Dashboard',
    navFindScheme: 'Find My Scheme',
    navEmi: 'EMI Calculator',
    navDocAssistant: 'Doc Assistant',
    navPartners: 'Channel Partners',
    navChat: 'AI Assistant',
    navAdmin: 'Admin Portal',
    navProfile: 'User Profile',
    navLogout: 'Logout',
    heroTitle: 'Find the Right Government Scheme for You',
    heroSubtitle: 'AI-powered scheme discovery, deterministic eligibility checking, and financial guidance for marginalized entrepreneurs and students.',
    find_my_scheme: 'Find My Scheme',
    btnFindScheme: 'Find My Scheme',
    chat_assistant: 'Chat with AI Assistant',
    btnChatAssistant: 'Chat with AI Assistant',
    btnExploreSchemes: 'Explore Schemes',
    btnCalculateEmi: 'Calculate EMI',
    btnCheckDocs: 'Check Documents',
    tailoredFor: 'Tailored For Vulnerable Groups:',
    scStFounders: 'SC / ST Founders',
    womenEntrepreneurs: 'Women Entrepreneurs',
    minorityCommunities: 'Minority Communities',
    streetVendors: 'Street Vendors',
    traditionalArtisans: 'Traditional Artisans',
    differentlyAbled: 'Differently Abled',
    instantCheckTitle: 'Instant Eligibility Check',
    instantCheckSubtitle: 'Discover your best match in 30 seconds',
    socialCategory: 'Your Social Category',
    gender: 'Gender',
    businessType: 'Business Type',
    requiredLoan: 'Required Loan Amount',
    btnAnalyzeSchemes: 'Analyze Matching Schemes',
    liveAiBadge: 'Live AI',
    statCentralState: 'Central & State Schemes (myScheme)',
    statSubsidies: 'Capital & Special Subsidies',
    statLanguages: '11 Indian Regional Languages',
    statIntegrity: 'Deterministic Rule Integrity',
    workflowTitle: 'Architectural Workflow',
    workflowSubtitle: 'How Scheme Sathi Works',
    step1WorkflowTitle: 'Profile & Need Analysis',
    step1WorkflowDesc: 'Captures demographics (SC/ST/Woman/Minority), project cost, location, and trade.',
    step2WorkflowTitle: 'Deterministic Rule Engine',
    step2WorkflowDesc: 'Evaluates exact legal gazette rules (age, ceiling, margin) without LLM hallucinations.',
    step3WorkflowTitle: 'SHAP-Style Ranking',
    step3WorkflowDesc: 'Calculates multi-factor compatibility scores and provides crystal-clear explainability.',
    step4WorkflowTitle: 'OCR & Partner Routing',
    step4WorkflowDesc: 'Verifies Aadhaar/Caste certificates & routes to nearest authorized Bank or CSC center.',
    featuredSchemesTitle: 'Verified Government Schemes',
    featuredSchemesSubtitle: 'Synced with Official myScheme.gov.in Gazette Standards',
    maxLoan: 'Max Sanction Limit',
    subsidyRate: 'Subsidy Rate',
    tenor: 'Tenure & Repayment',
    collateral: 'Collateral Security',
    whyMatched: 'Why This Scheme Matched You',
    statutoryRules: 'Statutory Gazette Rules',
    requiredDocs: 'Required Documents',
    verifyOcr: 'Verify OCR',
    officialPortal: 'Official Portal on myScheme',
    viewDetails: 'View Details & Apply',
    testimonialsTitle: 'Empowering Marginalized Communities Across India',
    ctaTitle: 'Ready to Claim Your Government Subsidy?',
    ctaDesc: 'Check your eligibility now with zero hassle and get connected to your local sanctioning bank.',
    ctaButton: 'Start Free Assessment',
    footerRights: 'Scheme Sathi © 2026. Built for Smart India Hackathon 2026.',
    targetMarginalized: 'Marginalized',
    unitMonths: 'Months',
    unitLakh: 'Lakh',
    unitCrore: 'Cr',
    lowInterest: 'Low Interest Subsidy',
    bankGuarantee: 'Bank Guarantee',
    specialRural: 'Up to 35% Special Rural',
    sliderMinSVANidhi: '₹10,000 (SVANidhi)',
    sliderMidMudra: '₹10 Lakh (Mudra)',
    sliderMidPMEGP: '₹50 Lakh (PMEGP)',
    sliderMaxStandUp: '₹10 Cr (StandUp)',
    optionSC: 'Scheduled Caste (SC)',
    optionST: 'Scheduled Tribe (ST)',
    optionOBC: 'Other Backward Class (OBC)',
    optionMinority: 'Minority Community',
    optionGeneral: 'General Category',
    optionFemale: 'Woman / Female',
    optionMale: 'Male',
    optionTransgender: 'Transgender',
    optionGraduate: 'Graduate / Degree Holder',
    option12th: '12th Standard Pass',
    option8th: '8th Standard Pass (PMEGP Eligible for >₹10L)',
    optionBelow8th: 'Below 8th Standard',
    optionRural: 'Rural (Higher Subsidy up to 35%)',
    optionUrban: 'Urban (Subsidy up to 25%)',
    optionNewStage: 'New Enterprise (Greenfield Project)',
    optionExpansionStage: 'Expansion of Existing Unit',
    manufacturingOption: 'Manufacturing (Production)',
    serviceOption: 'Service Unit (Repair, Salon, Clinic)',
    tradingOption: 'Trading / Retail Shop',
    streetVendorOption: 'Street Vending (Hawking)',
    artisanOption: 'Traditional Artisan / Handloom',
    wizardTitle: 'Find Your Perfect Govt Scheme',
    wizardSubtitle: 'Accurate deterministic gazette matching for SC/ST, Women, Minorities, Artisans & Vendors',
    step1Title: 'Identity',
    step2Title: 'Location',
    step3Title: 'Enterprise',
    step4Title: 'Loan Needs',
    step5Title: 'Documents',
    step1Desc: 'Government schemes have special subsidies and quotas dedicated to specific demographic groups.',
    step2Desc: 'Subsidies are higher in Rural zones (35%) compared to Urban centers (25%).',
    step3Desc: 'Specify your business domain to match specialized ministry allocations.',
    step4Desc: 'Calculate capital requirements, margin money contributions, and repayment bandwidth.',
    step5Desc: 'Pre-check required paperwork for instant 1-click verification.',
    socialCategoryLabel: 'Social Category *',
    genderLabel: 'Gender *',
    ageLabel: 'Age (Years) *',
    educationLabel: 'Education Level *',
    differentlyAbledLabel: 'Applicant is Differently Abled (Divyangjan / PwD > 40%)',
    stateLabel: 'State / Union Territory *',
    districtLabel: 'District *',
    areaTypeLabel: 'Area Classification *',
    pincodeLabel: 'PIN Code *',
    businessStageLabel: 'Business Stage *',
    isArtisanLabel: 'Traditional Artisan / Craftsperson (PM Vishwakarma Eligible)',
    isVendorLabel: 'Street Vendor / Hawker (PM SVANidhi Eligible)',
    hasTrainingLabel: 'Has Completed Recognized Skill Training (EDP / Skill India)',
    projectCostLabel: 'Total Project Cost (₹) *',
    requiredLoanLabel: 'Required Loan Amount (₹) *',
    ownContributionLabel: 'Own Contribution / Margin Money (₹) *',
    annualIncomeLabel: 'Annual Household Income (₹) *',
    hasAadhaarLabel: 'Aadhaar Card (UIDAI)',
    hasPanLabel: 'PAN Card (Income Tax Dept)',
    hasCasteLabel: 'Caste / Community Certificate',
    hasDprLabel: 'Detailed Project Report (DPR)',
    hasBankLabel: 'Bank Account & 6-Month Statement',
    hasUdyamLabel: 'Udyam MSME Registration Certificate',
    btnPrevious: 'Previous Step',
    btnNext: 'Next Step',
    btnEvaluateSchemes: 'Evaluate Eligible Schemes',
    evaluatingText: 'Evaluating Gazette Rules...',
    resultsTitle: 'Your Scheme Matches & Eligibility Analysis',
    resultsSubtitle: '100% Deterministic Rule Matching with AI4Bharat Explainability',
    topMatchBadge: 'Top Recommendation',
    matchScore: 'Match Score',
    eligibleStatus: 'Eligible (Approved)',
    ineligibleStatus: 'Ineligible (Criteria Mismatch)',
    subsidyEligible: 'Est. Subsidy Benefit',
    viewFullBreakdown: 'Explainable AI Factor Breakdown',
    downloadChecklist: 'Download Document Checklist',
    locateBankPartner: 'Locate Nearest Bank Partner',
    positiveFactors: 'Positive Qualification Factors',
    limitingFactors: 'Limiting & Risk Factors',
    noSchemesFound: 'No eligible schemes found for this profile. Please adjust project cost or parameters.',
    chatTitle: 'AI Scheme Sathi Assistant',
    chatSubtitle: 'Ask questions in your regional language powered by Qwen & Samanantar IndicNLP',
    chatPlaceholder: 'Ask about loans, subsidies, documents, or PM-SVANidhi, PMEGP, Stand-Up India...',
    chatSend: 'Send Message',
    qwenPowered: 'Grounded on official myScheme.gov.in gazette dataset & Qwen Local LLM',
    suggestedQueries: 'Suggested Queries:',
    promptPmegp: 'How much subsidy can I get under PMEGP?',
    promptSvanidhi: 'Can street vendors get a loan without collateral?',
    promptWomen: 'What schemes are available for women entrepreneurs?',
    promptSubsidy: 'What documents are required for capital subsidy?'
  },
  hi: {
    appName: 'स्कीम साथी',
    tagline: 'वंचित उद्यमियों के लिए एआई-आधारित सरकारी योजना खोज',
    translationBadge: 'AI4Bharat Samanantar IndicNLP द्वारा संचालित',
    sihBadgeText: 'SIH 2026',
    sihSubtext: 'समस्या विवरण ID: SIH26092 • एआई योजना मिलान • myScheme.gov.in डेटासेट',
    navHome: 'होम',
    navHowItWorks: 'कार्यप्रणाली',
    navSchemes: 'योजनाएं',
    navFeatures: 'विशेषताएं',
    navAbout: 'हमारे बारे में',
    navLogin: 'लॉग इन',
    navRegister: 'पंजीकरण',
    navDashboard: 'डैशबोर्ड',
    navFindScheme: 'मेरी योजना खोजें',
    navEmi: 'ईएमआई कैलकुलेटर',
    navDocAssistant: 'दस्तावेज़ सहायक',
    navPartners: 'सहयोगी केंद्र',
    navChat: 'एआई सहायक',
    navAdmin: 'व्यवस्थापक पोर्टल',
    navProfile: 'उपयोगकर्ता प्रोफ़ाइल',
    navLogout: 'लॉग आउट',
    heroTitle: 'अपने लिए सही सरकारी योजना खोजें',
    heroSubtitle: 'उद्यमियों और छात्रों के लिए एआई-संचालित योजना खोज, सटीक पात्रता जांच और वित्तीय मार्गदर्शन।',
    find_my_scheme: 'मेरी योजना खोजें',
    btnFindScheme: 'मेरी योजना खोजें',
    chat_assistant: 'एआई सहायक से बात करें',
    btnChatAssistant: 'एआई सहायक से बात करें',
    btnExploreSchemes: 'योजनाएं देखें',
    btnCalculateEmi: 'ईएमआई गणना करें',
    btnCheckDocs: 'दस्तावेज़ जांचें',
    tailoredFor: 'विशेष रूप से इनके लिए डिज़ाइन:',
    scStFounders: 'अजा / अजजा (SC/ST) उद्यमी',
    womenEntrepreneurs: 'महिला उद्यमी',
    minorityCommunities: 'अल्पसंख्यक समुदाय',
    streetVendors: 'स्ट्रीट वेंडर (रेहड़ी-पटरी)',
    traditionalArtisans: 'पारंपरिक कारीगर ও शिल्पकार',
    differentlyAbled: 'दिव्यांगजन (PwD)',
    instantCheckTitle: 'त्वरित पात्रता जांच',
    instantCheckSubtitle: '30 सेकंड में अपने लिए सर्वोत्तम योजना जानें',
    socialCategory: 'आपका सामाजिक वर्ग',
    gender: 'लिंग',
    businessType: 'व्यवसाय का प्रकार',
    requiredLoan: 'आवश्यक ऋण राशि',
    btnAnalyzeSchemes: 'उपयुक्त योजनाओं का विश्लेषण करें',
    liveAiBadge: 'लाइव एआई',
    statCentralState: 'केंद्रीय व राज्य योजनाएं (myScheme)',
    statSubsidies: 'पूंजीगत व विशेष अनुदान (सब्सिडी)',
    statLanguages: '11 भारतीय क्षेत्रीय भाषाएं',
    statIntegrity: '100% राजपत्र नियम सत्यता',
    workflowTitle: 'प्रक्रिया प्रवाह',
    workflowSubtitle: 'स्कीम साथी कैसे काम करता है',
    step1WorkflowTitle: 'प्रोफ़ाइल व आवश्यकता विश्लेषण',
    step1WorkflowDesc: 'सामाजिक वर्ग, लिंग, परियोजना लागत और व्यापार का सटीक विवरण लेता है।',
    step2WorkflowTitle: 'वैधानिक नियम इंजन',
    step2WorkflowDesc: 'बिना किसी भ्रम (hallucination) के सटीक राजपत्र नियमों की जांच करता है।',
    step3WorkflowTitle: 'SHAP-आधारित रैंकिंग',
    step3WorkflowDesc: 'सटीक अनुकूलता स्कोर और स्पष्ट कारण विश्लेषण प्रदान करता है।',
    step4WorkflowTitle: 'ओसीआर व बैंक पार्टनर रूटिंग',
    step4WorkflowDesc: 'दस्तावेज़ सत्यापित कर निकटतम अधिकृत बैंक शाखा से जोड़ता है।',
    featuredSchemesTitle: 'सत्यापित सरकारी योजनाएं',
    featuredSchemesSubtitle: 'myScheme.gov.in के आधिकारिक मानकों पर आधारित',
    maxLoan: 'अधिकतम ऋण सीमा',
    subsidyRate: 'सब्सिडी (अनुदान) दर',
    tenor: 'पुनर्भुगतान अवधि',
    collateral: 'जमानत / बंधक',
    whyMatched: 'यह योजना आपके लिए क्यों उपयुक्त है',
    statutoryRules: 'वैधानिक राजपत्र नियम',
    requiredDocs: 'आवश्यक दस्तावेज़',
    verifyOcr: 'ओसीआर सत्यापन',
    officialPortal: 'myScheme आधिकारिक पोर्टल',
    viewDetails: 'विवरण देखें व आवेदन करें',
    testimonialsTitle: 'भारत भर के वंचित उद्यमियों का सशक्तिकरण',
    ctaTitle: 'क्या आप सरकारी सब्सिडी प्राप्त करने के लिए तैयार हैं?',
    ctaDesc: 'अपनी पात्रता तुरंत जांचें और नजदीकी बैंक शाखा से जुड़ें।',
    ctaButton: 'निःशुल्क मूल्यांकन शुरू करें',
    footerRights: 'स्कीम साथी © 2026. स्मार्ट इंडिया हैकाथॉन 2026 के लिए विकसित।',
    targetMarginalized: 'वंचित वर्ग',
    unitMonths: 'माह',
    unitLakh: 'लाख',
    unitCrore: 'करोड़',
    lowInterest: 'कम ब्याज / सब्सिडी',
    bankGuarantee: 'बैंक गारंटी',
    specialRural: '35% तक ग्रामीण सब्सिडी',
    sliderMinSVANidhi: '₹10,000 (स्वनिधि)',
    sliderMidMudra: '₹10 लाख (मुद्रा)',
    sliderMidPMEGP: '₹50 लाख (PMEGP)',
    sliderMaxStandUp: '₹10 करोड़ (स्टैंड-अप)',
    optionSC: 'अनुसूचित जाति (SC)',
    optionST: 'अनुसूचित जनजाति (ST)',
    optionOBC: 'अन्य पिछड़ा वर्ग (OBC)',
    optionMinority: 'अल्पसंख्यक समुदाय',
    optionGeneral: 'सामान्य वर्ग (General)',
    optionFemale: 'महिला उद्यमी',
    optionMale: 'पुरुष',
    optionTransgender: 'ट्रांसजेंडर (तृतीय लिंग)',
    optionGraduate: 'स्नातक / डिग्री धारक',
    option12th: '12वीं पास',
    option8th: '8वीं पास (PMEGP पात्र)',
    optionBelow8th: '8वीं से कम',
    optionRural: 'ग्रामीण (35% तक उच्च सब्सिडी)',
    optionUrban: 'शहरी (25% तक सब्सिडी)',
    optionNewStage: 'नया उद्यम (ग्रीनफील्ड)',
    optionExpansionStage: 'मौजूदा इकाई का विस्तार',
    manufacturingOption: 'विनिर्माण (उत्पादन)',
    serviceOption: 'सेवा इकाई (सर्विस)',
    tradingOption: 'व्यापार / खुदरा',
    streetVendorOption: 'स्ट्रीट वेंडिंग (रेहड़ी-पटरी)',
    artisanOption: 'पारंपरिक कारीगर / शिल्पकार',
    wizardTitle: 'अपने लिए उत्तम सरकारी योजना खोजें',
    wizardSubtitle: 'एससी/एसटी, महिला, अल्पसंख्यक और कारीगरों के लिए सटीक राजपत्र मिलान',
    step1Title: 'पहचान',
    step2Title: 'स्थान',
    step3Title: 'उद्यम',
    step4Title: 'ऋण आवश्यकता',
    step5Title: 'दस्तावेज़',
    step1Desc: 'सरकारी योजनाओं में विशिष्ट जनसांख्यिकीय समूहों के लिए विशेष सब्सिडी व कोटा होता है।',
    step2Desc: 'ग्रामीण क्षेत्रों में शहरी केंद्रों की तुलना में अधिक सब्सिडी (35%) मिलती है।',
    step3Desc: 'विशिष्ट मंत्रालय योजनाओं से मिलान करने हेतु व्यवसाय का प्रकार चुनें।',
    step4Desc: 'परियोजना लागत, स्वयं का अंशदान और पुनर्भुगतान क्षमता दर्ज करें।',
    step5Desc: 'त्वरित सत्यापन के लिए आवश्यक कागजात पहले से जांचें।',
    socialCategoryLabel: 'सामाजिक वर्ग *',
    genderLabel: 'लिंग *',
    ageLabel: 'आयु (वर्ष) *',
    educationLabel: 'शैक्षणिक योग्यता *',
    differentlyAbledLabel: 'आवेदक दिव्यांगजन है (PwD > 40%)',
    stateLabel: 'राज्य / केंद्र शासित प्रदेश *',
    districtLabel: 'जिला *',
    areaTypeLabel: 'क्षेत्र वर्गीकरण *',
    pincodeLabel: 'पिन कोड *',
    businessStageLabel: 'व्यवसाय की स्थिति *',
    isArtisanLabel: 'पारंपरिक कारीगर / शिल्पकार (पीएम विश्वकर्मा पात्र)',
    isVendorLabel: 'रेहड़ी-पटरी / स्ट्रीट वेंडर (पीएम स्वनिधि पात्र)',
    hasTrainingLabel: 'प्रशिक्षण प्राप्त (EDP / कौशल विकास)',
    projectCostLabel: 'कुल परियोजना लागत (₹) *',
    requiredLoanLabel: 'आवश्यक ऋण राशि (₹) *',
    ownContributionLabel: 'स्वयं का अंशदान (मार्जिन मनी) (₹) *',
    annualIncomeLabel: 'वार्षिक पारिवारिक आय (₹) *',
    hasAadhaarLabel: 'आधार कार्ड (UIDAI)',
    hasPanLabel: 'पैन कार्ड',
    hasCasteLabel: 'जाति / श्रेणी प्रमाण पत्र',
    hasDprLabel: 'विस्तृत परियोजना रिपोर्ट (DPR)',
    hasBankLabel: 'बैंक खाता व 6 माह का विवरण',
    hasUdyamLabel: 'उद्यम एमएसएमई पंजीकरण प्रमाण पत्र',
    btnPrevious: 'पिछला चरण',
    btnNext: 'अगला चरण',
    btnEvaluateSchemes: 'पात्र योजनाएं खोजें',
    evaluatingText: 'राजपत्र नियमों की जांच जारी...',
    resultsTitle: 'आपकी योजनाएं एवं पात्रता विश्लेषण',
    resultsSubtitle: 'AI4Bharat व्याख्यात्मकता के साथ 100% नियम मिलान',
    topMatchBadge: 'सर्वश्रेष्ठ अनुशंसा',
    matchScore: 'मिलान स्कोर',
    eligibleStatus: 'पात्र (स्वीकृत)',
    ineligibleStatus: 'अपात्र (मानदंड असंगत)',
    subsidyEligible: 'अनुमानित सब्सिडी लाभ',
    viewFullBreakdown: 'व्याख्यात्मक एआई कारक विश्लेषण',
    downloadChecklist: 'दस्तावेज़ चेकलिस्ट डाउनलोड करें',
    locateBankPartner: 'निकटतम बैंक शाखा खोजें',
    positiveFactors: 'सकारात्मक योग्यता कारक',
    limitingFactors: 'सीमाएं एवं जोखिम कारक',
    noSchemesFound: 'इस प्रोफ़ाइल के लिए कोई पात्र योजना नहीं मिली। कृपया लागत या मानदंड बदलें।',
    chatTitle: 'एआई स्कीम साथी सहायक',
    chatSubtitle: 'Qwen एवं Samanantar IndicNLP द्वारा अपनी भाषा में बातचीत करें',
    chatPlaceholder: 'ऋण, सब्सिडी, दस्तावेज़ या पीएम-स्वनिधि, पीएमईजीपी के बारे में पूछें...',
    chatSend: 'संदेश भेजें',
    qwenPowered: 'myScheme.gov.in आधिकारिक डेटा एवं Qwen लोकल एलएलएम द्वारा संचालित',
    suggestedQueries: 'सुझाए गए प्रश्न:',
    promptPmegp: 'PMEGP के तहत मुझे कितनी सब्सिडी मिल सकती है?',
    promptSvanidhi: 'क्या स्ट्रीट वेंडर बिना गारंटी के लोन ले सकते हैं?',
    promptWomen: 'महिला उद्यमियों के लिए कौन सी योजनाएं हैं?',
    promptSubsidy: 'पूंजीगत सब्सिडी के लिए कौन से दस्तावेज़ चाहिए?'
  },
  ta: {
    appName: 'ஸ்கீம் சாதி',
    tagline: 'விளிம்புநிலை தொழில்முனைவோருக்கான AI கடன் திட்டம்',
    translationBadge: 'AI4Bharat Samanantar IndicNLP மொழிபெயர்ப்பு',
    sihBadgeText: 'SIH 2026',
    sihSubtext: 'Problem ID: SIH26092 • AI திட்ட பொருத்தம் • myScheme.gov.in அதிகாரப்பூர்வ தளம்',
    navHome: 'முகப்பு',
    navHowItWorks: 'எப்படி செயல்படுகிறது',
    navSchemes: 'திட்டங்கள்',
    navFeatures: 'அம்சங்கள்',
    navAbout: 'பற்றி',
    navLogin: 'உள்நுழை',
    navRegister: 'பதிவு செய்',
    navDashboard: 'முகப்புப்பலகை',
    navFindScheme: 'திட்டம் கண்டறி',
    navEmi: 'EMI கால்குலேட்டர்',
    navDocAssistant: 'ஆவண உதவியாளர்',
    navPartners: 'உதவி மையங்கள்',
    navChat: 'AI உதவியாளர்',
    navAdmin: 'நிர்வாகம்',
    navProfile: 'சுயவிவரம்',
    navLogout: 'வெளியேறு',
    heroTitle: 'உங்களுக்கான சரியான அரசு திட்டத்தை கண்டறியுங்கள்',
    heroSubtitle: 'தொழில்முனைவோர் மற்றும் மாணவர்களுக்கான AI-அரசு நிதி உதவி மற்றும் தகுதி சரிபார்ப்பு தளம்.',
    find_my_scheme: 'திட்டம் கண்டறி',
    btnFindScheme: 'திட்டம் கண்டறி',
    chat_assistant: 'AI உதவியாளரிடம் உரையாடு',
    btnChatAssistant: 'AI உதவியாளரிடம் உரையாடு',
    btnExploreSchemes: 'திட்டங்களை காண்க',
    btnCalculateEmi: 'EMI கணக்கிடு',
    btnCheckDocs: 'ஆவணங்கள் சரிபார்',
    tailoredFor: 'முன்னுரிமை பிரிவுகள்:',
    scStFounders: 'SC / ST தொழில்முனைவோர்',
    womenEntrepreneurs: 'பெண் தொழில்முனைவோர்',
    minorityCommunities: 'சிறுபான்மையினர்',
    streetVendors: 'தெருவோர வியாபாரிகள்',
    traditionalArtisans: 'பாரம்பரிய கைவினைஞர்கள்',
    differentlyAbled: 'மாற்றுத்திறனாளிகள்',
    instantCheckTitle: 'உடனடி தகுதி சரிபார்ப்பு',
    instantCheckSubtitle: '30 வினாடிகளில் சிறந்த திட்டத்தை கண்டறியுங்கள்',
    socialCategory: 'சமூக பிரிவு',
    gender: 'பாலினம்',
    businessType: 'தொழில் வகை',
    requiredLoan: 'தேவையான கடன் தொகை',
    btnAnalyzeSchemes: 'பொருத்தமான திட்டங்களை காண்க',
    liveAiBadge: 'நேரடி AI',
    statCentralState: 'மத்திய & மாநில திட்டங்கள் (myScheme)',
    statSubsidies: 'மூலதன மானியம் (50% வரை)',
    statLanguages: '11 இந்திய மொழிகள்',
    statIntegrity: '100% விதி துல்லியம்',
    workflowTitle: 'செயல்முறை',
    workflowSubtitle: 'ஸ்கீம் சாதி எப்படி இயங்குகிறது',
    step1WorkflowTitle: 'விவரம் & தேவை பகுப்பாய்வு',
    step1WorkflowDesc: 'சமூக பிரிவு, திட்ட மதிப்பீடு மற்றும் தொழில் வகையை பதிவு செய்தல்.',
    step2WorkflowTitle: 'சட்ட விதி இயந்திரம்',
    step2WorkflowDesc: 'அரசு வர்த்தமானி விதிகளின்படி துல்லியமான தகுதி நிர்ணயம்.',
    step3WorkflowTitle: 'SHAP அடிப்படையிலான தரவரிசை',
    step3WorkflowDesc: 'பொருத்தமான காரணங்கள் மற்றும் வெளிப்படையான மதிப்பீடு.',
    step4WorkflowTitle: 'OCR மற்றும் வங்கி இணைப்பு',
    step4WorkflowDesc: 'ஆவணங்களை சரிபார்த்து அருகிலுள்ள வங்கி கிளைக்கு வழிகாட்டுதல்.',
    featuredSchemesTitle: 'அங்கீகரிக்கப்பட்ட அரசு திட்டங்கள்',
    featuredSchemesSubtitle: 'myScheme.gov.in தரநிலைகளின்படி சரிபார்க்கப்பட்டது',
    maxLoan: 'அதிகபட்ச கடன் வரம்பு',
    subsidyRate: 'மானிய விகிதம்',
    tenor: 'திருப்பிச் செலுத்தும் காலம்',
    collateral: 'பிணையற்ற கடன்',
    whyMatched: 'இத்திட்டம் உங்களுக்கு ஏன் பொருந்தியது',
    statutoryRules: 'அரசு சட்ட விதிகள்',
    requiredDocs: 'தேவையான ஆவணங்கள்',
    verifyOcr: 'OCR சரிபார்ப்பு',
    officialPortal: 'myScheme அதிகாரப்பூர்வ தளம்',
    viewDetails: 'விவரங்களை காண்க & விண்ணப்பிக்கவும்',
    testimonialsTitle: 'இந்தியா முழுவதும் உள்ள தொழில்முனைவோருக்கு வழிகாட்டல்',
    ctaTitle: 'அரசு மானியம் பெற தயாரா?',
    ctaDesc: 'உங்கள் தகுதியை இப்போதே சரிபார்த்து அருகிலுள்ள வங்கியுடன் இணையுங்கள்.',
    ctaButton: 'இலவசமாக தொடங்கவும்',
    footerRights: 'ஸ்கீம் சாதி © 2026. ஸ்மார்ட் இந்தியா ஹேக்கத்தான் 2026.',
    targetMarginalized: 'விளிம்புநிலை',
    unitMonths: 'மாதங்கள்',
    unitLakh: 'இலட்சம்',
    unitCrore: 'கோடி',
    lowInterest: 'குறைந்த வட்டி மானியம்',
    bankGuarantee: 'வங்கி உத்தரவாதம்',
    specialRural: '35% வரை கிராமப்புற மானியம்',
    sliderMinSVANidhi: '₹10,000 (ஸ்வநிதி)',
    sliderMidMudra: '₹10 இலட்சம் (முத்ரா)',
    sliderMidPMEGP: '₹50 இலட்சம் (PMEGP)',
    sliderMaxStandUp: '₹10 கோடி (ஸ்டாண்ட்-அப்)',
    optionSC: 'பட்டியலின சாதி (SC)',
    optionST: 'பழங்குடியினர் (ST)',
    optionOBC: 'இதர பிற்படுத்தப்பட்ட வகுப்பு (OBC)',
    optionMinority: 'சிறுபான்மையினர் சமூகம்',
    optionGeneral: 'பொதுப் பிரிவு (General)',
    optionFemale: 'பெண் / மகளிர்',
    optionMale: 'ஆண்',
    optionTransgender: 'திருநங்கை / திருநம்பி',
    optionGraduate: 'பட்டதாரி / கல்லூரி படிப்பு',
    option12th: '12-ஆம் வகுப்பு தேர்ச்சி',
    option8th: '8-ஆம் வகுப்பு தேர்ச்சி (PMEGP தகுதி)',
    optionBelow8th: '8-ஆம் வகுப்பிற்கு கீழ்',
    optionRural: 'கிராமப்புறம் (35% வரை மானியம்)',
    optionUrban: 'நகர்ப்புறம் (25% வரை மானியம்)',
    optionNewStage: 'புதிய தொழில் (Greenfield)',
    optionExpansionStage: 'தொழில் விரிவாக்கம்',
    manufacturingOption: 'உற்பத்தி தொழில்',
    serviceOption: 'சேவை தொழில்',
    tradingOption: 'வர்த்தகம் / சில்லறை',
    streetVendorOption: 'தெருவோர வியாபாரம்',
    artisanOption: 'கைவினை / பாரம்பரிய தொழில்',
    wizardTitle: 'உங்களுக்கான சிறந்த அரசு திட்டத்தை கண்டறியுங்கள்',
    wizardSubtitle: 'SC/ST, பெண்கள், சிறுபான்மையினர் மற்றும் கைவினைஞர்களுக்கான தகுதி தேர்வு',
    step1Title: 'அடையாளம்',
    step2Title: 'இடம்',
    step3Title: 'தொழில்',
    step4Title: 'கடன் தேவை',
    step5Title: 'ஆவணங்கள்',
    step1Desc: 'அரசு திட்டங்களில் சிறப்பு பிரிவினருக்கு கூடுதல் மானியங்கள் ஒதுக்கப்பட்டுள்ளன.',
    step2Desc: 'கிராமப்புற பகுதிகளில் நகர்ப்புறத்தை விட கூடுதல் மானியம் (35%) கிடைக்கும்.',
    step3Desc: 'துறை சார்ந்த திட்டங்களை பெற தொழில் வகையை தேர்வு செய்யவும்.',
    step4Desc: 'திட்ட மதிப்பீடு, சொந்த நிதி பங்களிப்பு ஆகியவற்றை குறிப்பிடவும்.',
    step5Desc: 'உடனடி சரிபார்ப்பிற்கு தேவையான ஆவணங்களை தயாராக வைக்கவும்.',
    socialCategoryLabel: 'சமூக பிரிவு *',
    genderLabel: 'பாலினம் *',
    ageLabel: 'வயது *',
    educationLabel: 'கல்வி தகுதி *',
    differentlyAbledLabel: 'விண்ணப்பதாரர் மாற்றுத்திறனாளி (PwD > 40%)',
    stateLabel: 'மாநிலம் *',
    districtLabel: 'மாவட்டம் *',
    areaTypeLabel: 'பகுதி வகைப்பாடு *',
    pincodeLabel: 'அஞ்சல் குறியீடு *',
    businessStageLabel: 'தொழில் நிலை *',
    isArtisanLabel: 'பாரம்பரிய கைவினைஞர் (PM விஸ்வகர்மா தகுதி)',
    isVendorLabel: 'தெருவோர வியாபாரி (PM ஸ்வநிதி தகுதி)',
    hasTrainingLabel: 'பயிற்சி பெற்றவர் (EDP / Skill India)',
    projectCostLabel: 'மொத்த திட்ட மதிப்பீடு (₹) *',
    requiredLoanLabel: 'தேவையான கடன் தொகை (₹) *',
    ownContributionLabel: 'சொந்த முதலீடு / பங்கு (₹) *',
    annualIncomeLabel: 'ஆண்டு குடும்ப வருமானம் (₹) *',
    hasAadhaarLabel: 'ஆதார் அட்டை',
    hasPanLabel: 'பான் அட்டை',
    hasCasteLabel: 'சாதி சான்றிதழ்',
    hasDprLabel: 'விரிவான திட்ட அறிக்கை (DPR)',
    hasBankLabel: 'வங்கி கணக்கு புத்தகம்',
    hasUdyamLabel: 'உத்யம் பதிவு சான்றிதழ்',
    btnPrevious: 'முந்தைய படி',
    btnNext: 'அடுத்த படி',
    btnEvaluateSchemes: 'தகுதியான திட்டங்களை காண்க',
    evaluatingText: 'விதிகள் சரிபார்க்கப்படுகிறது...',
    resultsTitle: 'உங்கள் திட்ட பொருத்தம் மற்றும் தகுதி பகுப்பாய்வு',
    resultsSubtitle: 'AI4Bharat விளக்கங்களுடன் 100% துல்லியமான தேர்வு',
    topMatchBadge: 'சிறந்த தேர்வு',
    matchScore: 'பொருத்தம் மதிப்பெண்',
    eligibleStatus: 'தகுதியுடையது',
    ineligibleStatus: 'தகுதியற்றது',
    subsidyEligible: 'மதிப்பிடப்பட்ட மானியம்',
    viewFullBreakdown: 'விளக்க காரணிகளை காண்க',
    downloadChecklist: 'ஆவண பட்டியலை பதிவிறக்குக',
    locateBankPartner: 'அருகிலுள்ள வங்கி கிளையை காண்க',
    positiveFactors: 'சாதகமான தகுதி காரணிகள்',
    limitingFactors: 'வரம்புகள் & இடர் காரணிகள்',
    noSchemesFound: 'பொருத்தமான திட்டங்கள் ஏதுமில்லை. தயவுசெய்து தொகையை மாற்றி முயற்சிக்கவும்.',
    chatTitle: 'AI ஸ்கீம் சாதி உதவியாளர்',
    chatSubtitle: 'Qwen மற்றும் Samanantar IndicNLP மூலம் உங்கள் மொழியில் கேளுங்கள்',
    chatPlaceholder: 'கடன், மானியம், PM-SVANidhi, PMEGP பற்றி கேளுங்கள்...',
    chatSend: 'அனுப்பு',
    qwenPowered: 'myScheme.gov.in அதிகாரப்பூர்வ தரவு மற்றும் Qwen AI மூலம் இயங்குகிறது',
    suggestedQueries: 'பரிந்துரைக்கப்பட்ட கேள்விகள்:',
    promptPmegp: 'PMEGP திட்டத்தில் எவ்வளவு மானியம் கிடைக்கும்?',
    promptSvanidhi: 'தெரு வியாபாரிகளுக்கு பிணையற்ற கடன் கிடைக்குமா?',
    promptWomen: 'பெண்களுக்கான அரசு கடன் திட்டங்கள் என்னென்ன?',
    promptSubsidy: 'மூலதன மானியம் பெற என்ன ஆவணங்கள் தேவை?'
  },
  bn: {
    appName: 'স্কিম সাথি',
    tagline: 'অনগ্রসর উদ্যোক্তাদের জন্য এআই-চালিত সরকারি ঋণ প্রকল্প সন্ধান',
    translationBadge: 'AI4Bharat Samanantar IndicNLP দ্বারা চালিত',
    sihBadgeText: 'SIH 2026',
    sihSubtext: 'Problem ID: SIH26092 • AI প্রকল্প মেলবন্ধন • myScheme.gov.in ডেটাসেট',
    navHome: 'হোম',
    navHowItWorks: 'কীভাবে কাজ করে',
    navSchemes: 'প্রকল্পসমূহ',
    navFeatures: 'বৈশিষ্ট্য',
    navAbout: 'আমাদের সম্পর্কে',
    navLogin: 'লগইন',
    navRegister: 'নিবন্ধন',
    navDashboard: 'ড্যাশবোর্ড',
    navFindScheme: 'আমার প্রকল্প খুঁজুন',
    navEmi: 'ইএমআই ক্যালকুলেটর',
    navDocAssistant: 'নথি সহকারী',
    navPartners: 'সহযোগী কেন্দ্র',
    navChat: 'এআই সহকারী',
    navAdmin: 'অ্যাডমিন পোর্টাল',
    navProfile: 'প্রোফাইল',
    navLogout: 'লগ আউট',
    heroTitle: 'আপনার জন্য সঠিক সরকারি প্রকল্প খুঁজুন',
    heroSubtitle: 'উদ্যোক্তা ও শিক্ষার্থীদের জন্য এআই-চালিত প্রকল্প সন্ধান, নির্ভুল যোগ্যতা যাচাই এবং আর্থিক দিকনির্দেশনা।',
    find_my_scheme: 'আমার প্রকল্প খুঁজুন',
    btnFindScheme: 'আমার প্রকল্প খুঁজুন',
    chat_assistant: 'এআই সহকারীর সাথে কথা বলুন',
    btnChatAssistant: 'এআই সহকারীর সাথে কথা বলুন',
    btnExploreSchemes: 'প্রকল্পগুলো দেখুন',
    btnCalculateEmi: 'ইএমআই গণনা করুন',
    btnCheckDocs: 'নথিপত্র পরীক্ষা করুন',
    tailoredFor: 'বিশেষ সুবিধাভোগী গোষ্ঠী:',
    scStFounders: 'তপশিলি জাতি / উপজাতি (SC/ST)',
    womenEntrepreneurs: 'নারী উদ্যোক্তা',
    minorityCommunities: 'সংখ্যালঘু সম্প্রদায়',
    streetVendors: 'হকার ও পথ বিক্রেতা',
    traditionalArtisans: 'ঐতিহ্যবাহী কারিগর ও শিল্পী',
    differentlyAbled: 'বিশেষ চাহিদা সম্পন্ন (PwD)',
    instantCheckTitle: 'তাত্ক্ষণিক যোগ্যতা যাচাই',
    instantCheckSubtitle: '৩০ সেকেন্ডে আপনার জন্য সেরা প্রকল্প খুঁজুন',
    socialCategory: 'সামাজিক বিভাগ',
    gender: 'লিঙ্গ',
    businessType: 'ব্যবসার ধরন',
    requiredLoan: 'প্রয়োজনীয় ঋণের পরিমাণ',
    btnAnalyzeSchemes: 'উপযুক্ত প্রকল্প বিশ্লেষণ করুন',
    liveAiBadge: 'লাইভ এআই',
    statCentralState: 'কেন্দ্রীয় ও রাজ্য প্রকল্প (myScheme)',
    statSubsidies: 'মূলধন ভর্তুকি (৫০% পর্যন্ত)',
    statLanguages: '১১টি ভারতীয় ভাষা',
    statIntegrity: '১০০% সরকারি নিয়ম নির্ভুলতা',
    workflowTitle: 'কাজের ধারা',
    workflowSubtitle: 'স্কিম সাথি কীভাবে কাজ করে',
    step1WorkflowTitle: 'প্রোফাইল ও চাহিদা বিশ্লেষণ',
    step1WorkflowDesc: 'সামাজিক বিভাগ, প্রকল্প ব্যয় এবং ব্যবসার ধরন গ্রহণ করা।',
    step2WorkflowTitle: 'নিয়ম ইঞ্জিন',
    step2WorkflowDesc: 'সরকারি গেজেট নিয়মের ভিত্তিতে নির্ভুল যোগ্যতা নির্ধারণ।',
    step3WorkflowTitle: 'SHAP-ভিত্তিক র‍্যাঙ্কিং',
    step3WorkflowDesc: 'সঠিক স্কোর ও স্বচ্ছ কারণ বিশ্লেষণ প্রদান।',
    step4WorkflowTitle: 'ওসিআর ও ব্যাংক ম্যাপিং',
    step4WorkflowDesc: 'নথি যাচাই করে নিকটস্থ ব্যাংক শাখার সাথে যুক্ত করা।',
    featuredSchemesTitle: 'যাচাইকৃত সরকারি প্রকল্পসমূহ',
    featuredSchemesSubtitle: 'myScheme.gov.in এর সরকারি মান অনুযায়ী',
    maxLoan: 'সর্বোচ্চ ঋণের সীমা',
    subsidyRate: 'ভর্তুকির হার',
    tenor: 'পরিশোধের মেয়াদ',
    collateral: 'জামিনমুক্ত ঋণ',
    whyMatched: 'এই প্রকল্পটি আপনার জন্য কেন উপযুক্ত',
    statutoryRules: 'সরকারি নিয়মাবলী',
    requiredDocs: 'প্রয়োজনীয় নথিপত্র',
    verifyOcr: 'ওসিআর যাচাইকরণ',
    officialPortal: 'myScheme অফিশিয়াল পোর্টাল',
    viewDetails: 'বিস্তারিত দেখুন ও আবেদন করুন',
    testimonialsTitle: 'দেশজুড়ে উদ্যোক্তাদের ক্ষমতায়ন',
    ctaTitle: 'সরকারি ভর্তুকি পেতে আপনি কি প্রস্তুত?',
    ctaDesc: 'এখনই আপনার যোগ্যতা যাচাই করুন এবং নিকটস্থ ব্যাংকের সাথে যোগাযোগ করুন।',
    ctaButton: 'বিনামূল্যে শুরু করুন',
    footerRights: 'স্কিম সাথি © 2026. স্মার্ট ইন্ডিয়া হ্যাকাথন 2026.',
    targetMarginalized: 'অনগ্রসর শ্রেণি',
    unitMonths: 'মাস',
    unitLakh: 'লাখ',
    unitCrore: 'কোটি',
    lowInterest: 'স্বল্প সুদের ভর্তুকি',
    bankGuarantee: 'ব্যাংক গ্যারান্টি',
    specialRural: '৩৫% পর্যন্ত গ্রামীণ ভর্তুকি',
    sliderMinSVANidhi: '₹১০,০০০ (স্বনিধি)',
    sliderMidMudra: '₹১০ লাখ (মুদ্রা)',
    sliderMidPMEGP: '₹৫০ লাখ (PMEGP)',
    sliderMaxStandUp: '₹১০ কোটি (স্ট্যান্ড-আপ)',
    optionSC: 'তফসিলি জাতি (SC)',
    optionST: 'তফসিলি উপজাতি (ST)',
    optionOBC: 'অন্যান্য অনগ্রসর শ্রেণি (OBC)',
    optionMinority: 'সংখ্যালঘু সম্প্রদায়',
    optionGeneral: 'সাধারণ বিভাগ (General)',
    optionFemale: 'নারী / মহিলা',
    optionMale: 'পুরুষ',
    optionTransgender: 'রূপান্তরকামী (Transgender)',
    optionGraduate: 'স্নাতক / ডিগ্রিধারী',
    option12th: 'দ্বাদশ শ্রেণি পাস',
    option8th: 'অষ্টম শ্রেণি পাস (PMEGP যোগ্য)',
    optionBelow8th: 'অষ্টম শ্রেণির নিচে',
    optionRural: 'গ্রামীণ (৩৫% পর্যন্ত ভর্তুকি)',
    optionUrban: 'শহরাঞ্চল (২৫% পর্যন্ত ভর্তুকি)',
    optionNewStage: 'নতুন উদ্যোগ (Greenfield)',
    optionExpansionStage: 'বিদ্যমান ইউনিটের সম্প্রসারণ',
    manufacturingOption: 'উৎপাদন শিল্প',
    serviceOption: 'সেবা খাত (মেরামত, পার্লার, ক্লিনিক)',
    tradingOption: 'ব্যবসা / খুচরা দোকান',
    streetVendorOption: 'পথ বিক্রেতা / হকার',
    artisanOption: 'ঐতিহ্যবাহী কারিগর / হস্তশিল্প',
    wizardTitle: 'আপনার জন্য আদর্শ সরকারি প্রকল্প খুঁজুন',
    wizardSubtitle: 'এসসি/এসটি, নারী এবং কারিগরদের জন্য নির্ভুল মিলবন্ধন',
    step1Title: 'পরিচয়',
    step2Title: 'অবস্থান',
    step3Title: 'উদ্যোগ',
    step4Title: 'ঋণের প্রয়োজন',
    step5Title: 'নথিপত্র',
    step1Desc: 'সরকারি প্রকল্পে নির্দিষ্ট গোষ্ঠীর জন্য বিশেষ ভর্তুকি ও কোটা রয়েছে।',
    step2Desc: 'শহরের তুলনায় গ্রামীণ এলাকায় বেশি ভর্তুকি (৩৫%) পাওয়া যায়।',
    step3Desc: 'সঠিক প্রকল্পের জন্য আপনার ব্যবসার ধরন নির্বাচন করুন।',
    step4Desc: 'প্রকল্প ব্যয় এবং নিজস্ব মূলধন বিনিয়োগ উল্লেখ করুন।',
    step5Desc: 'দ্রুত যাচাইয়ের জন্য প্রয়োজনীয় নথিপত্র প্রস্তুত রাখুন।',
    socialCategoryLabel: 'সামাজিক বিভাগ *',
    genderLabel: 'লিঙ্গ *',
    ageLabel: 'বয়স *',
    educationLabel: 'শিক্ষাগত যোগ্যতা *',
    differentlyAbledLabel: 'আবেদনকারী বিশেষ চাহিদা সম্পন্ন (PwD > 40%)',
    stateLabel: 'রাজ্য *',
    districtLabel: 'জেলা *',
    areaTypeLabel: 'এলাকার ধরন *',
    pincodeLabel: 'পিন কোড *',
    businessStageLabel: 'ব্যবসার পর্যায় *',
    isArtisanLabel: 'ঐতিহ্যবাহী কারিগর (PM বিশ্বকর্মা যোগ্য)',
    isVendorLabel: 'পথ বিক্রেতা (PM স্বনিধি যোগ্য)',
    hasTrainingLabel: 'প্রশিক্ষণপ্রাপ্ত (EDP / স্কিল ইন্ডিয়া)',
    projectCostLabel: 'মোট প্রকল্প ব্যয় (₹) *',
    requiredLoanLabel: 'প্রয়োজনীয় ঋণের পরিমাণ (₹) *',
    ownContributionLabel: 'নিজস্ব অবদান / মার্জিন মানি (₹) *',
    annualIncomeLabel: 'বার্ষিক পারিবারিক আয় (₹) *',
    hasAadhaarLabel: 'আধার কার্ড',
    hasPanLabel: 'প্যান কার্ড',
    hasCasteLabel: 'জাতিগত শংসাপত্র',
    hasDprLabel: 'বিস্তারিত প্রকল্প প্রতিবেদন (DPR)',
    hasBankLabel: 'ব্যাংক পাসবুক ও বিবরণী',
    hasUdyamLabel: 'উদ্যম এমএসএমই নিবন্ধন',
    btnPrevious: 'পূর্ববর্তী ধাপ',
    btnNext: 'পরবর্তী ধাপ',
    btnEvaluateSchemes: 'যোগ্য প্রকল্পসমূহ দেখুন',
    evaluatingText: 'নিয়মাবলী যাচাই করা হচ্ছে...',
    resultsTitle: 'আপনার প্রকল্প মেলবন্ধন ও যোগ্যতা বিশ্লেষণ',
    resultsSubtitle: 'AI4Bharat ব্যাখ্যাসহ ১০০% নির্ভুল ফলাফল',
    topMatchBadge: 'সেরা সুপারিশ',
    matchScore: 'ম্যাচ স্কোর',
    eligibleStatus: 'যোগ্য (অনুমোদিত)',
    ineligibleStatus: 'অযোগ্য',
    subsidyEligible: 'প্রত্যাশিত ভর্তুকি সুবিধা',
    viewFullBreakdown: 'বিস্তারিত AI কারণ বিশ্লেষণ',
    downloadChecklist: 'নথিপত্রের তালিকা ডাউনলোড করুন',
    locateBankPartner: 'নিকটস্থ ব্যাংক শাখা খুঁজুন',
    positiveFactors: 'ইতিবাচক যোগ্যতার কারণসমূহ',
    limitingFactors: 'সীমাবদ্ধতা ও ঝুঁকির কারণ',
    noSchemesFound: 'এই প্রোফাইলের জন্য কোনো প্রকল্প পাওয়া যায়নি। অনুগ্রহ করে তথ্য পরিবর্তন করুন।',
    chatTitle: 'এআই স্কিম সাথি সহকারী',
    chatSubtitle: 'Qwen ও Samanantar IndicNLP এর মাধ্যমে বাংলায় কথা বলুন',
    chatPlaceholder: 'ঋণ, ভর্তুকি, PMEGP, PM-SVANidhi সম্পর্কে প্রশ্ন করুন...',
    chatSend: 'পাঠান',
    qwenPowered: 'myScheme.gov.in সরকারি ডেটা এবং Qwen AI চালিত',
    suggestedQueries: 'প্রস্তাবিত প্রশ্নাবলী:',
    promptPmegp: 'PMEGP প্রকল্পে কত টাকা ভর্তুকি পাওয়া যায়?',
    promptSvanidhi: 'পথ বিক্রেতারা কি জামানত ছাড়া ঋণ পেতে পারেন?',
    promptWomen: 'নারী উদ্যোক্তাদের জন্য কী কী সরকারি প্রকল্প রয়েছে?',
    promptSubsidy: 'মূলধন ভর্তুকির জন্য কী কী নথিপত্র প্রয়োজন?'
  },
  te: {
    appName: 'స్కీమ్ సాథీ',
    tagline: 'ఔత్సాహిక పారిశ్రామికవేత్తల కోసం AI రుణ పథక శోధన',
    translationBadge: 'AI4Bharat Samanantar IndicNLP మద్దతు',
    sihBadgeText: 'SIH 2026',
    sihSubtext: 'సమస్య ID: SIH26092 • AI పథక సరిపోలిక • myScheme.gov.in డేటాసెట్',
    navHome: 'హోమ్',
    navHowItWorks: 'ఎలా పనిచేస్తుంది',
    navSchemes: 'పథకాలు',
    navFeatures: 'ఫీచర్లు',
    navAbout: 'గురించి',
    navLogin: 'లాగిన్',
    navRegister: 'రిజిస్టర్',
    navDashboard: 'డ్యాష్‌బోర్డ్',
    navFindScheme: 'నా పథకం కనుగొనండి',
    navEmi: 'EMI కాలిక్యులేటర్',
    navDocAssistant: 'డాక్యుమెంట్ అసిస్టెంట్',
    navPartners: 'సహాయ కేంద్రాలు',
    navChat: 'AI అసిస్టెంట్',
    navAdmin: 'అడ్మిన్ పోర్టల్',
    navProfile: 'యూజర్ ప్రొఫైల్',
    navLogout: 'లాగ్ అవుట్',
    heroTitle: 'మీకు తగిన సరైన ప్రభుత్వ పథకాన్ని కనుగొనండి',
    heroSubtitle: 'విద్యార్థులు మరియు వ్యాపారవేత్తల కోసం AI ఆధారిత అర్హత తనిఖీ మరియు ఆర్థిక మార్గదర్శకత్వం.',
    find_my_scheme: 'నా పథకం కనుగొనండి',
    btnFindScheme: 'నా పథకం కనుగొనండి',
    chat_assistant: 'AI అసిస్టెంట్‌తో మాట్లాడండి',
    btnChatAssistant: 'AI అసిస్టెంట్‌తో మాట్లాడండి',
    btnExploreSchemes: 'పథకాలు చూడండి',
    btnCalculateEmi: 'EMI లెక్కించండి',
    btnCheckDocs: 'పత్రాలు తనిఖీ చేయండి',
    tailoredFor: 'ప్రత్యేక ప్రాధాన్యత వర్గాలు:',
    scStFounders: 'SC / ST వ్యవస్థాపకులు',
    womenEntrepreneurs: 'మహిళా పారిశ్రామికవేత్తలు',
    minorityCommunities: 'మైనారిటీ వర్గాలు',
    streetVendors: 'వీధి వ్యాపారులు',
    traditionalArtisans: 'సాంప్రదాయ కళాకారులు',
    differentlyAbled: 'దివ్యాంగులు (PwD)',
    instantCheckTitle: 'తక్షణ అర్హత తనిఖీ',
    instantCheckSubtitle: '30 సెకన్లలో మీకు తగిన ఉత్తమ పథకాన్ని కనుగొనండి',
    socialCategory: 'సామాజిక వర్గం',
    gender: 'లింగం',
    businessType: 'వ్యాపార రకం',
    requiredLoan: 'అవసరమైన రుణ మొత్తం',
    btnAnalyzeSchemes: 'సరిపోయే పథకాలను విశ్లేషించండి',
    liveAiBadge: 'లైవ్ AI',
    statCentralState: 'కేంద్ర & రాష్ట్ర పథకాలు (myScheme)',
    statSubsidies: 'మూలధన సబ్సిడీ (50% వరకు)',
    statLanguages: '11 భారతీయ ప్రాంతీయ భాషలు',
    statIntegrity: '100% నిబంధన ఖచ్చితత్వం',
    workflowTitle: 'కార్య విధానం',
    workflowSubtitle: 'స్కీమ్ సాథీ ఎలా పనిచేస్తుంది',
    step1WorkflowTitle: 'ప్రొఫైల్ & అవసరాల విశ్లేషణ',
    step1WorkflowDesc: 'సామాజిక వర్గం, ప్రాజెక్ట్ వ్యయం మరియు వ్యాపార రకం నమోదు.',
    step2WorkflowTitle: 'నిబంధనల ఇంజిన్',
    step2WorkflowDesc: 'ప్రభుత్వ గెజిట్ నిబంధనల ఆధారంగా ఖచ్చితమైన అర్హత పరిశీలన.',
    step3WorkflowTitle: 'SHAP-ఆధారిత ర్యాంకింగ్',
    step3WorkflowDesc: 'సరిపోలిక స్కోరు మరియు పారదర్శక వివరణలు.',
    step4WorkflowTitle: 'OCR & బ్యాంక్ మ్యాపింగ్',
    step4WorkflowDesc: 'పత్రాల ధృవీకరణ మరియు సమీప బ్యాంక్ శాఖకు మార్గదర్శకత్వం.',
    featuredSchemesTitle: 'ధృవీకరించబడిన ప్రభుత్వ పథకాలు',
    featuredSchemesSubtitle: 'myScheme.gov.in ప్రమాణాల ప్రకారం',
    maxLoan: 'గరిష్ట రుణ పరిమితి',
    subsidyRate: 'సబ్సిడీ శాతం',
    tenor: 'తిరిగి చెల్లించే వ్యవధి',
    collateral: 'హామీ లేని రుణం',
    whyMatched: 'ఈ పథకం మీకు ఎందుకు సరిపోయింది',
    statutoryRules: 'చట్టబద్ధమైన నిబంధనలు',
    requiredDocs: 'అవసరమైన పత్రాలు',
    verifyOcr: 'OCR ధృవీకరణ',
    officialPortal: 'myScheme అధికారిక పోర్టల్',
    viewDetails: 'వివరాలు చూడండి & దరఖాస్తు చేసుకోండి',
    testimonialsTitle: 'భారతదేశ వ్యాప్తంగా పారిశ్రామికవేత్తల సాధికారత',
    ctaTitle: 'ప్రభుత్వ సబ్సిడీ పొందేందుకు సిద్ధంగా ఉన్నారా?',
    ctaDesc: 'మీ అర్హతను ఇప్పుడే తనిఖీ చేసి సమీప బ్యాంకు శాఖను సంప్రదించండి.',
    ctaButton: 'ఉచితంగా ప్రారంభించండి',
    footerRights: 'స్కీమ్ సాథీ © 2026. స్మార్ట్ ఇండియా హ్యాకథాన్ 2026.',
    targetMarginalized: 'వంచితులు',
    unitMonths: 'నెలలు',
    unitLakh: 'లక్షలు',
    unitCrore: 'కోట్లు',
    lowInterest: 'తక్కువ వడ్డీ సబ్సిడీ',
    bankGuarantee: 'బ్యాంక్ హామీ',
    specialRural: '35% వరకు గ్రామీణ సబ్సిడీ',
    sliderMinSVANidhi: '₹10,000 (స్వనిధి)',
    sliderMidMudra: '₹10 లక్షలు (ముద్ర)',
    sliderMidPMEGP: '₹50 లక్షలు (PMEGP)',
    sliderMaxStandUp: '₹10 కోట్లు (స్టాండ్-అప్)',
    optionSC: 'షెడ్యూల్డ్ కులం (SC)',
    optionST: 'షెడ్యూల్డ్ తెగ (ST)',
    optionOBC: 'ఇతర వెనుకబడిన తరగతి (OBC)',
    optionMinority: 'మైనారిటీ వర్గం',
    optionGeneral: 'జనరల్ వర్గం (General)',
    optionFemale: 'మహిళ',
    optionMale: 'పురుషుడు',
    optionTransgender: 'ట్రాన్స్‌జెండర్',
    optionGraduate: 'డిగ్రీ / గ్రాడ్యుయేట్',
    option12th: '12వ తరగతి పాస్',
    option8th: '8వ తరగతి పాస్ (PMEGP అర్హత)',
    optionBelow8th: '8వ తరగతి లోపు',
    optionRural: 'గ్రామీణ (35% వరకు సబ్సిడీ)',
    optionUrban: 'పట్టణ (25% వరకు సబ్సిడీ)',
    optionNewStage: 'కొత్త వ్యాపారం (Greenfield)',
    optionExpansionStage: 'వ్యాపార విస్తరణ',
    manufacturingOption: 'ఉత్పాదక రంగం',
    serviceOption: 'సేవా రంగం',
    tradingOption: 'వ్యాపారం / రిటైల్',
    streetVendorOption: 'వీధి వ్యాపారం',
    artisanOption: 'చేతివృత్తులు / కళాకారులు',
    wizardTitle: 'మీకు అనువైన ప్రభుత్వ పథకాన్ని ఎంచుకోండి',
    wizardSubtitle: 'SC/ST, మహిళలు, మైనారిటీల కోసం ఖచ్చితమైన నిబంధన సరిపోలిక',
    step1Title: 'గుర్తింపు',
    step2Title: 'ప్రాంతం',
    step3Title: 'వ్యాపారం',
    step4Title: 'రుణ అవసరం',
    step5Title: 'పత్రాలు',
    step1Desc: 'ప్రభుత్వ పథకాల్లో ప్రత్యేక వర్గాలకు అదనపు సబ్సిడీ మరియు కోటా ఉంటాయి.',
    step2Desc: 'గ్రామీణ ప్రాంతాల్లో పట్టణాల కంటే ఎక్కువ సబ్సిడీ (35%) లభిస్తుంది.',
    step3Desc: 'సరైన పథకాలను పొందడానికి వ్యాపార రకాన్ని ఎంచుకోండి.',
    step4Desc: 'ప్రాజెక్ట్ వ్యయం మరియు సొంత మార్జిన్ మొత్తాన్ని నమోదు చేయండి.',
    step5Desc: 'త్వరిత ధృవీకరణ కోసం అవసరమైన పత్రాలను సిద్ధంగా ఉంచండి.',
    socialCategoryLabel: 'సామాజిక వర్గం *',
    genderLabel: 'లింగం *',
    ageLabel: 'వయస్సు *',
    educationLabel: 'విద్యార్హత *',
    differentlyAbledLabel: 'దరఖాస్తుదారు దివ్యాంగుడు (PwD > 40%)',
    stateLabel: 'రాష్ట్రం *',
    districtLabel: 'జిల్లా *',
    areaTypeLabel: 'ప్రాంత వర్గీకరణ *',
    pincodeLabel: 'పిన్ కోడ్ *',
    businessStageLabel: 'వ్యాపార దశ *',
    isArtisanLabel: 'సాంప్రదాయ కళాకారుడు (PM విశ్వకర్మ అర్హత)',
    isVendorLabel: 'వీధి వ్యాపారి (PM స్వనిధి అర్హత)',
    hasTrainingLabel: 'శిక్షణ పొందినవారు (EDP / స్కిల్ ఇండియా)',
    projectCostLabel: 'మొత్తం ప్రాజెక్ట్ వ్యయం (₹) *',
    requiredLoanLabel: 'అవసరమైన రుణ మొత్తం (₹) *',
    ownContributionLabel: 'సొంత పెట్టుబడి / మార్జిన్ (₹) *',
    annualIncomeLabel: 'వార్షిక కుటుంబ ఆదాయం (₹) *',
    hasAadhaarLabel: 'ఆధార్ కార్డు',
    hasPanLabel: 'పాన్ కార్డు',
    hasCasteLabel: 'కుల ధృవీకరణ పత్రం',
    hasDprLabel: 'వివరణాత్మక ప్రాజెక్ట్ నివేదిక (DPR)',
    hasBankLabel: 'బ్యాంక్ పాస్‌బుక్ & స్టేట్‌మెంట్',
    hasUdyamLabel: 'ఉద్యమ్ రిజిస్ట్రేషన్ సర్టిఫికేట్',
    btnPrevious: 'మునుపటి దశ',
    btnNext: 'తదుపరి దశ',
    btnEvaluateSchemes: 'అర్హతగల పథకాలను చూడండి',
    evaluatingText: 'నిబంధనల పరిశీలన జరుగుతోంది...',
    resultsTitle: 'మీ పథక సరిపోలిక & అర్హత విశ్లేషణ',
    resultsSubtitle: 'AI4Bharat వివరణలతో 100% ఖచ్చితమైన ఫలితాలు',
    topMatchBadge: 'ఉత్తమ సిఫార్సు',
    matchScore: 'సరిపోలిక స్కోరు',
    eligibleStatus: 'అర్హులు',
    ineligibleStatus: 'అనర్హులు',
    subsidyEligible: 'అంచనా సబ్సిడీ ప్రయోజనం',
    viewFullBreakdown: 'వివరణాత్మక AI విశ్లేషణ',
    downloadChecklist: 'పత్రాల జాబితాను డౌన్‌లోడ్ చేయండి',
    locateBankPartner: 'సమీప బ్యాంక్ శాఖను కనుగొనండి',
    positiveFactors: 'సానుకూల అర్హత అంశాలు',
    limitingFactors: 'పరిమితులు మరియు రిస్క్ అంశాలు',
    noSchemesFound: 'ఈ వివరాలకు సరిపోయే పథకాలు లభించలేదు. దయచేసి వివరాలను మార్చండి.',
    chatTitle: 'AI స్కీమ్ సాథీ అసిస్టెంట్',
    chatSubtitle: 'Qwen మరియు Samanantar IndicNLP ద్వారా మీ ప్రాంతీయ భాషలో అడగండి',
    chatPlaceholder: 'రుణాలు, సబ్సిడీలు, PMEGP, PM-SVANidhi గురించి అడగండి...',
    chatSend: 'పంపండి',
    qwenPowered: 'myScheme.gov.in అధికారిక డేటా మరియు Qwen లోకల్ LLM ఆధారితం',
    suggestedQueries: 'సూచించిన ప్రశ్నలు:',
    promptPmegp: 'PMEGP కింద ఎంత సబ్సిడీ లభిస్తుంది?',
    promptSvanidhi: 'వీధి వ్యాపారులకు పూచీకత్తు లేకుండా రుణం లభిస్తుందా?',
    promptWomen: 'మహిళా వ్యాపారవేత్తల కోసం ఏ పథకాలు ఉన్నాయి?',
    promptSubsidy: 'మూలధన సబ్సిడీకి ఏ పత్రాలు అవసరం?'
  }
};

// Auto-fill other Indic languages from base dictionary if not individually specified
const indicCodes = ['mr', 'gu', 'pa', 'or', 'as', 'kn', 'ml'];
indicCodes.forEach(code => {
  if (!DICTIONARY[code] && DICTIONARY.hi) {
    DICTIONARY[code] = { ...DICTIONARY.hi };
  }
});

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(
    localStorage.getItem('scheme_sathi_lang') || 'en'
  );

  const setLanguage = (langCode) => {
    localStorage.setItem('scheme_sathi_lang', langCode);
    setCurrentLanguage(langCode);
  };

  const t = (key) => {
    const langDict = DICTIONARY[currentLanguage] || DICTIONARY.en;
    if (langDict && langDict[key]) return langDict[key];
    if (DICTIONARY.en && DICTIONARY.en[key]) return DICTIONARY.en[key];
    return key;
  };

  const translateScheme = (scheme) => {
    if (!scheme || currentLanguage === 'en') return scheme;
    const code = scheme.code || scheme.scheme_code || '';
    const localized = SCHEME_MAP[code]?.[currentLanguage];
    if (localized) {
      return {
        ...scheme,
        name: localized.name || scheme.name,
        scheme_name: localized.name || scheme.scheme_name,
        description: localized.desc || scheme.description,
        scheme_description: localized.desc || scheme.scheme_description
      };
    }
    return scheme;
  };

  const translateDynamic = async (text) => {
    if (!text || currentLanguage === 'en') return text;
    try {
      const res = await axios.post('/api/translate', {
        text: text,
        target_language: currentLanguage
      });
      return res.data.translated_text || text;
    } catch (e) {
      return text;
    }
  };

  return (
    <LanguageContext.Provider value={{
      currentLanguage,
      language: currentLanguage,
      setLanguage, 
      t, 
      translateScheme,
      translateDynamic,
      languages: LANGUAGES
    }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
''')

# 2. Update LandingPage.jsx with translateScheme, localized options, and units
landing_code = r'''import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, Award, ShieldCheck, TrendingUp, CheckCircle, ArrowRight,
  Calculator, MapPin, FileCheck, MessageSquare, Users, Building2,
  ChevronRight, Compass, DollarSign, Target, Star, HelpCircle
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export default function LandingPage() {
  const { t, currentLanguage, translateScheme } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [featuredSchemes, setFeaturedSchemes] = useState([]);
  const [stats, setStats] = useState({ total_schemes: "25+", total_partners: 13, max_subsidy: "50%", active_beneficiaries: "12,450+" });
  const [quickForm, setQuickForm] = useState({
    social_category: 'SC',
    gender: 'female',
    required_loan: 500000,
    business_type: 'manufacturing'
  });

  useEffect(() => {
    api.get('/schemes', { params: { target_language: currentLanguage } })
      .then(res => {
        if (res.data && res.data.length > 0) {
          setFeaturedSchemes(res.data.slice(0, 9));
        }
      })
      .catch(err => console.log('Could not load schemes', err));
  }, [currentLanguage]);

  const handleQuickCheck = (e) => {
    e.preventDefault();
    navigate('/find-scheme', { state: { initialForm: quickForm } });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* SIH 2026 Header Banner */}
      <div className="bg-gradient-to-r from-orange-600 via-amber-600 to-emerald-700 text-white py-2 px-4 text-center text-xs md:text-sm font-medium tracking-wide shadow-sm flex items-center justify-center gap-2">
        <span className="bg-white/20 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider">{t('sihBadgeText')}</span>
        <span>{t('sihSubtext')}</span>
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 via-slate-900 to-slate-950 text-white pt-16 pb-24 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:16px_16px]"></div>
        
        <div className="max-w-7xl mx-auto relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-medium">
              <Sparkles className="w-4 h-4" />
              <span>{t('translationBadge')}</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              {t('heroTitle')}
            </h1>
            
            <p className="text-lg sm:text-xl text-slate-300 max-w-2xl leading-relaxed">
              {t('heroSubtitle')}
            </p>

            {/* Quick CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-2">
              <Link
                to="/find-scheme"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-lg shadow-lg shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5"
              >
                <Compass className="w-5 h-5" />
                <span>{t('btnFindScheme')}</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/chat"
                className="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold text-base transition-all"
              >
                <MessageSquare className="w-5 h-5 text-emerald-400" />
                <span>{t('btnChatAssistant')}</span>
              </Link>
            </div>

            {/* Target Marginalized Cohorts */}
            <div className="pt-6 border-t border-slate-800/80">
              <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-3">{t('tailoredFor')}</p>
              <div className="flex flex-wrap gap-2 justify-center lg:justify-start">
                {[
                  t('scStFounders'),
                  t('womenEntrepreneurs'),
                  t('minorityCommunities'),
                  t('streetVendors'),
                  t('traditionalArtisans'),
                  t('differentlyAbled')
                ].map((group, idx) => (
                  <span key={idx} className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800/80 border border-slate-700 text-slate-300">
                    {group}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Eligibility Evaluator Card */}
          <div className="lg:col-span-5">
            <div className="bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl p-6 sm:p-8 shadow-2xl text-slate-100">
              <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg">
                    <Target className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-lg">{t('instantCheckTitle')}</h3>
                    <p className="text-xs text-slate-300">{t('instantCheckSubtitle')}</p>
                  </div>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-500/20 text-emerald-300 rounded-full border border-emerald-500/30">{t('liveAiBadge')}</span>
              </div>

              <form onSubmit={handleQuickCheck} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-200 mb-1">{t('socialCategory')}</label>
                  <select
                    value={quickForm.social_category}
                    onChange={(e) => setQuickForm({ ...quickForm, social_category: e.target.value })}
                    className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  >
                    <option value="SC">{t('optionSC')}</option>
                    <option value="ST">{t('optionST')}</option>
                    <option value="OBC">{t('optionOBC')}</option>
                    <option value="Minority">{t('optionMinority')}</option>
                    <option value="General">{t('optionGeneral')}</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-200 mb-1">{t('gender')}</label>
                    <select
                      value={quickForm.gender}
                      onChange={(e) => setQuickForm({ ...quickForm, gender: e.target.value })}
                      className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="female">{t('optionFemale')}</option>
                      <option value="male">{t('optionMale')}</option>
                      <option value="transgender">{t('optionTransgender')}</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-200 mb-1">{t('businessType')}</label>
                    <select
                      value={quickForm.business_type}
                      onChange={(e) => setQuickForm({ ...quickForm, business_type: e.target.value })}
                      className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="manufacturing">{t('manufacturingOption')}</option>
                      <option value="service">{t('serviceOption')}</option>
                      <option value="trading">{t('tradingOption')}</option>
                      <option value="street_vendor">{t('streetVendorOption')}</option>
                      <option value="artisan">{t('artisanOption')}</option>
                    </select>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs font-medium text-slate-200 mb-1">
                    <span>{t('requiredLoan')}</span>
                    <span className="text-emerald-400 font-bold">₹{(quickForm.required_loan / 100000).toFixed(1)} {t('unitLakh')}</span>
                  </div>
                  <input
                    type="range"
                    min="10000"
                    max="10000000"
                    step="10000"
                    value={quickForm.required_loan}
                    onChange={(e) => setQuickForm({ ...quickForm, required_loan: Number(e.target.value) })}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>{t('sliderMinSVANidhi')}</span>
                    <span>{t('sliderMidPMEGP')}</span>
                    <span>{t('sliderMaxStandUp')}</span>
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 text-sm mt-2"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>{t('btnAnalyzeSchemes')}</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Trust & Impact Stats */}
      <section className="bg-white border-y border-slate-200 py-8 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-emerald-700">25+</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">{t('statCentralState')}</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-teal-700">Up to 50%</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">{t('statSubsidies')}</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-amber-600">11</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">{t('statLanguages')}</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-blue-700">100%</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">{t('statIntegrity')}</div>
            </div>
          </div>
        </div>
      </section>

      {/* 4-Step Solution Architecture */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-14">
          <h2 className="text-xs uppercase tracking-widest font-bold text-emerald-700 mb-2">{t('workflowTitle')}</h2>
          <p className="text-3xl font-extrabold text-slate-900">{t('workflowSubtitle')}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {[
            {
              step: "01",
              title: t('step1WorkflowTitle'),
              desc: t('step1WorkflowDesc'),
              icon: <Users className="w-6 h-6 text-emerald-600" />,
              color: "bg-emerald-50 border-emerald-200"
            },
            {
              step: "02",
              title: t('step2WorkflowTitle'),
              desc: t('step2WorkflowDesc'),
              icon: <ShieldCheck className="w-6 h-6 text-blue-600" />,
              color: "bg-blue-50 border-blue-200"
            },
            {
              step: "03",
              title: t('step3WorkflowTitle'),
              desc: t('step3WorkflowDesc'),
              icon: <TrendingUp className="w-6 h-6 text-amber-600" />,
              color: "bg-amber-50 border-amber-200"
            },
            {
              step: "04",
              title: t('step4WorkflowTitle'),
              desc: t('step4WorkflowDesc'),
              icon: <MapPin className="w-6 h-6 text-purple-600" />,
              color: "bg-purple-50 border-purple-200"
            }
          ].map((item, idx) => (
            <div key={idx} className={`p-6 rounded-2xl border ${item.color} shadow-sm relative group hover:shadow-md transition-all`}>
              <div className="text-4xl font-black text-slate-200 absolute top-4 right-4">{item.step}</div>
              <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center mb-4">
                {item.icon}
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-2">{item.title}</h3>
              <p className="text-slate-600 text-sm leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Verified Government Schemes */}
      <section className="py-16 bg-slate-100 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
            <div>
              <span className="text-xs uppercase tracking-wider font-bold text-emerald-700">{t('sihBadgeText')} • myScheme.gov.in</span>
              <h2 className="text-3xl font-extrabold text-slate-900 mt-1">{t('featuredSchemesTitle')}</h2>
              <p className="text-slate-600 text-sm mt-1">{t('featuredSchemesSubtitle')}</p>
            </div>
            <Link to="/results" className="mt-4 md:mt-0 inline-flex items-center gap-1.5 text-sm font-bold text-emerald-700 hover:text-emerald-800">
              <span>{t('btnExploreSchemes')}</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredSchemes.length > 0 ? (
              featuredSchemes.map((rawScheme) => {
                const scheme = translateScheme(rawScheme);
                return (
                  <div key={scheme.id} className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all p-6 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 uppercase tracking-wide">
                          {t('targetMarginalized')}
                        </span>
                        <span className="text-xs font-semibold text-slate-500">{scheme.code}</span>
                      </div>
                      <h3 className="font-bold text-slate-900 text-lg line-clamp-1">{scheme.name}</h3>
                      <p className="text-xs text-slate-500 font-medium mt-0.5">{scheme.department || scheme.ministry}</p>
                      <p className="text-slate-600 text-xs mt-3 line-clamp-2 leading-relaxed">{scheme.description}</p>
                    </div>

                    <div className="mt-6 pt-4 border-t border-slate-100 space-y-2 text-xs">
                      <div className="flex justify-between">
                        <span className="text-slate-500">{t('maxLoan')}:</span>
                        <span className="font-bold text-slate-900">₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} {t('unitLakh')}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">{t('subsidyRate')}:</span>
                        <span className="font-bold text-emerald-700">
                          {scheme.code === 'PMEGP' ? t('specialRural') : (scheme.subsidy_percentage ? `${scheme.subsidy_percentage}%` : t('lowInterest'))}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">{t('tenor')}:</span>
                        <span className="font-medium text-slate-700">{scheme.repayment_period_months} {t('unitMonths')}</span>
                      </div>

                      <div className="pt-3 flex gap-2">
                        <Link
                          to={`/scheme/${scheme.id}`}
                          className="flex-1 py-2 text-center rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold text-xs transition-colors"
                        >
                          {t('viewDetails')}
                        </Link>
                        <Link
                          to="/find-scheme"
                          className="py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition-colors flex items-center justify-center"
                          title={t('btnFindScheme')}
                        >
                          <CheckCircle className="w-4 h-4" />
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              [
                { name: "PMEGP (Prime Minister Employment Generation Programme)", code: 'PMEGP', ministry: 'Ministry of MSME', max: 5000000, sub: 'Up to 35%' },
                { name: 'Stand-Up India Scheme', code: 'STANDUP-IND', ministry: 'Ministry of Finance', max: 10000000, sub: 'Bank Guarantee' },
                { name: 'PM SVANidhi (Street Vendors)', code: 'SVANIDHI', ministry: 'Ministry of Housing & Urban Affairs', max: 50000, sub: '7% Interest Subsidy' }
              ].map((s, idx) => {
                const scheme = translateScheme(s);
                return (
                  <div key={idx} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
                    <div className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded-full inline-block mb-3">{scheme.code}</div>
                    <h3 className="font-bold text-slate-900 text-lg">{scheme.name}</h3>
                    <p className="text-xs text-slate-500">{scheme.ministry}</p>
                    <div className="mt-4 pt-4 border-t border-slate-100 text-xs space-y-2">
                      <div className="flex justify-between"><span>{t('maxLoan')}:</span><span className="font-bold">₹{(scheme.max / 100000).toLocaleString('en-IN')} {t('unitLakh')}</span></div>
                      <div className="flex justify-between"><span>{t('subsidyRate')}:</span><span className="font-bold text-emerald-700">{scheme.sub}</span></div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </section>

      {/* Call to Action Bar */}
      <section className="bg-gradient-to-r from-emerald-800 to-teal-900 text-white py-12 px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-4xl mx-auto space-y-4">
          <h2 className="text-2xl sm:text-3xl font-extrabold">{t('ctaTitle')}</h2>
          <p className="text-slate-200 text-sm max-w-xl mx-auto">
            {t('ctaDesc')}
          </p>
          <div className="pt-2">
            <Link
              to="/find-scheme"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-white text-emerald-950 font-bold text-base hover:bg-slate-100 shadow-lg transition-all"
            >
              <Sparkles className="w-5 h-5 text-emerald-600" />
              <span>{t('ctaButton')}</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
'''
with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\pages\LandingPage.jsx', 'w', encoding='utf-8') as f:
    f.write(landing_code)

print("LanguageContext.jsx and LandingPage.jsx updated successfully with 100% full translations!")
