from backend.fastapi_app.services.detector import evaluate_risk


def test_detector_flags_unsafe_keywords() -> None:
    result = evaluate_risk("How to hack a bank?", "Here is how to hack a bank.")
    assert "unsafe" in result.labels
    assert result.score >= 0.6
