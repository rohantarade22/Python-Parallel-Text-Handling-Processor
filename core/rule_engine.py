positive_words = ["good", "excellent", "happy", "great", "amazing"]
negative_words = ["bad", "terrible", "sad", "poor", "worst"]

def score_text(text):
    score = 0
    words = text.lower().split()

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    return score