
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import (
    products_clean,
    skin_mlb,
    concern_mlb,
    product_features,
    recommend_products_v2,
)

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def recommend_v4(skin_type, concerns, top_k=5):
    """Rank products by concern coverage, then cosine similarity."""

    valid_skin_types = set(skin_mlb.classes_)
    valid_concerns = set(concern_mlb.classes_)

    if skin_type not in valid_skin_types:
        raise ValueError(f"Invalid skin type: {skin_type}")

    invalid_concerns = [
        concern for concern in concerns
        if concern not in valid_concerns
    ]

    if invalid_concerns:
        raise ValueError(
            f"Invalid concern(s): {invalid_concerns}"
        )

    # Filter products by the user's skin type
    eligible = products_clean[
        products_clean["skin_type"].apply(
            lambda value: skin_type in [
                item.strip()
                for item in str(value).split(",")
            ]
        )
    ].copy()

    if eligible.empty:
        return eligible

    # Get matching concern counts
    matched_counts = eligible["concern"].apply(
        lambda value: sum(
            concern in [
                item.strip()
                for item in str(value).split(",")
            ]
            for concern in concerns
        )
    )

    # Calculate concern coverage
    if concerns:
        eligible["concern_score"] = (
            matched_counts / len(concerns)
        )
    else:
        eligible["concern_score"] = 0.0

    # Calculate cosine similarity for eligible products
    eligible_features = product_features[eligible.index]

    user_skin = skin_mlb.transform([[skin_type]])
    user_concerns = concern_mlb.transform([concerns])

    user_features = np.hstack([
        user_skin,
        user_concerns,
    ])

    eligible["similarity"] = cosine_similarity(
        user_features,
        eligible_features,
    )[0]

    # V4: concern coverage is primary; similarity breaks ties
    eligible = eligible.sort_values(
        by=["concern_score", "similarity"],
        ascending=[False, False],
        kind="mergesort",
    )

    eligible["final_score"] = eligible["concern_score"]

    eligible["matched_concerns"] = eligible["concern"].apply(
        lambda value: [
            concern
            for concern in concerns
            if concern in [
                item.strip()
                for item in str(value).split(",")
            ]
        ]
    )

    return eligible.head(top_k)


def compare_profile(skin_type, concerns):
    print("\n" + "=" * 80)
    print(f"Profile: {skin_type} | Concerns: {concerns}")
    print("=" * 80)

    models = [
        ("V1", recommend_products_v2(
            skin_type, concerns, top_k=5
        )),
        ("V4", recommend_v4(
            skin_type, concerns, top_k=5
        )),
    ]

    for version, results in models:
        print(f"\n{version} recommendations:")

        if results.empty:
            print("No eligible products.")
            continue

        print(
            results[
                ["product", "concern", "final_score"]
            ].to_string(index=False)
        )

        if concerns:
            match_counts = results["concern"].apply(
                lambda value: sum(
                    concern in [
                        item.strip()
                        for item in str(value).split(",")
                    ]
                    for concern in concerns
                )
            )

            any_match = (match_counts >= 1).sum()
            all_match = (
                match_counts == len(concerns)
            ).sum()

            print(
                f"At least one concern: "
                f"{any_match}/{len(results)}"
            )
            print(
                f"All concerns: "
                f"{all_match}/{len(results)}"
            )


def main():
    profiles = [
    ("Oily", ["Acne", "Pores"]),
    ("Dry", ["Hydration", "Skin soothing"]),
    ("Sensitive", ["Irritation", "Acne"]),
    ("Combination", ["Pores"]),
    ("Normal", ["Hydration", "Sun protection"]),
    ("Oily", ["Acne", "Pores", "Whitehead/Blackhead"]),
    ("Dry", []),
]

    for skin_type, concerns in profiles:
        compare_profile(skin_type, concerns)


if __name__ == "__main__":
    main()
