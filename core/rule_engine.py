import re

# -------------------------
# Weighted Sentiment Rules
# -------------------------

POSITIVE_RULES = {
    "excellent": 3,
    "amazing": 3,
    "fantastic": 3,
    "great": 2,
    "good": 1,
    "nice": 1,
    "love": 2,
    "wonderful": 3,
    "perfect": 2,
    "satisfied": 2
}

NEGATIVE_RULES = {
    "terrible": -3,
    "awful": -3,
    "worst": -3,
    "bad": -2,
    "poor": -2,
    "hate": -3,
    "disappointed": -2,
    "horrible": -3,
    "useless": -2,
    "slow": -1
}

def score_text(text):
    """
    Calculate weighted sentiment score based on rule matching.
    """
    text = text.lower()

    words = re.findall(r'\b\w+\b', text)

    score = 0

    for word in words:
        if word in POSITIVE_RULES:
            score += POSITIVE_RULES[word]

        if word in NEGATIVE_RULES:
            score += NEGATIVE_RULES[word]

    return score