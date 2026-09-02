from disclosure_snippets import DISCLOSURE_SNIPPETS

RISK_FLAG_KEYWORDS = {
    "litigation": ["litigation", "lawsuit"],
    "regulatory": ["regulatory", "regulator"],
    "customer_concentration": ["customers", "concentration"],
}

HEDGING_KEYWORDS = ["assuming", "cautiously", "visibility"]
CONFIDENT_KEYWORDS = ["confident", "approved"]


def extract_signals(snippet: str) -> dict:
    """Mock mode: keyword/regex rules, no LLM call."""
    text = snippet.lower()

    risk_flags = []
    for flag_name, keywords in RISK_FLAG_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            risk_flags.append(flag_name)

    hedging_detected = any(kw in text for kw in HEDGING_KEYWORDS)

    if any(kw in text for kw in CONFIDENT_KEYWORDS):
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }


if  __name__ == "__main__":
    for snippet in DISCLOSURE_SNIPPETS:
        result = extract_signals(snippet)
        print(f"\n{snippet[:60]}...")
        print(f"  risk_flags: {result['risk_flags']}")
        print(f"  hedging_detected: {result['hedging_detected']}")
        print(f"  sentiment: {result['sentiment']}")