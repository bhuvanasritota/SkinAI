from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from src.recommender import recommend_products_v2

from .database import (
    Base,
    engine,
    get_db
)

from . import models

from .models import (
    User,
    UserProfile
)

from .schemas import (
    UserCreate,
    LoginRequest,
    ProfileCreate,
    ProfileResponse
)

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="SkinAI API",
    description="AI-powered Personalized Skincare Recommendation API",
    version="1.0.0"
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# REQUEST MODELS
# ============================================================

class RecommendationRequest(BaseModel):

    skin_type: str

    concerns: list[str]


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "SkinAI API is running!"
    }


# ============================================================
# SIGNUP
# ============================================================

@app.post("/auth/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/auth/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user.email
        )
        .first()
    )

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        user.password,
        existing_user.password_hash
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        existing_user.id
    )

    return {
        "message": "Login successful",

        "access_token": access_token,

        "token_type": "bearer",

        "user_id": existing_user.id,

        "name": existing_user.name,

        "email": existing_user.email
    }


# ============================================================
# GET CURRENT USER
# ============================================================

@app.get("/auth/me")
def get_me(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


# ============================================================
# CREATE / UPDATE PROFILE
# ============================================================

@app.post(
    "/profile",
    response_model=ProfileResponse
)
def create_or_update_profile(
    profile: ProfileCreate,

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db)
):

    if not profile.concerns:

        raise HTTPException(
            status_code=400,
            detail="At least one concern is required"
        )

    existing_profile = (
        db.query(UserProfile)
        .filter(
            UserProfile.user_id == user_id
        )
        .first()
    )

    if existing_profile:

        existing_profile.skin_type = (
            profile.skin_type
        )

        existing_profile.concerns = (
            profile.concerns
        )

        existing_profile.age_range = (
            profile.age_range
        )

        existing_profile.product_preferences = (
            profile.product_preferences
        )

        existing_profile.budget = (
            profile.budget
        )

        existing_profile.ingredients_to_avoid = (
            profile.ingredients_to_avoid
        )

    else:

        existing_profile = UserProfile(
            user_id=user_id,
            skin_type=profile.skin_type,
            concerns=profile.concerns,
            age_range=profile.age_range,
            product_preferences=(
                profile.product_preferences
            ),
            budget=profile.budget,
            ingredients_to_avoid=(
                profile.ingredients_to_avoid
            )
        )

        db.add(existing_profile)

    db.commit()

    db.refresh(existing_profile)

    return existing_profile


# ============================================================
# GET PROFILE
# ============================================================

@app.get(
    "/profile",
    response_model=ProfileResponse
)
def get_profile(
    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db)
):

    profile = (
        db.query(UserProfile)
        .filter(
            UserProfile.user_id == user_id
        )
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


# ============================================================
# DIRECT RECOMMENDATION API
# ============================================================

@app.post("/recommendations")
def get_recommendations(
    request: RecommendationRequest
):

    recommendations = recommend_products_v2(
        request.skin_type,
        request.concerns,
        top_k=5
    )

    return recommendations.to_dict(
        orient="records"
    )


# ============================================================
# AUTHENTICATED RECOMMENDATIONS
# ============================================================

@app.get("/recommendations")
def get_my_recommendations(
    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db)
):

    profile = (
        db.query(UserProfile)
        .filter(
            UserProfile.user_id == user_id
        )
        .first()
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Please complete your skin profile first"
        )

    recommendations = recommend_products_v2(
        profile.skin_type,
        profile.concerns,
        top_k=5
    )

    return {
        "recommendations":
            recommendations.to_dict(
                orient="records"
            )
    }