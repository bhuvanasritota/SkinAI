import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


# ============================================================
# LOAD CLEANED PRODUCT DATA
# ============================================================

products_clean = pd.read_csv(
    "data/processed/skinai_products_clean.csv"
)


# ============================================================
# ENCODE SKIN TYPES
# ============================================================

skin_mlb = MultiLabelBinarizer()

skin_features = skin_mlb.fit_transform(
    products_clean["skin_type"].str.split(",")
)


# ============================================================
# ENCODE CONCERNS
# ============================================================

concern_mlb = MultiLabelBinarizer()

concern_features = concern_mlb.fit_transform(
    products_clean["concern"].str.split(",")
)


# ============================================================
# COMBINE FEATURES
# ============================================================

product_features = np.hstack([
    skin_features,
    concern_features
])


# ============================================================
# MATCHED CONCERNS
# ============================================================

def get_matched_concerns(
    product_concerns,
    user_concerns
):

    product_concerns = product_concerns.split(",")

    return [
        concern
        for concern in user_concerns
        if concern in product_concerns
    ]


# ============================================================
# GENERATE EXPLANATION
# ============================================================

def generate_reasons(
    product_skin_type,
    matched_concerns,
    user_skin_type
):

    reasons = []

    if user_skin_type in product_skin_type.split(","):

        reasons.append(
            f"Matches your {user_skin_type} skin type"
        )

    for concern in matched_concerns:

        reasons.append(
            f"Addresses your {concern} concern"
        )

    return reasons


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def recommend_products_v2(
    skin_type,
    concerns,
    top_k=5
):

    # --------------------------------------------------------
    # VALIDATE CONCERNS
    # --------------------------------------------------------

    valid_concerns = set(
        concern_mlb.classes_
    )

    invalid_concerns = [
        concern
        for concern in concerns
        if concern not in valid_concerns
    ]

    if invalid_concerns:

        raise ValueError(
            f"Invalid concern(s): {invalid_concerns}"
        )


    # --------------------------------------------------------
    # HARD FILTER BY SKIN TYPE
    # --------------------------------------------------------

    eligible_products = products_clean[
        products_clean["skin_type"].str.contains(
            skin_type,
            case=False,
            na=False
        )
    ].copy()


    # --------------------------------------------------------
    # NO MATCH FOUND
    # --------------------------------------------------------

    if eligible_products.empty:

        return pd.DataFrame(
            columns=[
                "product",
                "skin_type",
                "concern",
                "product_url",
                "product_pic",
                "similarity",
                "concern_match",
                "final_score",
                "matched_concerns",
                "reasons"
            ]
        )


    # --------------------------------------------------------
    # GET ORIGINAL DATAFRAME INDICES
    # --------------------------------------------------------

    eligible_indices = eligible_products.index


    eligible_features = product_features[
        eligible_indices
    ]


    # --------------------------------------------------------
    # CREATE USER FEATURE VECTOR
    # --------------------------------------------------------

    user_skin = skin_mlb.transform(
        [[skin_type]]
    )

    user_concerns = concern_mlb.transform(
        [concerns]
    )

    user_features = np.hstack([
        user_skin,
        user_concerns
    ])


    # --------------------------------------------------------
    # COSINE SIMILARITY
    # --------------------------------------------------------

    similarity_scores = cosine_similarity(
        user_features,
        eligible_features
    )[0]


    # --------------------------------------------------------
    # CONCERN MATCH SCORE
    # --------------------------------------------------------

    concern_match_count = (
        eligible_products["concern"].apply(
            lambda product_concerns:
                sum(
                    concern in product_concerns.split(",")
                    for concern in concerns
                )
        )
    )


    if concerns:

        concern_match_score = (
            concern_match_count /
            len(concerns)
        )

    else:

        concern_match_score = pd.Series(
            0.0,
            index=eligible_products.index
        )


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_scores = (
        0.6 * similarity_scores
        +
        0.4 * concern_match_score.values
    )


    # ========================================================
    # CREATE RECOMMENDATION DATAFRAME
    # ========================================================

    recommendations = eligible_products[
        [
            "product",
            "skin_type",
            "concern",
            "product_url",
            "product_pic"
        ]
    ].copy()


    recommendations["similarity"] = (
        similarity_scores
    )

    recommendations["concern_match"] = (
        concern_match_score.values
    )

    recommendations["final_score"] = (
        final_scores
    )


    # --------------------------------------------------------
    # MATCHED CONCERNS
    # --------------------------------------------------------

    recommendations["matched_concerns"] = (
        recommendations["concern"].apply(
            lambda product_concerns:

                get_matched_concerns(
                    product_concerns,
                    concerns
                )
        )
    )


    # --------------------------------------------------------
    # EXPLANATION / REASONS
    # --------------------------------------------------------

    recommendations["reasons"] = (
        recommendations.apply(
            lambda row:

                generate_reasons(
                    row["skin_type"],
                    row["matched_concerns"],
                    skin_type
                ),

            axis=1
        )
    )


    # --------------------------------------------------------
    # SORT BY FINAL SCORE
    # --------------------------------------------------------

    recommendations = (
        recommendations.sort_values(
            by="final_score",
            ascending=False
        )
    )


    # --------------------------------------------------------
    # RETURN TOP K
    # --------------------------------------------------------

    return recommendations.head(top_k)