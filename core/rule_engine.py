import re

# Weighted Sentiment Rules

POSITIVE_RULES = {
    # Strong Positive
    "excellent": 3, "amazing": 3, "fantastic": 3, "outstanding": 3,
    "brilliant": 3, "superb": 3, "awesome": 3, "incredible": 3,
    "perfect": 3, "wonderful": 3, "best": 3,

    # Moderate Positive 
    "great": 2, "good": 2, "nice": 2, "love": 2,
    "satisfied": 2, "happy": 2, "pleased": 2,
    "impressive": 2, "enjoyed": 2, "valuable": 2,
    "reliable": 2, "efficient": 2,

    # Mild Positive 
    "fine": 1, "decent": 1, "ok": 1, "okay": 1,
    "useful": 1, "smooth": 1, "fast": 1,
    "clean": 1, "simple": 1, "easy": 1
}

# ---------------- NEGATIVE WORDS ----------------
NEGATIVE_RULES = {
    # Strong Negative 
    "terrible": -3, "awful": -3, "worst": -3,
    "horrible": -3, "disaster": -3, "pathetic": -3,
    "useless": -3, "broken": -3, "hate": -3,

    # Moderate Negative
    "bad": -2, "poor": -2, "disappointed": -2,
    "annoying": -2, "slow": -2, "difficult": -2,
    "problem": -2, "issue": -2, "waste": -2,
    "boring": -2, "confusing": -2,

    # Mild Negative 
    "not": -1, "lag": -1, "delay": -1,
    "hard": -1, "weak": -1, "low": -1,
    "bug": -1, "error": -1, "fail": -1
}

def score_text(text):
    text = text.lower()

    words = re.findall(r'\b\w+\b', text)

    score = 0

    for word in words:
        if word in POSITIVE_RULES:
            score += POSITIVE_RULES[word]

        if word in NEGATIVE_RULES:
            score += NEGATIVE_RULES[word]

    return score