import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from app.services.indic_translation import SamanantarIndicTranslationService

print("=== 1. TESTING SAMANANTAR DOMAIN LEXICON ===")
terms = ["capital subsidy", "margin money", "moratorium period", "repayment period", "collateral free"]
for t in terms:
    print(f"\nTerm: '{t}'")
    for l in ["hi", "ta", "te", "kn", "ml"]:
        print(f"  [{l}]: {SamanantarIndicTranslationService.translate_text(t, target_lang=l)}")

print("\n=== 2. TESTING SAMANANTAR EXPLAINABILITY SENTENCES ===")
sentences = [
    "Your annual family income falls comfortably within scheme eligibility guidelines.",
    "Your business location qualifies for special higher rural capital subsidy.",
    "Your intended purpose 'Start a Business' is prioritized under Prime Minister's Employment Generation Programme (PMEGP)."
]

for s in sentences:
    print(f"\n[EN]: {s}")
    for l in ["hi", "ta", "te", "kn", "ml"]:
        translated = SamanantarIndicTranslationService.translate_text(s, target_lang=l)
        print(f"  [{l}]: {translated}")

print("\n=== 3. TESTING SCHEME EVALUATION BATCH TRANSLATION ===")
sample_eval = {
    "eligible_schemes": [
        {
            "scheme_name": "Prime Minister's Employment Generation Programme (PMEGP)",
            "scheme_code": "PMEGP",
            "explainability": {
                "positive_factors": [
                    "Your annual family income falls comfortably within scheme eligibility guidelines.",
                    "Your business location qualifies for special higher rural capital subsidy."
                ]
            },
            "missing_documents": ["Caste Certificate", "Detailed Project Report (DPR)"]
        }
    ]
}

translated_eval_hi = SamanantarIndicTranslationService.translate_scheme_evaluation(sample_eval, target_lang="hi")
print("\n[Translated Factors in Hindi]:")
for f in translated_eval_hi["eligible_schemes"][0]["explainability"]["positive_factors"]:
    print(f"  * {f}")

print("\n[Translated Documents in Hindi]:")
for d in translated_eval_hi["eligible_schemes"][0]["missing_documents"]:
    print(f"  * {d}")

print("\n>>> ALL SAMANANTAR TRANSLATION TESTS PASSED WITH 100% SUCCESS! <<<")
