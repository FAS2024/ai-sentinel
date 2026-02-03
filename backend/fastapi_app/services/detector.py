from dataclasses import dataclass


@dataclass
class RiskResult:
    """Structured risk output from the detector."""
    score: float
    labels: list[str]


UNSAFE_KEYWORDS = {
    "hack",
    "bomb",
    "kill",
    "weapon",
    "exploit",
    "phishing",
    "malware",
    "credit card",
    "illegal",
}

BIAS_KEYWORDS = {
    "all of them",
    "inferior",
    "superior",
    "hate",
    "stupid",
}

HALLUCINATION_HINTS = {
    "i guarantee",
    "100%",
    "always true",
}


def evaluate_risk(request_text: str, response_text: str) -> RiskResult:
    """Return a risk score and labels using lightweight keyword rules."""
    content = f"{request_text}\n{response_text}".lower()
    labels: list[str] = []
    score = 0.05

    if any(k in content for k in UNSAFE_KEYWORDS):
        labels.append("unsafe")
        score += 0.6

    if any(k in content for k in BIAS_KEYWORDS):
        labels.append("bias")
        score += 0.2

    if any(k in content for k in HALLUCINATION_HINTS):
        labels.append("hallucination_risk")
        score += 0.15

    if not labels:
        labels.append("clean")

    return RiskResult(score=min(score, 0.99), labels=labels)
