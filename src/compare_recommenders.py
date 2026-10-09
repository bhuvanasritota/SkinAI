
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
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def recommend_v3(skin_type, concerns, top_k=5):
    """Rank skin-type-compatible products by concern coverage."""

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

    matched_counts = eligible["concern"].apply(
        lambda value: sum(
            concern in [
                item.strip()
                for item in str(value).split(",")
            ]
            for concern in concerns
        )
    )

    if concerns:
        eligible["concern_score"] = (
            matched_counts / len(concerns)
        )
    else:
        eligible["concern_score"] = 0.0

    # V3 uses concern coverage as its ranking score.
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

    return eligible.sort_values(
        by="final_score",
        ascending=False,
    ).head(top_k)


def compare_profile(skin_type, concerns):
    print("\n" + "=" * 80)
    print(f"Profile: {skin_type} | Concerns: {concerns}")
    print("=" * 80)

    v1 = recommend_products_v2(
        skin_type, concerns, top_k=5
    )

    v3 = recommend_v3(
        skin_type, concerns, top_k=5
    )

    for version, results in [("V1", v1), ("V3", v3)]:
        print(f"\n{version} recommendations:")

        if results.empty:
            print("No eligible products.")
            continue

        print(
            results[
                ["product", "concern", "final_score"]
            ].to_string(index=False)
        )

        def count_matches(value):
            product_concerns = [
                item.strip()
                for item in str(value).split(",")
            ]
            return sum(
                concern in product_concerns
                for concern in concerns
            )

        match_counts = results["concern"].apply(
            count_matches
        )

        if concerns:
            any_match = (match_counts >= 1).sum()
            all_match = (
                match_counts == len(concerns)
            ).sum()

            print("\nRanking evaluation:")
            print(
                f"Top-{len(results)} products matching "
                f"at least one concern: "
                f"{any_match}/{len(results)}"
            )
            print(
                f"Top-{len(results)} products matching "
                f"all concerns: "
                f"{all_match}/{len(results)}"
            )

            print(
                "At-least-one-concern rate: "
                f"{any_match / len(results):.0%}"
            )
            print(
                "All-concerns match rate: "
                f"{all_match / len(results):.0%}"
            )
        else:
            print(
                "No concerns selected; concern-based "
                "ranking metrics are not applicable."
            )

def main():
    profiles = [
        ("Oily", ["Acne", "Pores"]),
        ("Dry", ["Hydration", "Skin soothing"]),
        ("Sensitive", ["Irritation", "Acne"]),
    ]

    for skin_type, concerns in profiles:
        compare_profile(skin_type, concerns)


if __name__ == "__main__":
    main()
