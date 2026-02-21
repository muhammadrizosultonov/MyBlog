from typing import Dict


def detect_language(message: str) -> str:
    text = (message or "").lower()
    uzbek_markers = [
        "salom",
        "assalomu",
        "rahmat",
        "qanday",
        "nima",
        "qayer",
        "necha",
        "ha",
        "yoq",
        "yo'q",
        "men",
        "siz",
        "menga",
        "bo'ladi",
        "boladi",
        "tavsiyalar",
        "loyiha",
        "blog",
        "ishda",
    ]
    if any(marker in text for marker in uzbek_markers):
        return "uz"
    return "en"


def build_system_prompt(context_text: str, language: str) -> str:
    if language == "uz":
        language_rule = "Answer in Uzbek."
        refusal = (
            "Kechirasiz, men faqat Muhammadrizo va uning portfeli, loyihalari yoki blogi haqida javob bera olaman."
        )
        unknown = "Bu savol bo'yicha aniq ma'lumot topilmadi."
    else:
        language_rule = "Answer in English."
        refusal = (
            "Sorry, I can only answer questions about Muhammadrizo and his portfolio, projects, or blog."
        )
        unknown = "No exact information is available for this question."

    return (
        "You are a strict assistant for Muhammadrizo's personal portfolio website.\n"
        "RULES:\n"
        "1) Use ONLY the context below.\n"
        "2) If the question is unrelated to Muhammadrizo, respond with the refusal sentence exactly.\n"
        "3) If relevant but missing info, respond with the unknown sentence exactly.\n"
        "4) Be concise (2-5 sentences max), professional, and deterministic.\n"
        f"5) {language_rule}\n"
        f"Refusal: {refusal}\n"
        f"Unknown: {unknown}\n\n"
        "Context:\n"
        f"{context_text}"
    )
