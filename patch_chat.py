# -*- coding: utf-8 -*-
"""
Patch chat.py to safely handle both Scheme objects and dicts / SimpleNamespace
"""

chat_code = r'''# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from typing import Dict, Any, List, Optional
from app.config import settings

class MultilingualChatService:
    """
    Multilingual Grounded Conversational AI Assistant using Qwen from Ollama,
    with deterministic gazette fallback for 11 Regional Indian Languages:
    English, Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം),
    Marathi (मराठी), Bengali (বাংলা), Gujarati (ગુજરાતી), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ), Assamese (অসমীয়া).
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

    INTENT_RESPONSES = {
        "en": {
            "greeting": "Namaste! I am your AI Scheme Sathi powered by Qwen. I can help you discover government loan schemes and capital subsidies. What type of business or loan are you looking for?",
            "ask_income": "To determine your exact subsidy rate and eligibility, what is your annual family income?",
            "ask_loan_amount": "How much loan amount do you require for your project?",
            "found_schemes": "Here are verified government loan schemes from the official myScheme.gov.in database matching your requirement:",
            "fallback": "I have understood your request. Let us examine the most suitable Central & State schemes for you."
        },
        "hi": {
            "greeting": "नमस्ते! मैं आपका एआई स्कीम साथी हूँ (Qwen संचालित)। मैं आपको सरकारी ऋण योजनाओं और सब्सिडी खोजने में मदद करूँगा। आप किस प्रकार का व्यवसाय शुरू या विस्तारित करना चाहते हैं?",
            "ask_income": "सटीक सब्सिडी और पात्रता के लिए, आपकी वार्षिक पारिवारिक आय कितनी है?",
            "ask_loan_amount": "आपको अपने प्रोजेक्ट के लिए कितने ऋण की आवश्यकता है?",
            "found_schemes": "आपकी आवश्यकताओं के अनुसार myScheme.gov.in की सत्यापित सरकारी योजनाएं:",
            "fallback": "मैंने आपकी बात समझ ली है। आइए आपके लिए सर्वोत्तम सरकारी योजनाएं देखें।"
        },
        "ta": {
            "greeting": "வணக்கம்! நான் உங்கள் ஏஐ திட்டம் சாதி (Qwen). அரசு கடன் திட்டங்கள் மற்றும் மூலதன மானியங்களை கண்டறிய நான் உங்களுக்கு உதவுகிறேன். உங்களுக்கு என்ன தொழில் உதவி தேவை?",
            "ask_income": "துல்லியமான மானியம் மற்றும் தகுதியை அறிய, உங்கள் ஆண்டு குடும்ப வருமானம் என்ன?",
            "ask_loan_amount": "உங்கள் திட்டத்திற்கு எவ்வளவு கடன் தேவைப்படுகிறது?",
            "found_schemes": "உங்கள் தேவைகளுக்கு ஏற்ற myScheme.gov.in அரசு கடன் திட்டங்கள்:",
            "fallback": "உங்கள் தேவையை நான் புரிந்துகொண்டேன். பொருத்தமான திட்டங்களை பார்க்கலாம்."
        },
        "te": {
            "greeting": "నమస్కారం! నేను మీ ఏఐ స్కీమ్ సాథిని (Qwen). ప్రభుత్వ రుణ పథకాలు మరియు సబ్సిడీలను కనుగొనడంలో నేను మీకు సహాయం చేస్తాను. మీకు ఏ వ్యాపార రుణం కావాలి?",
            "ask_income": "ఖచ్చితమైన సబ్సిడీ మరియు అర్హతను నిర్ణయించడానికి, మీ వార్షిక కుటుంబ ఆదాయం ఎంత?",
            "ask_loan_amount": "మీ ప్రాజెక్ట్ కోసం మీకు ఎంత రుణం అవసరం?",
            "found_schemes": "మీ అవసరాలకు సరిపోయే myScheme.gov.in ప్రభుత్వ రుణ పథకాలు:",
            "fallback": "మీ అభ్యర్థనను నేను అర్థం చేసుకున్నాను. సరైన పథకాలను పరిశీలిద్దాం."
        },
        "kn": {
            "greeting": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಎಐ ಸ್ಕೀಮ್ ಸಾಥಿ (Qwen). ಸರ್ಕಾರಿ ಸಾಲ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳನ್ನು ಹುಡುಕಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ನೀವು ಯಾವ ವ್ಯವಹಾರವನ್ನು ಪ್ರಾರಂಭಿಸಲು ಬಯಸುತ್ತೀರಿ?",
            "ask_income": "ನಿಖರವಾದ ಸಬ್ಸಿಡಿ ಮತ್ತು ಅರ್ಹತೆಯನ್ನು ತಿಳಿಯಲು ನಿಮ್ಮ ವಾರ್ಷಿಕ ಕುಟುಂಬದ ಆದಾಯ ಎಷ್ಟು?",
            "ask_loan_amount": "ನಿಮ್ಮ ಯೋಜನೆಗೆ ಎಷ್ಟು ಸಾಲದ ಮೊತ್ತ ಬೇಕಾಗಿದೆ?",
            "found_schemes": "ನಿಮ್ಮ ಅಗತ್ಯಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗುವ myScheme.gov.in ಸರ್ಕಾರಿ ಸಾಲ ಯೋಜನೆಗಳು:",
            "fallback": "ನಿಮ್ಮ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಸೂಕ್ತ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ನೋಡೋಣ."
        },
        "ml": {
            "greeting": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ സ്കീം സാഥി അസിസ്റ്റന്റാണ് (Qwen). സർക്കാർ വായ്പാ പദ്ധതികളും സബ്സിഡികളും കണ്ടെത്താൻ സഹായിക്കാം. ഏത് തരം ബിസിനസ്സ് വായ്പയാണ് താങ്കൾക്ക് ആവശ്യം?",
            "ask_income": "കൃത്യമായ സബ്‌സിഡിയും അർഹതയും അറിയാൻ വാർഷിക കുടുംബ വരുമാനം വ്യക്തമാക്കുക:",
            "ask_loan_amount": "എത്ര തുകയുടെ വായ്പയാണ് താങ്കൾക്ക് ആവശ്യം?",
            "found_schemes": "നിങ്ങളുടെ ആവശ്യത്തിനനുയോജ്യമായ myScheme.gov.in സർക്കാർ വായ്പാ പദ്ധതികൾ:",
            "fallback": "താങ്കളുടെ ആവശ്യം ഞാൻ മനസ്സിലാക്കി. നമുക്ക് പദ്ധതികൾ പരിശോധിക്കാം."
        },
        "mr": {
            "greeting": "नमस्कार! मी तुमचा एआय स्कीम साथी आहे (Qwen द्वारे समर्थित). शासकीय कर्ज योजना व भांडवली अनुदान शोधण्यात मी मदत करू शकेन. तुम्हाला कोणत्या व्यवसायासाठी कर्ज हवे आहे?",
            "ask_income": "अचूक अनुदान व पात्रता ठरवण्यासाठी तुमचे वार्षिक कौटुंबिक उत्पन्न किती आहे?",
            "ask_loan_amount": "तुमच्या प्रकल्पासाठी किती कर्जाची आवश्यकता आहे?",
            "found_schemes": "myScheme.gov.in वरील तुमच्या गरजेनुसार सत्यापित सरकारी योजना:",
            "fallback": "मी आपली विनंती समजून घेतली आहे. आपल्यासाठी सर्वोत्तम योजना पाहूया."
        },
        "bn": {
            "greeting": "নমস্কার! আমি আপনার এআই স্কিম সাথি (Qwen চালিত)। সরকারি ঋণ প্রকল্প এবং ভর্তুকি খুঁজে পেতে আমি সাহায্য করব। আপনার কি ধরণের ব্যবসার জন্য ঋণ প্রয়োজন?",
            "ask_income": "সঠিক ভর্তুকি ও যোগ্যতা যাচাই করতে আপনার বার্ষিক পারিবারিক আয় কত?",
            "ask_loan_amount": "আপনার প্রকল্পের জন্য কত টাকার ঋণ প্রয়োজন?",
            "found_schemes": "myScheme.gov.in থেকে আপনার প্রয়োজনীয়তার সাথে সংগতিপূর্ণ সরকারি প্রকল্পসমূহ:",
            "fallback": "আমি আপনার অনুরোধ বুঝতে পেরেছি। আপনার জন্য সেরা প্রকল্পগুলো বিশ্লেষণ করছি।"
        },
        "gu": {
            "greeting": "નમસ્તે! હું તમારો એઆઈ સ્કીમ સાથી છું (Qwen આધારિત). સરકારી લોન યોજનાઓ અને સબસિડી શોધવામાં હું મદદ કરી શકું છું. તમે કયા વ્યવસાય માટે લોન શોધી રહ્યા છો?",
            "ask_income": "ચોક્કસ સબસિડી અને પાત્રતા જાણવા માટે તમારી વાર્ષિક કૌટુંબિક આવક કેટલી છે?",
            "ask_loan_amount": "તમારા પ્રોજેક્ટ માટે કેટલી લોનની જરૂર છે?",
            "found_schemes": "myScheme.gov.in આધારિત તમારી જરૂરિયાત મુજબની સરકારી યોજનાઓ:",
            "fallback": "મેં તમારી વાત સમજી લીધી છે. ચાલો તમારા માટે શ્રેષ્ઠ યોજનાઓ જોઈએ."
        },
        "pa": {
            "greeting": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਏਆਈ ਸਕੀਮ ਸਾਥੀ ਹਾਂ (Qwen ਸੰਚਾਲਿਤ)। ਮੈਂ ਸਰਕਾਰੀ ਕਰਜ਼ਾ ਯੋਜਨਾਵਾਂ ਅਤੇ ਸਬਸਿਡੀਆਂ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ। ਤੁਹਾਨੂੰ ਕਿਸ ਕਾਰੋਬਾਰ ਲਈ ਕਰਜ਼ਾ ਚਾਹੀਦਾ ਹੈ?",
            "ask_income": "ਸਹੀ ਸਬਸਿਡੀ ਅਤੇ ਯੋਗਤਾ ਜਾਣਨ ਲਈ ਤੁਹਾਡੀ ਸਾਲਾਨਾ ਪਰਿਵਾਰਕ ਆਮਦਨ ਕਿੰਨੀ ਹੈ?",
            "ask_loan_amount": "ਤੁਹਾਨੂੰ ਆਪਣੇ ਪ੍ਰੋਜੈਕਟ ਲਈ ਕਿੰਨੇ ਕਰਜ਼ੇ ਦੀ ਲੋੜ ਹੈ?",
            "found_schemes": "myScheme.gov.in ਤੋਂ ਤੁਹਾਡੀ ਲੋੜ ਅਨੁਸਾਰ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ:",
            "fallback": "ਮੈਂ ਤੁਹਾਡੀ ਬੇਨਤੀ ਸਮਝ ਲਈ ਹੈ। ਆਓ ਸਭ ਤੋਂ ਵਧੀਆ ਯੋਜਨਾਵਾਂ ਦੇਖੀਏ।"
        },
        "or": {
            "greeting": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ AI ସ୍କିମ ସାଥି (Qwen ଚାଳିତ)। ସରକାରୀ ଋଣ ଯୋଜନା ଏବଂ ରିହାତି ଖୋଜିବାରେ ମୁଁ ସାହାଯ୍ୟ କରିବି। ଆପଣ କେଉଁ ବ୍ୟବସାୟ ପାଇଁ ଋଣ ଚାହୁଁଛନ୍ତି?",
            "ask_income": "ସଠିକ ରିହାତି ଓ ଯୋଗ୍ୟତା ଜାଣିବା ପାଇଁ ଆପଣଙ୍କ ବାର୍ଷିକ ପାରିବାରିକ ଆୟ କେତେ?",
            "ask_loan_amount": "ଆପଣଙ୍କ ପ୍ରକଳ୍ପ ପାଇଁ କେତେ ଋଣ ଆବଶ୍ୟକ?",
            "found_schemes": "myScheme.gov.in ରୁ ଆପଣଙ୍କ ଆବଶ୍ୟକତା ଅନୁଯାୟୀ ସରକାରୀ ଯୋଜନା:",
            "fallback": "ମୁଁ ଆପଣଙ୍କ ଅନୁରୋଧ ବୁଝିପାରିଲି। ଆସନ୍ତୁ ଉପଯୁକ୍ତ ଯୋଜନା ଦେଖିବା।"
        },
        "as": {
            "greeting": "নমস্কাৰ! মই আপোনাৰ AI আঁচনি সাথি (Qwen চালিত)। চৰকাৰী ঋণ আঁচনি আৰু ৰাজসাহায্য বিচাৰি পোৱাত মই সহায় কৰিম। আপোনাক কি ব্যৱসায়ৰ বাবে ঋণ লাগে?",
            "ask_income": "সঠিক ৰাজসাহায্য আৰু যোগ্যতা নিৰ্ধাৰণ কৰিবলৈ আপোনাৰ বাৰ্ষিক পাৰিবাৰিক আয় কিমান?",
            "ask_loan_amount": "আপোনাৰ প্ৰকল্পৰ বাবে কিমান ঋণৰ প্ৰয়োজন?",
            "found_schemes": "myScheme.gov.in ৰ পৰা আপোনাৰ প্ৰয়োজনীয়তা অনুসৰি চৰকাৰী আঁচনিসমূহ:",
            "fallback": "মই আপোনাৰ অনুৰোধ বুজি পাইছো। আহক উপযুক্ত আঁচনিসমূহ চাওঁ।"
        }
    }

    @classmethod
    def get_ollama_model(cls) -> str:
        """Find an available Qwen model from Ollama, fallback to config default."""
        try:
            url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/tags"
            req = urllib.request.Request(url, headers={"User-Agent": "SchemeSathi/1.0"})
            with urllib.request.urlopen(req, timeout=1) as resp:
                data = json.loads(resp.read().decode())
                models = [m.get("name", "") for m in data.get("models", [])]
                for m in models:
                    if "qwen" in m.lower():
                        return m
        except Exception:
            pass
        return settings.OLLAMA_MODEL or "qwen3:4b"

    @classmethod
    def _get_scheme_field(cls, scheme: Any, field: str, default: Any = "") -> Any:
        """Safely extract field from Scheme ORM model, dict, or namespace."""
        if isinstance(scheme, dict):
            return scheme.get(field, default)
        return getattr(scheme, field, default)

    @classmethod
    def query_qwen_ollama(
        cls, 
        user_message: str, 
        language: str = "en", 
        schemes_db: List[Any] = []
    ) -> Optional[str]:
        """
        Query Qwen via Ollama with verified statutory scheme context for grounded responses.
        """
        model = cls.get_ollama_model()
        lang_name = cls.LANGUAGE_NAMES.get(language, "English")

        # Build concise knowledge base from database
        scheme_context_items = []
        for s in schemes_db[:15]:
            s_name = cls._get_scheme_field(s, "scheme_name") or cls._get_scheme_field(s, "name") or "Scheme"
            s_code = cls._get_scheme_field(s, "code") or cls._get_scheme_field(s, "scheme_code") or ""
            s_max = cls._get_scheme_field(s, "max_loan_amount", 0)
            s_sub = cls._get_scheme_field(s, "subsidy_percentage", 0)
            s_target = cls._get_scheme_field(s, "target_category", "")
            s_biz = cls._get_scheme_field(s, "business_type", "")
            s_rural = cls._get_scheme_field(s, "rural_subsidy_percentage", 0)

            scheme_context_items.append(
                f"- Scheme: {s_name} ({s_code})\n"
                f"  Max Loan: Rs {s_max:,} | Subsidy: {s_sub}%\n"
                f"  Target: {s_target} | Eligible: {s_biz} | Rural Subsidy: {s_rural}%"
            )
        scheme_context = "\n".join(scheme_context_items)

        system_prompt = f"""You are 'Scheme Sathi', an expert Indian Government Scheme Advisor for marginalized entrepreneurs and students.
You provide 100% accurate, gazetted financial advice based on official myScheme.gov.in guidelines.
CRITICAL INSTRUCTIONS:
1. Always respond in natural, polite, and fluent {lang_name}.
2. Never hallucinate scheme limits. Use the provided Verified Gazette Database.
3. Mention key parameters: Maximum loan sanction, subsidy percentage, required margin money, and documents.
4. Keep the response concise, structured, and easy to read for rural and small business founders.

VERIFIED GAZETTE KNOWLEDGE BASE:
{scheme_context}
"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.8,
                "num_predict": 400
            }
        }

        try:
            url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat"
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "SchemeSathi/1.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result.get("message", {}).get("content", "")
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                if content:
                    return content
        except Exception:
            pass
        return None

    @classmethod
    def generate_response(
        cls, 
        message: str, 
        language: str = "en", 
        schemes_db: List[Any] = []
    ) -> Dict[str, Any]:
        """
        Main response generation pipeline:
        1. Attempt Qwen from Ollama for conversational AI.
        2. Fall back to deterministic gazette rules matching if Ollama is offline.
        """
        lang = language.lower() if language else "en"
        if lang not in cls.LANGUAGE_NAMES:
            lang = "en"

        # 1. Try Ollama Qwen
        qwen_reply = cls.query_qwen_ollama(message, language=lang, schemes_db=schemes_db)
        if qwen_reply:
            matched_cards = cls._extract_matching_schemes(message, schemes_db)
            return {
                "reply": qwen_reply,
                "source": f"Qwen via Ollama ({cls.get_ollama_model()})",
                "language": lang,
                "matched_schemes": matched_cards
            }

        # 2. Deterministic Gazette Rule Matching Fallback
        return cls._deterministic_fallback(message, lang, schemes_db)

    @classmethod
    def _extract_matching_schemes(cls, message: str, schemes_db: List[Any]) -> List[Dict[str, Any]]:
        """Identify referenced schemes from user query to render interactive cards."""
        msg_lower = message.lower()
        matched = []
        for s in schemes_db:
            s_name = cls._get_scheme_field(s, "scheme_name") or cls._get_scheme_field(s, "name") or ""
            s_code = cls._get_scheme_field(s, "code") or cls._get_scheme_field(s, "scheme_code") or ""
            s_id = cls._get_scheme_field(s, "id") or 1
            s_max = cls._get_scheme_field(s, "max_loan_amount", 0)
            s_sub = cls._get_scheme_field(s, "subsidy_percentage", 0)

            if (s_code and s_code.lower() in msg_lower) or any(word in msg_lower for word in s_name.lower().split() if len(word) > 3):
                matched.append({
                    "id": s_id,
                    "name": s_name,
                    "code": s_code,
                    "max_loan": s_max,
                    "subsidy": s_sub
                })
                if len(matched) >= 3:
                    break
        return matched

    @classmethod
    def _deterministic_fallback(
        cls, 
        message: str, 
        lang: str, 
        schemes_db: List[Any]
    ) -> Dict[str, Any]:
        """Rule-based multilingual fallback when Ollama Qwen is offline."""
        msg_lower = message.lower()
        responses = cls.INTENT_RESPONSES.get(lang, cls.INTENT_RESPONSES["en"])

        # Check for greeting
        if any(w in msg_lower for w in ["hi", "hello", "namaste", "vanakkam", "namaskara", "nomoshkar", "kem cho", "sat sri akal", "nomoskar"]):
            return {
                "reply": responses["greeting"],
                "source": "Rule Gazette Fallback",
                "language": lang,
                "matched_schemes": []
            }

        # Check for Street Vendor / SVANidhi
        if any(w in msg_lower for w in ["vendor", "thela", "street", "10000", "50000", "patari", "feriwala"]):
            svanidhi = next((s for s in schemes_db if "SVANIDHI" in (cls._get_scheme_field(s, "code") or cls._get_scheme_field(s, "scheme_code") or "")), None)
            reply = f"{responses['found_schemes']}\n\n"
            if svanidhi:
                name = cls._get_scheme_field(svanidhi, "name") or cls._get_scheme_field(svanidhi, "scheme_name")
                code = cls._get_scheme_field(svanidhi, "code") or cls._get_scheme_field(svanidhi, "scheme_code")
                reply += f"• **{name} ({code})**\n  - Loan Limit: ₹10,000 - ₹50,000\n  - Collateral Free: 100%\n  - Interest Subsidy: 7% on timely repayment."
            return {
                "reply": reply,
                "source": "Rule Gazette Fallback",
                "language": lang,
                "matched_schemes": cls._extract_matching_schemes("svanidhi", schemes_db)
            }

        # Check for Women / Stand-Up India / Mudra
        if any(w in msg_lower for w in ["woman", "women", "female", "mahila", "sc", "st"]):
            reply = f"{responses['found_schemes']}\n\n"
            reply += "• **Stand-Up India Scheme (STANDUP-IND)**: ₹10 Lakh - ₹1 Crore for SC/ST & Women with Bank Guarantee.\n"
            reply += "• **Pradhan Mantri MUDRA Yojana (PMMY)**: Up to ₹10 Lakh Collateral Free across Shishu, Kishore, and Tarun categories.\n"
            return {
                "reply": reply,
                "source": "Rule Gazette Fallback",
                "language": lang,
                "matched_schemes": cls._extract_matching_schemes("standup mudra", schemes_db)
            }

        # General high subsidy / PMEGP
        reply = f"{responses['found_schemes']}\n\n"
        reply += "• **Prime Minister's Employment Generation Programme (PMEGP)**\n  - Up to ₹50 Lakh for Manufacturing\n  - Up to 35% Capital Subsidy for SC/ST/Women in Rural Areas."

        return {
            "reply": reply,
            "source": "Rule Gazette Fallback",
            "language": lang,
            "matched_schemes": cls._extract_matching_schemes("pmegp", schemes_db)
        }
'''

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\backend\app\services\chat.py', 'w', encoding='utf-8') as f:
    f.write(chat_code)

print("chat.py updated safely!")
