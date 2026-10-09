
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import recommend_products_v2
from src.compare_v4 import recommend_v4


def test_skin_type_filtering():
    results = recommend_products_v2(
        "Oily", ["Acne", "Pores"], top_k=5
    )

    for skin_types in results["skin_type"]:
        assert "Oily" in [
            item.strip()
            for item in skin_types.split(",")
        ]


def test_scores_are_sorted():
    results = recommend_products_v2(
        "Dry", ["Hydration", "Skin soothing"], top_k=5
    )

    scores = results["final_score"].tolist()
    assert scores == sorted(scores, reverse=True)


def test_invalid_concern_is_rejected():
    try:
        recommend_products_v2(
            "Oily", ["InvalidConcern"], top_k=5
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "An invalid concern should raise ValueError."
        )


def test_v4_empty_concerns():
    results = recommend_v4("Dry", [], top_k=5)

    assert len(results) <= 5
    assert "final_score" in results.columns

    if not results.empty:
        assert (results["final_score"] == 0).all()


def test_v4_matches_skin_type():
    results = recommend_v4(
        "Sensitive", ["Irritation", "Acne"], top_k=5
    )

    for skin_types in results["skin_type"]:
        assert "Sensitive" in [
            item.strip()
            for item in skin_types.split(",")
        ]


if __name__ == "__main__":
    tests = [
        test_skin_type_filtering,
        test_scores_are_sorted,
        test_invalid_concern_is_rejected,
        test_v4_empty_concerns,
        test_v4_matches_skin_type,
    ]

    failures = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as error:
            failures += 1
            print(f"FAIL: {test.__name__}: {error}")

    print(f"\nPassed: {len(tests) - failures}/{len(tests)}")
    print(f"Failed: {failures}/{len(tests)}")
