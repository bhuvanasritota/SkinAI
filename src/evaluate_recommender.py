
import sys
from pathlib import Path

# Allow imports from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import (
    products_clean,
    recommend_products_v2,
)


def evaluate_profile(skin_type, concerns):
    print("\n" + "=" * 70)
    print(f"Skin type: {skin_type}")
    print(f"Selected concerns: {concerns}")
    print("=" * 70)

    # Generate recommendations
    recommendations = recommend_products_v2(
        skin_type=skin_type,
        concerns=concerns,
        top_k=5,
    )

    # Find all products compatible with the selected skin type
    eligible_products = products_clean[
        products_clean["skin_type"].apply(
            lambda value: skin_type.casefold()
            in [
                item.strip().casefold()
                for item in str(value).split(",")
            ]
        )
    ].copy()

    # Count how many selected concerns each eligible product matches
    eligible_products["matched_count"] = (
        eligible_products["concern"].apply(
            lambda value: sum(
                concern in [
                    item.strip()
                    for item in str(value).split(",")
                ]
                for concern in concerns
            )
        )
    )

    total_eligible = len(eligible_products)

    products_with_any_match = (
        eligible_products["matched_count"] > 0
    ).sum()

    products_with_all_matches = (
        eligible_products["matched_count"] == len(concerns)
    ).sum()

    print("\nConcern Matching Analysis")
    print(f"Eligible products: {total_eligible}")
    print(
        "Products matching at least one concern: "
        f"{products_with_any_match}"
    )
    print(
        "Products matching all concerns: "
        f"{products_with_all_matches}"
    )

    if recommendations.empty:
        print("\nNo eligible products found.")
        return

    # Check 1: Every recommendation matches the selected skin type
    invalid_skin_matches = recommendations[
        ~recommendations["skin_type"].apply(
            lambda value: skin_type.casefold()
            in [
                item.strip().casefold()
                for item in str(value).split(",")
            ]
        )
    ]

    assert invalid_skin_matches.empty, (
        "A recommendation does not match the selected skin type."
    )

    # Check 2: Scores are in descending order
    scores = recommendations["final_score"].tolist()

    assert scores == sorted(scores, reverse=True), (
        "Recommendations are not sorted by final score."
    )

    # Check 3: Scores are between 0 and 1
    assert recommendations["final_score"].between(
        0, 1
    ).all(), "A final score is outside the expected range."

    print("\nTop recommendations:")

    display_columns = [
        "product",
        "skin_type",
        "concern",
        "final_score",
        "matched_concerns",
    ]

    print(
        recommendations[display_columns].to_string(
            index=False
        )
    )

    print("\nChecks passed:")
    print("- All recommendations match the selected skin type.")
    print("- Recommendations are sorted by score.")
    print("- Final scores are within [0, 1].")


def main():
    print("SKINAI V1 BASELINE EVALUATION")
    print(f"\nTotal products in dataset: {len(products_clean)}")

    available_skin_types = sorted({
        item.strip()
        for values in products_clean["skin_type"].dropna()
        for item in str(values).split(",")
    })

    print("Available skin types:", available_skin_types)

    test_profiles = [
        ("Oily", ["Acne", "Pores"]),
        ("Dry", ["Hydration", "Skin soothing"]),
        ("Sensitive", ["Irritation", "Acne"]),
    ]

    for skin_type, concerns in test_profiles:
        try:
            evaluate_profile(skin_type, concerns)
        except (AssertionError, ValueError, KeyError) as error:
            print(f"\nEvaluation failed: {error}")


if __name__ == "__main__":
    main()
