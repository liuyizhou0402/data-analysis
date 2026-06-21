"""
Diabetes Risk Assessment API
=============================
FastAPI service exposing the trained XGBoost model as a REST API.

Endpoints:
  GET  /              - service status
  GET  /health        - health check (with model probe)
  POST /predict       - single-patient risk prediction
  POST /predict/batch - batch prediction (up to 500 patients)
  GET  /docs          - auto-generated Swagger UI

Enterprise features:
  - Pydantic input validation (invalid values return 422, not model crash)
  - Prediction audit log (CSV, required for clinical compliance)
  - SHAP explainability on every prediction
  - Batch endpoint for bulk screening workflows
  - lifespan context manager (modern FastAPI pattern)
"""

import csv
import shap
import joblib
import logging
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    PatientInput, PredictionResponse, BatchInput,
    RiskLevel, RiskFactor,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR   = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "outputs/models/xgb_diabetes_risk_model.pkl"
LOG_PATH   = BASE_DIR / "outputs/prediction_log.csv"

CATEGORICAL = ["sex", "ethnicity", "smoking_status", "remoteness"]
NUMERIC = [
    "age", "bmi", "waist_cm", "systolic_bp",
    "fasting_glucose_mmol", "hba1c_pct", "cholesterol_mmol",
    "physical_activity_days_pw", "diet_quality_score",
    "family_history_diabetes", "prev_gestational_dm",
    "hypertension", "cvd_history", "depression_anxiety",
    "seifa_decile", "alcohol_risk_level",
]

# ---------------------------------------------------------------------------
# Lifespan — defined BEFORE FastAPI() so the name exists at instantiation
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    if not MODEL_PATH.exists():
        raise RuntimeError("Model not found. Run src/02_modeling.py first.")

    _pipeline    = joblib.load(MODEL_PATH)
    _preprocessor = _pipeline.named_steps["preprocessor"]
    _xgb_clf     = _pipeline.named_steps["classifier"]
    _explainer   = shap.TreeExplainer(_xgb_clf)
    _cat_names   = (_preprocessor.named_transformers_["cat"]
                    .get_feature_names_out(CATEGORICAL).tolist())

    application.state.pipeline      = _pipeline
    application.state.preprocessor  = _preprocessor
    application.state.explainer     = _explainer
    application.state.feature_names = NUMERIC + _cat_names

    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "w", newline="") as f:
            csv.writer(f).writerow([
                "timestamp", "patient_id", "risk_probability",
                "risk_level", "top_factor_1", "top_factor_2",
            ])

    logger.info("Model loaded. API ready.")
    yield
    # shutdown — add cleanup here if needed

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    lifespan=lifespan,
    title="Australian Diabetes Risk Assessment API",
    description=(
        "Predicts Type 2 diabetes risk for adult patients in Australian "
        "primary care using an XGBoost model trained on AUSDRISK-aligned features. "
        "Every prediction includes SHAP-based explanations.\n\n"
        "**Model:** xgb-v1.0 | **ROC-AUC:** 0.895 | **PR-AUC:** 0.377"
    ),
    version="1.0.0",
    contact={"name": "Portfolio",
             "url": "https://github.com/liuyizhou0402/data-analysis"},
)

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# ---------------------------------------------------------------------------
# Core prediction logic
# ---------------------------------------------------------------------------
def _predict_single(patient: PatientInput, patient_id: str,
                    request: Request) -> PredictionResponse:
    pipeline      = request.app.state.pipeline
    preprocessor  = request.app.state.preprocessor
    explainer     = request.app.state.explainer
    feature_names = request.app.state.feature_names

    df   = pd.DataFrame([patient.model_dump()])
    prob = float(pipeline.predict_proba(df)[0, 1])

    if prob < 0.05:
        level = RiskLevel.low
        rec   = "Routine review in 3 years. Encourage healthy lifestyle."
    elif prob < 0.15:
        level = RiskLevel.moderate
        rec   = "Lifestyle intervention recommended. Review in 12 months."
    else:
        level = RiskLevel.high
        rec   = ("Refer for HbA1c/fasting glucose test. "
                 "Consider diabetes prevention program.")

    X_tr       = preprocessor.transform(df)
    shap_vals  = explainer.shap_values(X_tr)[0]
    shap_s     = pd.Series(shap_vals, index=feature_names)
    top_feats  = shap_s.abs().nlargest(6).index

    top_factors = [
        RiskFactor(
            feature=f,
            shap_value=round(float(shap_s[f]), 4),
            direction="increases_risk" if shap_s[f] > 0 else "reduces_risk",
        )
        for f in top_feats
    ]

    with open(LOG_PATH, "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.now(timezone.utc).isoformat(),
            patient_id, round(prob, 4), level.value,
            top_factors[0].feature if top_factors else "",
            top_factors[1].feature if len(top_factors) > 1 else "",
        ])

    return PredictionResponse(
        patient_id=patient_id,
        risk_probability=round(prob, 4),
        risk_probability_pct=f"{prob*100:.1f}%",
        risk_level=level,
        recommendation=rec,
        top_risk_factors=top_factors,
    )

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Status"])
async def root():
    return {"service": "Australian Diabetes Risk Assessment API",
            "version": "1.0.0", "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Status"])
async def health_check(request: Request):
    try:
        probe = PatientInput(
            age=40, sex="Male", ethnicity="European",
            remoteness="Major City", bmi=25.0, waist_cm=85.0,
            systolic_bp=120, fasting_glucose_mmol=5.0, hba1c_pct=5.2,
            cholesterol_mmol=5.0, physical_activity_days_pw=3,
            smoking_status="Never", alcohol_risk_level=1,
            diet_quality_score=6, family_history_diabetes=0,
            prev_gestational_dm=0, hypertension=0, cvd_history=0,
            depression_anxiety=0, seifa_decile=5,
        )
        result = _predict_single(probe, "health-check", request)
        return {"status": "healthy", "model": "loaded",
                "test_prediction": result.risk_probability,
                "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {e}")


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(patient: PatientInput, request: Request,
                  patient_id: str = "unknown"):
    """Single-patient diabetes risk prediction with SHAP explanation."""
    try:
        return _predict_single(patient, patient_id, request)
    except Exception as e:
        logger.error(f"Prediction error for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(body: BatchInput, request: Request):
    """Batch prediction for up to 500 patients (clinic bulk screening)."""
    ids = body.patient_ids or [f"PT-{i+1:04d}" for i in range(len(body.patients))]
    if len(ids) != len(body.patients):
        raise HTTPException(status_code=422,
                            detail="patient_ids length must match patients length.")

    results, errors = [], []
    for pid, patient in zip(ids, body.patients):
        try:
            results.append(_predict_single(patient, pid, request))
        except Exception as e:
            errors.append({"patient_id": pid, "error": str(e)})

    return {
        "total": len(body.patients),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors,
        "high_risk_count":     sum(1 for r in results if r.risk_level == RiskLevel.high),
        "moderate_risk_count": sum(1 for r in results if r.risk_level == RiskLevel.moderate),
    }
