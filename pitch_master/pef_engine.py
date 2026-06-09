"""Pitch Master — PEF-100 Scoring Engine (v0.1 Heuristic).

This is a heuristic v0.1 score, not investment advice.
It uses simple text analysis to estimate pitch deck quality.

The real PEF-100 is a 23-variable measurement system validated through
inter-rater reliability and factor analysis. This simplified version
provides a rough approximation for the open-source tool.
"""

from __future__ import annotations

import re
import math


# Keyword sets for each layer
KEYWORDS = {
    "problem": ["problem", "challenge", "pain", "frustration", "struggle", "issue", "gap"],
    "solution": ["solution", "solve", "address", "approach", "method", "platform", "tool"],
    "market": ["market", "tam", "sam", "som", "billion", "million", "addressable", "opportunity"],
    "traction": ["traction", "revenue", "users", "growth", "mrr", "arr", "customers", "pilot", "loi"],
    "team": ["team", "founder", "ceo", "cto", "experience", "background", "serial", "expert"],
    "why_now": ["now", "timing", "regulation", "shift", "trend", "momentum", "window"],
    "business_model": ["pricing", "subscription", "saas", "revenue model", "unit economics", "margin"],
    "ask": ["raising", "funding", "invest", "round", "seed", "series", "ask", "use of funds"],
    "funding": ["fundraise", "capital", "investment", "raise", "raised"],
}

# Cognitive friction indicators
FRICTION_WORDS = [
    "however", "although", "nevertheless", "notwithstanding",
    "complexity", "nuance", "caveat", "it depends",
    "unclear", "ambiguous", "confusing", "uncertain",
]

# Red flag patterns
RED_FLAGS = [
    (r" guaranteed returns? ", "Guaranteed returns claim"),
    (r" no competition ", "No competition claim"),
    (r" first (?:mover|to market) ", "First mover claim without evidence"),
    (r" disruption ", "Buzzword without substance"),
    (r" ai .* (?:will|going to) ", "AI hype without specifics"),
    (r" (?:10x|100x|1000x) ", "Unrealistic multiplier claims"),
    (r" no risk ", "No risk claim"),
    (r" (?:patent|patented) pending ", "Patent pending claim"),
]


def _count_words(text: str) -> int:
    return len(text.split())


def _count_pages(text: str) -> int:
    return max(1, text.count("\f") + 1)


def _avg_sentence_length(text: str) -> float:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    return sum(len(s.split()) for s in sentences) / len(sentences)


def _readability_score(text: str) -> float:
    """Simple readability estimate (0-100, higher = easier to read)."""
    words = text.split()
    if not words:
        return 50
    avg_word_len = sum(len(w) for w in words) / len(words)
    avg_sent_len = _avg_sentence_length(text)
    # Simplified Flesch-like score
    score = 100 - (avg_word_len * 5) - (avg_sent_len * 0.8)
    return max(0, min(100, score))


def _keyword_presence(text: str, keywords: list[str]) -> float:
    """Fraction of keywords present in text (0-1)."""
    if not keywords:
        return 0
    text_lower = text.lower()
    found = sum(1 for kw in keywords if kw.lower() in text_lower)
    return found / len(keywords)


def _count_red_flags(text: str) -> list[str]:
    """Find red flags in text."""
    flags = []
    text_lower = text.lower()
    for pattern, label in RED_FLAGS:
        if re.search(pattern, text_lower):
            flags.append(label)
    return flags


def _count_friction(text: str) -> float:
    """Count cognitive friction words (0-1, higher = more friction)."""
    words = text.lower().split()
    if not words:
        return 0
    friction_count = sum(1 for w in words if w in FRICTION_WORDS)
    return min(1.0, friction_count / max(1, len(words) / 100))


