# -*- coding: utf-8 -*-
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
    def query_cloud_ai_api(
        cls,
        user_message: str,
        language: str = "en",
        schemes_db: List[Any] = []
    ) -> Optional[str]:
        """
        Query Cloud AI / Chatbase / AI Gateway API using configured API_KEY.
        """
        api_key = settings.API_KEY or settings.CHATBASE_API_KEY or settings.CHATBOT_API_KEY
        if not api_key or "xx" in api_key: # check if token is valid non-masked
            return None

        lang_name = cls.LANGUAGE_NAMES.get(language, "English")
        try:
            # Attempt Chatbase API v1 Chat endpoint
            url = "https://www.chatbase.co/api/v1/chat"
            payload = {
                "messages": [
                    {"role": "user", "content": f"Answer in {lang_name} regarding Indian Government business schemes: {user_message}"}
                ],
                "stream": False
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "SchemeSathi/1.0"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result.get("text") or result.get("message") or result.get("response")
                if text:
                    return text
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
        1. Attempt Cloud AI API with user API Key.
        2. Attempt Qwen from Ollama.
        3. Fall back to deterministic gazette rules matching.
        """
        lang = language.lower() if language else "en"
        if lang not in cls.LANGUAGE_NAMES:
            lang = "en"

        # 1. Try Cloud AI API with user API key
        cloud_reply = cls.query_cloud_ai_api(message, language=lang, schemes_db=schemes_db)
        if cloud_reply:
            matched_cards = cls._extract_matching_schemes(message, schemes_db)
            return {
                "reply": cloud_reply,
                "response": cloud_reply,
                "source": "AI Cloud Gateway (API Key)",
                "model_used": "AI Cloud Gateway (API Key Authenticated)",
                "language": lang,
                "matched_schemes": matched_cards,
                "recommendations": matched_cards,
                "scheme_recommendations": matched_cards,
                "extracted_intent": {"language": lang},
                "suggested_options": []
            }

        # 2. Try Ollama Qwen
        qwen_reply = cls.query_qwen_ollama(message, language=lang, schemes_db=schemes_db)
        if qwen_reply:
            matched_cards = cls._extract_matching_schemes(message, schemes_db)
            return {
                "reply": qwen_reply,
                "response": qwen_reply,
                "source": f"Qwen via Ollama ({cls.get_ollama_model()})",
                "model_used": f"Qwen via Ollama ({cls.get_ollama_model()})",
                "language": lang,
                "matched_schemes": matched_cards,
                "recommendations": matched_cards,
                "scheme_recommendations": matched_cards,
                "extracted_intent": {"language": lang},
                "suggested_options": []
            }

        # 2. Deterministic Gazette Rule Matching Fallback
        res = cls._deterministic_fallback(message, lang, schemes_db)
        res["response"] = res["reply"]
        res["model_used"] = res.get("source", "Gazette Knowledge Base")
        res["recommendations"] = res.get("matched_schemes", [])
        res["scheme_recommendations"] = res.get("matched_schemes", [])
        res["extracted_intent"] = {"language": lang}
        res["suggested_options"] = []
        return res

    @classmethod
    def process_message(
        cls, 
        user_message: str = "", 
        message: str = "", 
        language: str = "en", 
        schemes_db: List[Any] = []
    ) -> Dict[str, Any]:
        """Alias for generate_response accepting user_message or message parameter."""
        query = user_message or message
        return cls.generate_response(message=query, language=language, schemes_db=schemes_db)

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

    SCHEME_HIGHLIGHTS = {
        "svanidhi": {
            "en": "• **PM SVANidhi Scheme (SVANIDHI)**\n  - Loan Limit: ₹10,000 - ₹50,000\n  - Collateral Free: 100%\n  - Interest Subsidy: 7% on timely digital repayment.\n  - Eligibility: Urban & Peri-urban Street Vendors with Vending Certificate.",
            "hi": "• **पीएम स्वनिधि योजना (PM-SVANIDHI)**\n  - ऋण सीमा: ₹10,000 से ₹50,000\n  - जमानत मुक्त: 100% बिना किसी गारंटी\n  - ब्याज अनुदान: समय पर डिजिटल भुगतान पर 7% की छूट\n  - पात्रता: स्ट्रीट वेंडर्स व रेहड़ी-पटरी व्यवसायी।",
            "ta": "• **பிஎம் ஸ்வநிதி திட்டம் (PM-SVANIDHI)**\n  - கடன் வரம்பு: ₹10,000 முதல் ₹50,000 வரை\n  - பிணையற்ற கடன்: 100% உத்தரவாதம் தேவையில்லை\n  - வட்டி மானியம்: சரியான முறையில் திருப்பிச் செலுத்தினால் 7% வட்டி சலுகை\n  - தகுதி: தெருவோர வியாபாரிகள் மற்றும் சிறு வணிகர்கள்.",
            "te": "• **పీఎం స్వనిధి పథకం (PM-SVANIDHI)**\n  - రుణ పరిమితి: ₹10,000 నుండి ₹50,000 వరకు\n  - హామీ లేని రుణం: 100% ఎలాంటి పూచీకత్తు అవసరం లేదు\n  - వడ్డీ రాయితీ: సకాలంలో డిజిటల్ చెల్లింపులపై 7% వడ్డీ రాయితీ\n  - అర్హత: వీధి వ్యాపారులు మరియు తోపుడు బండ్ల వ్యాపారులు.",
            "kn": "• **ಪಿಎಂ ಸ್ವನಿಧಿ ಯೋಜನೆ (PM-SVANIDHI)**\n  - ಸಾಲದ ಮಿತಿ: ₹10,000 ರಿಂದ ₹50,000 ವರೆಗೆ\n  - ಖಾತರಿ ರಹಿತ ಸಾಲ: 100% ಯಾವುದೇ ಭದ್ರತೆ ಅಗತ್ಯವಿಲ್ಲ\n  - ಬಡ್ಡಿ ರಿಯಾಯಿತಿ: ಸಕಾಲಿಕ ಡಿಜಿಟಲ್ ಮರುಪಾವತಿಗೆ 7% ಬಡ್ಡಿ ಸಹಾಯಧನ\n  - ಅರ್ಹತೆ: ಬೀದಿ ಬದಿ ವ್ಯಾಪಾರಿಗಳು ಮತ್ತು ಸಣ್ಣ ವ್ಯಾಪಾರಿಗಳು.",
            "ml": "• **പിഎം സ്വനിധി പദ്ധതി (PM-SVANIDHI)**\n  - വായ്പാ പരിധി: ₹10,000 മുതൽ ₹50,000 വരെ\n  - ഈടില്ലാത്ത വായ്പ: 100% സുരക്ഷ ആവശ്യമില്ല\n  - പലിശ ഇളവ്: കൃത്യസമയത്ത് തിരിച്ചടച്ചാൽ 7% പലിശ സബ്‌സിഡി\n  - യോഗ്യത: തെരുവ് കച്ചവടക്കാരും ചെറുകിട സംരംഭകരും.",
            "mr": "• **पीएम स्वनिधी योजना (PM-SVANIDHI)**\n  - कर्ज मर्यादा: ₹10,000 ते ₹50,000\n  - तारणमुक्त कर्ज: 100% कोणतीही हमी आवश्यक नाही\n  - व्याज सवलत: वेळेवर डिजिटल परतफेडीवर 7% व्याज अनुदान\n  - पात्रता: पथविक्रेते व फेरीवाले व्यावसायिक.",
            "bn": "• **পিএম স্বনিধি প্রকল্প (PM-SVANIDHI)**\n  - ঋণের সীমা: ₹১০,০০০ থেকে ₹৫০,০০০ পর্যন্ত\n  - জামিনমুক্ত ঋণ: ১০০% কোনো গ্যারান্টি লাগবে না\n  - সুদের ভর্তুকি: সময়মতো ডিজিটাল পরিশোধে ৭% সুদের ছাড়\n  - যোগ্যতা: পথ বিক্রেতা ও হকার ভাইবোনেরা।",
            "gu": "• **પીએમ સ્વનિધિ યોજના (PM-SVANIDHI)**\n  - લોન મર્યાદા: ₹10,000 થી ₹50,000\n  - તારણ મુક્ત લોન: 100% કોઈ ગેરંટીની જરૂર નથી\n  - વ્યાજ સબસિડી: સમયસર ડિજિટલ ચૂકવણી પર 7% વ્યાજ રાહત\n  - પાત્રતા: શેરી ફેરિયા અને લારી-ગલ્લા ધારકો.",
            "pa": "• **ਪੀਐਮ ਸਵਨਿਧੀ ਯੋਜਨਾ (PM-SVANIDHI)**\n  - ਕਰਜ਼ਾ ਸੀਮਾ: ₹10,000 ਤੋਂ ₹50,000\n  - ਬਿਨਾਂ ਗਰੰਟੀ ਕਰਜ਼ਾ: 100% ਕੋਈ ਜ਼ਮਾਨਤ ਨਹੀਂ\n  - ਵਿਆਜ ਛੋਟ: ਸਮੇਂ ਸਿਰ ਡਿਜੀਟਲ ਭੁਗਤਾਨ 'ਤੇ 7% ਸਬਸਿਡੀ\n  - ਯੋਗਤਾ: ਰੇਹੜੀ-ਫੜ੍ਹੀ ਵਾਲੇ ਅਤੇ ਛੋਟੇ ਦੁਕਾਨਦਾਰ।",
            "or": "• **ପିଏମ ସ୍ୱନିଧି ଯୋଜନା (PM-SVANIDHI)**\n  - ଋଣ ସୀମା: ₹୧୦,୦୦୦ ରୁ ₹୫୦,୦୦୦\n  - ଜାମିନ ମୁକ୍ତ ଋଣ: ୧୦୦% କୌଣସି ଗ୍ୟାରେଣ୍ଟି ଆବଶ୍ୟକ ନାହିଁ\n  - ସୁଧ ରିହାତି: ସମୟାନୁସାରେ ଡିଜିଟାଲ ପରିଶୋଧରେ ୭% ସୁଧ ରିହାତି\n  - ଯୋଗ୍ୟତା: ରାସ୍ତାକଡ଼ ବିକ୍ରେତା ଓ ଉଠାଦୋକାନୀ।",
            "as": "• **পিএম স্বনিধি আঁচনি (PM-SVANIDHI)**\n  - ঋণৰ সীমা: ₹১০,০০০ ৰ পৰা ₹৫০,০০০ লৈ\n  - বন্ধকমুক্ত ঋণ: ১০০% কোনো জামিনৰ প্ৰয়োজন নাই\n  - সুদ ৰেহাই: সময়মতে ডিজিটেল পৰিশোধত ৭% সুদ ৰাজসাহায্য\n  - যোগ্যতা: পথ বিক্ৰেতা আৰু ক্ষুদ্র ব্যৱসায়ী।"
        },
        "standup": {
            "en": "• **Stand-Up India Scheme (STANDUP-IND)**\n  - Loan Limit: ₹10 Lakh to ₹1 Crore\n  - Margin Money: Up to 15% (Convergence with state schemes)\n  - Target Beneficiaries: SC / ST and Women Entrepreneurs for Greenfield Enterprises.\n• **Pradhan Mantri MUDRA Yojana (PMMY)**\n  - Shishu (up to ₹50k), Kishore (₹50k - ₹5L), Tarun (₹5L - ₹10L)\n  - Collateral Free with CGTMSE Coverage.",
            "hi": "• **स्टैंड-अप इंडिया योजना (STANDUP-IND)**\n  - ऋण सीमा: ₹10 लाख से ₹1 करोड़\n  - स्वयं का अंशदान (मार्जिन): केवल 15%\n  - लक्षित लाभार्थी: अनुसूचित जाति (SC), अनुसूचित जनजाति (ST) एवं महिला उद्यमी।\n• **प्रधानमंत्री मुद्रा योजना (PMMY)**\n  - शिशु (₹50,000 तक), किशोर (₹50,000 - ₹5 लाख), तरुण (₹5 लाख - ₹10 लाख)\n  - 100% गारंटी मुक्त (CGTMSE सुरक्षित)।",
            "ta": "• **ஸ்டாண்ட்-அப் இந்தியா திட்டம் (STANDUP-IND)**\n  - கடன் வரம்பு: ₹10 லட்சம் முதல் ₹1 கோடி வரை\n  - சொந்த பங்களிப்பு: 15% மட்டுமே\n  - பயனாளி: SC / ST மற்றும் பெண் தொழில்முனைவோர்.\n• **பிரதம மந்திரி முத்ரா திட்டம் (PMMY)**\n  - சிசு (₹50,000 வரை), கிஷோர் (₹50,000 - ₹5 லட்சம்), தருண் (₹5 லட்சம் - ₹10 லட்சம்)\n  - பிணையற்ற கடன் வசதி.",
            "te": "• **స్టాండ్-అప్ ఇండియా పథకం (STANDUP-IND)**\n  - రుణ పరిమితి: ₹10 లక్షల నుండి ₹1 కోటి వరకు\n  - మార్జిన్ మనీ: కేవలం 15%\n  - లబ్ధిదారులు: SC / ST మరియు మహిళా పారిశ్రామికవేత్తలు.\n• **ప్రధాన మంత్రి ముద్రా యోజన (PMMY)**\n  - శిశు (₹50,000 వరకు), కిషోర్ (₹50,000 - ₹5 లక్షలు), తరుణ్ (₹5 లక్షలు - ₹10 లక్షలు)\n  - ఎలాంటి పూచీకత్తు అవసరం లేదు.",
            "kn": "• **ಸ್ಟ್ಯಾಂಡ್‌-ಅಪ್ ಇಂಡಿಯಾ ಯೋಜನೆ (STANDUP-IND)**\n  - ಸಾಲದ ಮಿತಿ: ₹10 ಲಕ್ಷದಿಂದ ₹1 ಕೋಟಿ ವರೆಗೆ\n  - ಮಾರ್ಜಿನ್ ಮನಿ: ಕೇವಲ 15%\n  - ಫಲಾನುಭವಿಗಳು: ಎಸ್‌ಸಿ / ಎಸ್‌ಟಿ ಮತ್ತು ಮಹಿಳಾ ಉದ್ಯಮಿಗಳು.\n• **ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ (PMMY)**\n  - ಶಿಶು (₹50,000 ವರೆಗೆ), ಕಿಶೋರ್ (₹50,000 - ₹5 ಲಕ್ಷ), ತರುಣ್ (₹5 ಲಕ್ಷ - ₹10 ಲಕ್ಷ)\n  - ಖಾತರಿ ರಹಿತ ಸುಲಭ ಸಾಲ.",
            "ml": "• **സ്റ്റാൻഡ്-അപ്പ് ഇന്ത്യ പദ്ധതി (STANDUP-IND)**\n  - വായ്പാ പരിധി: ₹10 ലക്ഷം മുതൽ ₹1 കോടി വരെ\n  - മാർജിൻ മണി: 15% മാത്രം\n  - ഗുണഭോക്താക്കൾ: SC / ST വിഭാഗങ്ങളും വനിതാ സംരംഭകരും.\n• **പ്രധാനമന്ത്രി മുദ്ര യോജന (PMMY)**\n  - ശിശു (₹50,000 വരെ), കിഷോർ (₹50,000 - ₹5 ലക്ഷം), തരുൺ (₹5 ലക്ഷം - ₹10 ലക്ഷം)\n  - ഈടില്ലാത്ത സാമ്പത്തിക സഹായം.",
            "mr": "• **स्टँड-अप इंडिया योजना (STANDUP-IND)**\n  - कर्ज मर्यादा: ₹10 लाख ते ₹1 कोटी\n  - स्वतःचे योगदान: फक्त 15%\n  - लाभार्थी: अनुसूचित जाती (SC), अनुसूचित जमाती (ST) व महिला उद्योजक.\n• **प्रधानमंत्री मुद्रा योजना (PMMY)**\n  - शिशु (₹50,000 पर्यंत), किशोर (₹50,000 - ₹5 लाख), तरुण (₹5 लाख - ₹10 लाख)\n  - संपूर्ण तारणमुक्त कर्ज.",
            "bn": "• **স্ট্যান্ড-আপ ইন্ডিয়া স্কিম (STANDUP-IND)**\n  - ঋণের সীমা: ₹১০ লাখ থেকে ₹১ কোটি\n  - মার্জিন মানি: মাত্র ১৫%\n  - সুবিধাভোগী: তপশিলি জাতি (SC), উপজাতি (ST) এবং মহিলা উদ্যোক্তা।\n• **প্রধানমন্ত্রী মুদ্রা যোজনা (PMMY)**\n  - শিশু (₹৫০,০০০ পর্যন্ত), কিশোর (₹৫০,০০০ - ₹৫ লাখ), তরুণ (₹৫ লাখ - ₹১০ লাখ)\n  - সম্পূর্ণ জামিনমুক্ত ঋণ সুবিধা।",
            "gu": "• **સ્ટેન્ડ-અપ ઇન્ડિયા યોજના (STANDUP-IND)**\n  - લોન મર્યાદા: ₹10 લાખ થી ₹1 કરોડ\n  - માર્જિન મની: માત્ર 15%\n  - લાભાર્થીઓ: SC / ST અને મહિલા સાહસિકો.\n• **પ્રધાનમંત્રી મુદ્રા યોજના (PMMY)**\n  - શિશુ (₹50,000 સુધી), કિશોર (₹50,000 - ₹5 લાખ), તરુણ (₹5 લાખ - ₹10 લાખ)\n  - કોઈ ગેરંટી વગર લોન.",
            "pa": "• **ਸਟੈਂਡ-ਅੱਪ ਇੰਡੀਆ ਸਕੀਮ (STANDUP-IND)**\n  - ਕਰਜ਼ਾ ਸੀਮਾ: ₹10 ਲੱਖ ਤੋਂ ₹1 ਕਰੋੜ\n  - ਮਾਰਜਨ ਮਨੀ: ਸਿਰਫ਼ 15%\n  - ਲਾਭਪਾਤਰੀ: ਅਨੁਸੂਚਿਤ ਜਾਤੀ (SC), ਅਨੁਸੂਚਿਤ ਜਨਜਾਤੀ (ST) ਅਤੇ ਮਹਿਲਾ ਉੱਦਮੀ।\n• **ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਮੁਦਰਾ ਯੋਜਨਾ (PMMY)**\n  - ਸ਼ਿਸ਼ੂ (₹50,000 ਤੱਕ), ਕਿਸ਼ੋਰ (₹50,000 - ₹5 ਲੱਖ), ਤਰੁਣ (₹5 ਲੱਖ - ₹10 ਲੱਖ)\n  - ਬਿਨਾਂ ਕਿਸੇ ਗਾਰੰਟੀ ਕਰਜ਼ਾ।",
            "or": "• **ଷ୍ଟାଣ୍ଡ-ଅପ୍ ଇଣ୍ଡିଆ ଯୋଜନା (STANDUP-IND)**\n  - ଋଣ ସୀମା: ₹୧୦ ଲକ୍ଷ ରୁ ₹୧ କୋଟି\n  - ମାର୍ଜିନ ଅର୍ଥ: ମାତ୍ର ୧୫%\n  - ହିତାଧିକାରୀ: SC / ST ଏବଂ ମହିଳା ଉଦ୍ୟୋଗୀ।\n• **ପ୍ରଧାନମନ୍ତ୍ରୀ ମୁଦ୍ରା ଯୋଜନା (PMMY)**\n  - ଶିଶୁ (₹୫୦,୦୦୦ ପର୍ଯ୍ୟନ୍ତ), କିଶୋର (₹୫୦,୦୦୦ - ₹୫ ଲକ୍ଷ), ତରୁଣ (₹୫ ଲକ୍ଷ - ₹୧୦ ଲକ୍ଷ)\n  - ସମ୍ପୂର୍ଣ୍ଣ ଜାମିନ ମୁକ୍ତ ଋଣ।",
            "as": "• **ষ্টেণ্ড-আপ ইণ্ডিয়া আঁচনি (STANDUP-IND)**\n  - ঋণৰ সীমা: ₹১০ লাখৰ পৰা ₹১ কোটি\n  - মার্জিন ধন: মাত্ৰ ১৫%\n  - হিতাধিকাৰী: অনুসূচীত জাতি (SC), অনুসূচীত জনজাতি (ST) আৰু মহিলা উদ্যোগী।\n• **প্ৰধানমন্ত্ৰী মুদ্রা যোজনা (PMMY)**\n  - শিশু (₹৫০,০০০ লৈকে), কিশোৰ (₹৫০,০০০ - ₹৫ লাখ), তৰুণ (₹৫ লাখ - ₹১০ লাখ)\n  - কোনো বন্ধক অবিহনে ঋণ।"
        },
        "pmegp": {
            "en": "• **Prime Minister's Employment Generation Programme (PMEGP)**\n  - Maximum Project Cost: Up to ₹50 Lakh (Manufacturing) / ₹20 Lakh (Service)\n  - Capital Subsidy: Up to 35% in Rural Areas (25% in Urban Areas for Special Category: SC/ST/Women/OBC/Minorities)\n  - Own Contribution: Only 5% for Special Category beneficiaries.\n• **PM Vishwakarma Scheme**\n  - Up to ₹3 Lakh Collateral-Free Enterprise Loan @ 5% Concessional Interest Rate + ₹15,000 Modern Tool-kit Incentive.",
            "hi": "• **प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)**\n  - अधिकतम परियोजना लागत: ₹50 लाख (विनिर्माण) / ₹20 लाख (सेवा)\n  - पूंजीगत अनुदान (सब्सिडी): ग्रामीण क्षेत्रों में 35% तक (शहरी क्षेत्रों में विशेष श्रेणी के लिए 25%)\n  - स्वयं का अंशदान: विशेष वर्ग (SC/ST/महिला/दिव्यांग) के लिए केवल 5%।\n• **पीएम विश्वकर्मा योजना (PM-VISHWAKARMA)**\n  - 18 पारंपरिक शिल्पों के लिए ₹3 लाख तक का ऋण मात्र 5% रियायती ब्याज पर + ₹15,000 टूलकिट अनुदान।",
            "ta": "• **பிரதமரின் வேலைவாய்ப்பு உருவாக்கும் திட்டம் (PMEGP)**\n  - அதிகபட்ச திட்ட மதிப்பு: ₹50 லட்சம் (உற்பத்தி) / ₹20 லட்சம் (சேவை)\n  - மூலதன மானியம்: கிராமப்புறங்களில் 35% வரை (நகர்ப்புறங்களில் 25% மானியம்)\n  - சொந்த முதலீடு: சிறப்பு பிரிவினருக்கு (SC/ST/பெண்கள்) வெறும் 5% மட்டுமே.\n• **பிஎம் விஸ்வகர்மா திட்டம் (PM-VISHWAKARMA)**\n  - பாரம்பரிய கைவினைஞர்களுக்கு 5% சலுகை வட்டியில் ₹3 லட்சம் வரை பிணையற்ற கடன் + ₹15,000 உபகரண மானியம்.",
            "te": "• **ప్రధాన మంత్రి ఉపాధి కల్పన కార్యక్రమం (PMEGP)**\n  - గరిష్ట ప్రాజెక్ట్ ఖర్చు: ₹50 లక్షలు (తయారీ) / ₹20 లక్షలు (సేవలు)\n  - మూలధన సబ్సిడీ: గ్రామీణ ప్రాంతాల్లో 35% వరకు (పట్టణాల్లో ప్రత్యేక వర్గాలకు 25%)\n  - సొంత వాటా: ప్రత్యేక వర్గాల (SC/ST/మహిళలు) వారికి కేవలం 5% మాత్రమే.\n• **పీఎం విశ్వకర్మ పథకం (PM-VISHWAKARMA)**\n  - 18 రకాల సాంప్రదాయ చేతివృత్తుల వారికి 5% రాయితీ వడ్డీతో ₹3 లక్షల వరకు రుణం + ₹15,000 టూల్‌కిట్ గ్రాంట్.",
            "kn": "• **ಪ್ರಧಾನ ಮಂತ್ರಿ ಉದ್ಯೋಗ ಸೃಷ್ಟಿ ಕಾರ್ಯಕ್ರಮ (PMEGP)**\n  - ಗರಿಷ್ಠ ಯೋಜನಾ ವೆಚ್ಚ: ₹50 ಲಕ್ಷ (ಉತ್ಪಾದನೆ) / ₹20 ಲಕ್ಷ (ಸೇವೆ)\n  - ಬಂಡವಾಳ ಸಬ್ಸಿಡಿ: ಗ್ರಾಮೀಣ ಪ್ರದೇಶದಲ್ಲಿ 35% ವರೆಗೆ (ನಗರ ಪ್ರದೇಶದಲ್ಲಿ 25%)\n  - ಸ್ವಂತ ಹೂಡಿಕೆ: ವಿಶೇಷ ವರ್ಗಗಳಿಗೆ (SC/ST/ಮಹಿಳೆಯರು) ಕೇವಲ 5% ಮಾತ್ರ.\n• **ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಯೋಜನೆ (PM-VISHWAKARMA)**\n  - ಸಾಂಪ್ರದಾಯಿಕ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ 5% ಬಡ್ಡಿದರದಲ್ಲಿ ₹3 ಲಕ್ಷದವರೆಗೆ ಸಾಲ + ₹15,000 ಟೂಲ್‌ಕಿಟ್ ಪ್ರೋತ್ಸಾಹಧನ.",
            "ml": "• **പ്രധാനമന്ത്രി തൊഴിൽ ദായക പദ്ധതി (PMEGP)**\n  - പരമാവധി പ്രോജക്ട് തുക: ₹50 ലക്ഷം (നിർമ്മാണം) / ₹20 ലക്ഷം (സേവനം)\n  - മൂലധന സബ്‌സിഡി: ഗ്രാമപ്രദേശങ്ങളിൽ 35% വരെ (നഗരങ്ങളിൽ പ്രത്യേക വിഭാഗങ്ങൾക്ക് 25%)\n  - സ്വന്തം വിഹിതം: പ്രത്യേക വിഭാഗങ്ങൾക്ക് (SC/ST/വനിതകൾ) വെറും 5% മാത്രം.\n• **പിഎം വിശ്വകർമ പദ്ധതി (PM-VISHWAKARMA)**\n  - പരമ്പരാഗത കരകൗശല വിദഗ്ദ്ധർക്ക് 5% പലിശ നിരക്കിൽ ₹3 ലക്ഷം വരെ വായ്പ + ₹15,000 ടൂൾകിറ്റ് ഗ്രാന്റ്.",
            "mr": "• **पंतप्रधान रोजगार निर्मिती कार्यक्रम (PMEGP)**\n  - कमाल प्रकल्प मर्यादा: ₹50 लाख (उत्पादन) / ₹20 लाख (सेवा)\n  - भांडवली अनुदान (सब्सिडी): ग्रामीण भागात 35% पर्यंत (शहरी भागात विशेष प्रवर्गासाठी 25%)\n  - स्वतःचे योगदान: विशेष प्रवर्गासाठी (SC/ST/महिला/अल्पसंख्याक) फक्त 5%.\n• **पीएम विश्वकर्मा योजना (PM-VISHWAKARMA)**\n  - 18 पारंपारिक कारागिरांसाठी 5% सवलतीच्या व्याजाने ₹3 लाखांपर्यंत तारणमुक्त कर्ज + ₹15,000 टूलकिट अनुदान.",
            "bn": "• **প্রধানমন্ত্রী কর্মসংস্থান সৃষ্টি কর্মসূচি (PMEGP)**\n  - সর্বোচ্চ প্রকল্প ব্যয়: ₹৫০ লাখ (উৎপাদন) / ₹২০ লাখ (সেবা)\n  - মূলধন ভর্তুকি: গ্রামীণ এলাকায় ৩৫% পর্যন্ত (শহরাঞ্চলে বিশেষ বিভাগের জন্য ২৫%)\n  - নিজস্ব অবদান: বিশেষ শ্রেণীর (SC/ST/মহিলা) জন্য মাত্র ৫%।\n• **পিএম বিশ্বকর্মা প্রকল্প (PM-VISHWAKARMA)**\n  - ঐতিহ্যবাহী কারিগরদের জন্য ৫% সুদে ₹৩ লাখ পর্যন্ত জামিনমুক্ত ঋণ + ₹১৫,০০০ আধুনিক সরঞ্জাম অনুদান।",
            "gu": "• **પ્રધાનમંત્રી રોજગાર સર્જન કાર્યક્રમ (PMEGP)**\n  - મહત્તમ પ્રોજેક્ટ ખર્ચ: ₹50 લાખ (ઉત્પાદન) / ₹20 લાખ (સેવા)\n  - મૂડી સબસિડી: ગ્રામીણ વિસ્તારમાં 35% સુધી (શહેરી વિસ્તારમાં વિશેષ વર્ગ માટે 25%)\n  - પોતાનું યોગદાન: વિશેષ વર્ગ (SC/ST/મહિલા) માટે માત્ર 5%.\n• **પીએમ વિશ્વકર્મા યોજના (PM-VISHWAKARMA)**\n  - પરંપરાગત કારીગરો માટે 5% ના રાહત વ્યાજે ₹3 લાખ સુધીની લોન + ₹15,000 ટૂલકીટ સહાય.",
            "pa": "• **ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਰੋਜ਼ਗਾਰ ਉਤਪਾਦਨ ਪ੍ਰੋਗਰਾਮ (PMEGP)**\n  - ਵੱਧ ਤੋਂ ਵੱਧ ਪ੍ਰੋਜੈਕਟ ਲਾਗਤ: ₹50 ਲੱਖ (ਉਤਪਾਦਨ) / ₹20 ਲੱਖ (ਸੇਵਾ)\n  - ਪੂੰਜੀ ਸਬਸਿਡੀ: ਪੇਂਡੂ ਖੇਤਰਾਂ ਵਿੱਚ 35% ਤੱਕ (ਸ਼ਹਿਰੀ ਖੇਤਰਾਂ ਵਿੱਚ ਵਿਸ਼ੇਸ਼ ਸ਼੍ਰੇਣੀ ਲਈ 25%)\n  - ਆਪਣਾ ਹਿੱਸਾ: ਵਿਸ਼ੇਸ਼ ਸ਼੍ਰੇਣੀ (SC/ST/ਮਹਿਲਾ) ਲਈ ਸਿਰਫ਼ 5%।\n• **ਪੀਐਮ ਵਿਸ਼ਵਕਰਮਾ ਯੋਜਨਾ (PM-VISHWAKARMA)**\n  - ਰਵਾਇਤੀ ਦਸਤਕਾਰਾਂ ਲਈ 5% ਰਿਆਇਤੀ ਵਿਆਜ 'ਤੇ ₹3 ਲੱਖ ਤੱਕ ਕਰਜ਼ਾ + ₹15,000 ਟੂਲਕਿੱਟ ਸਹਾਇਤਾ।",
            "or": "• **ପ୍ରଧାନମନ୍ତ୍ରୀ ନିଯୁକ୍ତି ସୃଷ୍ଟି କାର୍ଯ୍ୟକ୍ରମ (PMEGP)**\n  - ସର୍ବାଧିକ ପ୍ରକଳ୍ପ ମୂଲ୍ୟ: ₹୫୦ ଲକ୍ଷ (ଉତ୍ପାଦନ) / ₹୨୦ ଲକ୍ଷ (ସେବା)\n  - ପୁଞ୍ଜି ରିହାତି (ସବସିଡି): ଗ୍ରାମାଞ୍ଚଳରେ ୩୫% ପର୍ଯ୍ୟନ୍ତ (ସହରାଞ୍ଚଳରେ ବିଶେଷ ବର୍ଗ ପାଇଁ ୨୫%)\n  - ନିଜ ଅଂଶଧନ: ବିଶେଷ ବର୍ଗ (SC/ST/ମହିଳା) ପାଇଁ ମାତ୍ର ୫%।\n• **ପିଏମ ବିଶ୍ୱକର୍ମା ଯୋଜନା (PM-VISHWAKARMA)**\n  - ପାରମ୍ପରିକ କାରିଗରଙ୍କ ପାଇଁ ୫% ସୁଧରେ ₹୩ ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ଋଣ + ₹୧୫,୦୦୦ ଟୁଲକିଟ୍ ଅନୁଦାନ।",
            "as": "• **প্ৰধানমন্ত্ৰী নিয়োগ সৃষ্টি কাৰ্যসূচী (PMEGP)**\n  - সৰ্বোচ্চ প্ৰকল্প ব্যয়: ₹৫০ লাখ (উৎপাদন) / ₹২০ লাখ (সেৱা)\n  - মূলধন ৰাজসাহায্য: গ্ৰাম্য অঞ্চলত ৩৫% লৈকে (নগৰাঞ্চলত বিশেষ শ্ৰেণীৰ বাবে ২৫%)\n  - নিজৰ অংশদান: বিশেষ শ্ৰেণীৰ (SC/ST/মহিলা) বাবে মাত্ৰ ৫%।\n• **পিএম বিশ্বকর্মা আঁচনি (PM-VISHWAKARMA)**\n  - পৰম্পৰাগত শিল্পীসকলৰ বাবে ৫% ৰেহাই সুতত ₹৩ লাখলৈকে ঋণ + ₹১৫,০০০ আধুনিক সঁজুলি অনুদান।"
        }
    }

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
        if any(w in msg_lower for w in ["vendor", "thela", "street", "10000", "50000", "patari", "feriwala", "वेंडर", "வியாபாரி", "వ్యాపారి"]):
            hl = cls.SCHEME_HIGHLIGHTS["svanidhi"].get(lang, cls.SCHEME_HIGHLIGHTS["svanidhi"]["en"])
            reply = f"{responses['found_schemes']}\n\n{hl}"
            return {
                "reply": reply,
                "source": "Rule Gazette Fallback",
                "language": lang,
                "matched_schemes": cls._extract_matching_schemes("svanidhi", schemes_db)
            }

        # Check for Women / Stand-Up India / Mudra
        if any(w in msg_lower for w in ["woman", "women", "female", "mahila", "sc", "st", "महिला", "பெண்", "మహిళ", "ಮಹಿಳೆ"]):
            hl = cls.SCHEME_HIGHLIGHTS["standup"].get(lang, cls.SCHEME_HIGHLIGHTS["standup"]["en"])
            reply = f"{responses['found_schemes']}\n\n{hl}"
            return {
                "reply": reply,
                "source": "Rule Gazette Fallback",
                "language": lang,
                "matched_schemes": cls._extract_matching_schemes("standup mudra", schemes_db)
            }

        # General high subsidy / PMEGP / Vishwakarma
        hl = cls.SCHEME_HIGHLIGHTS["pmegp"].get(lang, cls.SCHEME_HIGHLIGHTS["pmegp"]["en"])
        reply = f"{responses['found_schemes']}\n\n{hl}"

        return {
            "reply": reply,
            "source": "Rule Gazette Fallback",
            "language": lang,
            "matched_schemes": cls._extract_matching_schemes("pmegp", schemes_db)
        }
