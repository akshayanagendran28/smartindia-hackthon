from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.indic_translation import SamanantarIndicTranslationService

router = APIRouter(prefix="/translate", tags=["IndicNLP Samanantar Translation"])

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "hi"
    source_language: str = "en"

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    target_language: str = "hi"
    source_language: str = "en"

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    target_language: str
    source_language: str
    engine: str = "AI4Bharat Samanantar IndicNLP"

class BatchTranslateResponse(BaseModel):
    translations: List[str]
    target_language: str
    engine: str = "AI4Bharat Samanantar IndicNLP"

@router.post("", response_model=TranslateResponse)
def translate_single_text(req: TranslateRequest):
    translated = SamanantarIndicTranslationService.translate_text(
        text=req.text,
        target_lang=req.target_language,
        source_lang=req.source_language
    )
    return TranslateResponse(
        original_text=req.text,
        translated_text=translated,
        target_language=req.target_language,
        source_language=req.source_language
    )

@router.post("/batch", response_model=BatchTranslateResponse)
def translate_multiple_texts(req: BatchTranslateRequest):
    translations = SamanantarIndicTranslationService.translate_batch(
        texts=req.texts,
        target_lang=req.target_language
    )
    return BatchTranslateResponse(
        translations=translations,
        target_language=req.target_language
    )

@router.get("/lexicon")
def get_domain_lexicon():
    return {
        "engine": "AI4Bharat Samanantar IndicNLP",
        "supported_languages": ["en", "hi", "ta", "te", "kn", "ml"],
        "lexicon": SamanantarIndicTranslationService.DOMAIN_LEXICON,
        "explainability_corpus_size": len(SamanantarIndicTranslationService.EXPLAINABILITY_CORPUS)
    }