def compute_pef100(text: str) -> dict:
    """Compute PEF-100 heuristic score from text.

    Args:
        text: Extracted text from pitch deck.

    Returns:
        Dictionary with layer scores, overall score, and metadata.
    """
    word_count = _count_words(text)
    page_count = _count_pages(text)
    readability = _readability_score(text)
    avg_sent_len = _avg_sentence_length(text)

    # --- ATTENTION layer (0-25) ---
    novelty = min(5, _keyword_presence(text, ["novel", "unique", "first", "new", "innovative", "breakthrough"]) * 5)
    relevance = min(5, _keyword_presence(text, KEYWORDS["problem"] + KEYWORDS["solution"]) * 5)
    energy = min(5, _keyword_presence(text, ["exciting", "massive", "huge", "incredible", "powerful", "transform"]) * 5)
    timing = min(5, _keyword_presence(text, KEYWORDS["why_now"]) * 5)
    attention = novelty + relevance + energy + timing

    # --- UNDERSTANDING layer (0-25) ---
    clarity = min(5, readability / 20)
    compression = min(5, max(0, 5 - (word_count / max(1, page_count) / 200)))
    structure = min(5, _keyword_presence(text, KEYWORDS["problem"] + KEYWORDS["solution"] + KEYWORDS["market"] + KEYWORDS["traction"] + KEYWORDS["team"]) * 5)
    visual_cog = min(5, max(0, 5 - (page_count / 10)))  # Too many pages = less visual
    understanding = clarity + compression + structure + visual_cog

    # --- BELIEF layer (0-25) ---
    proof = min(5, _keyword_presence(text, ["data", "evidence", "study", "research", "survey", "test", "validation"]) * 5)
    traction = min(5, _keyword_presence(text, KEYWORDS["traction"]) * 5)
    mechanism = min(5, _keyword_presence(text, KEYWORDS["solution"] + ["how it works", "technology", "algorithm", "process"]) * 5)
    market_logic = min(5, _keyword_presence(text, KEYWORDS["market"] + KEYWORDS["business_model"]) * 5)
    belief = proof + traction + mechanism + market_logic

    # --- TRUST layer (0-25) ---
    competence = min(5, _keyword_presence(text, KEYWORDS["team"] + ["years", "experience", "background", "serial"]) * 5)
    authenticity = min(5, max(0, 5 - _count_friction(text) * 5))
    founder_fit = min(5, _keyword_presence(text, ["myself", "personal", "own problem", "lived experience", "passion"]) * 5)
    exec_cred = min(5, _keyword_presence(text, KEYWORDS["team"] + ["exit", "ipo", "scaled", "built", "led"]) * 5)
    trust = competence + authenticity + founder_fit + exec_cred

    # --- FOMO layer (0-25) ---
    upside = min(5, _keyword_presence(text, KEYWORDS["market"] + ["billion", "trillion", "massive"]) * 5)
    momentum = min(5, _keyword_presence(text, KEYWORDS["traction"] + ["accelerating", "growing", "viral"]) * 5)
    scarcity = min(5, _keyword_presence(text, ["exclusive", "only", "first", "limited", "window"]) * 5)
    asymmetry = min(5, _keyword_presence(text, ["upside", "10x", "100x", "asymmetric", "power law"]) * 5)
    fomo = upside + momentum + scarcity + asymmetry

    # --- PENALTY layer ---
    cognitive_friction = _count_friction(text) * 10  # 0-10
    red_flags = _count_red_flags(text)
    perceived_risk = min(10, len(red_flags) * 2)

    # --- OVERALL PEF-100 ---
    positive_total = attention + understanding + belief + trust + fomo
    max_positive = 125  # 5 layers x 25
    penalty = cognitive_friction + perceived_risk
    max_penalty = 20

    pef_raw = (positive_total / max_positive) * 80 + ((max_penalty - penalty) / max_penalty) * 20
    pef_score = max(0, min(100, pef_raw))

    return {
        "pef100": round(pef_score, 1),
        "layers": {
            "attention": round(attention, 1),
            "understanding": round(understanding, 1),
            "belief": round(belief, 1),
            "trust": round(trust, 1),
            "fomo": round(fomo, 1),
        },
        "penalties": {
            "cognitive_friction": round(cognitive_friction, 1),
            "perceived_risk": round(perceived_risk, 1),
        },
        "variables": {
            "novelty": round(novelty, 1),
            "relevance": round(relevance, 1),
            "energy": round(energy, 1),
            "timing": round(timing, 1),
            "clarity": round(clarity, 1),
            "compression": round(compression, 1),
            "structure": round(structure, 1),
            "visual_cognition": round(visual_cog, 1),
            "proof": round(proof, 1),
            "traction": round(traction, 1),
            "mechanism": round(mechanism, 1),
            "market_logic": round(market_logic, 1),
            "competence": round(competence, 1),
            "authenticity": round(authenticity, 1),
            "founder_fit": round(founder_fit, 1),
            "exec_credibility": round(exec_cred, 1),
            "upside": round(upside, 1),
            "momentum": round(momentum, 1),
            "scarcity": round(scarcity, 1),
            "asymmetry": round(asymmetry, 1),
        },
        "metadata": {
            "word_count": word_count,
            "page_count": page_count,
            "readability": round(readability, 1),
            "avg_sentence_length": round(avg_sent_len, 1),
        },
        "red_flags": red_flags,
        "disclaimer": "This is a heuristic v0.1 score, not investment advice.",
    }
