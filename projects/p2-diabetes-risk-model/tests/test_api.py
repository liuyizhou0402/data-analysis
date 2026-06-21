"""
API 单元测试
=============
pytest + httpx 测试所有端点。

运行方式: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="module")
def client():
    # context manager triggers lifespan (startup/shutdown)
    with TestClient(app) as c:
        yield c

# ── 测试数据 ───────────────────────────────────────────────────────────────────
LOW_RISK_PATIENT = {
    "age": 28, "sex": "Female", "ethnicity": "European",
    "remoteness": "Major City",
    "bmi": 22.5, "waist_cm": 72.0, "systolic_bp": 115,
    "fasting_glucose_mmol": 4.6, "hba1c_pct": 4.9,
    "cholesterol_mmol": 4.2, "physical_activity_days_pw": 5,
    "smoking_status": "Never", "alcohol_risk_level": 1,
    "diet_quality_score": 8, "family_history_diabetes": 0,
    "prev_gestational_dm": 0, "hypertension": 0,
    "cvd_history": 0, "depression_anxiety": 0, "seifa_decile": 8,
}

HIGH_RISK_PATIENT = {
    "age": 67, "sex": "Male", "ethnicity": "Indigenous_Australian",
    "remoteness": "Remote",
    "bmi": 34.2, "waist_cm": 108.0, "systolic_bp": 158,
    "fasting_glucose_mmol": 6.4, "hba1c_pct": 6.1,
    "cholesterol_mmol": 6.2, "physical_activity_days_pw": 0,
    "smoking_status": "Current", "alcohol_risk_level": 2,
    "diet_quality_score": 2, "family_history_diabetes": 1,
    "prev_gestational_dm": 0, "hypertension": 1,
    "cvd_history": 1, "depression_anxiety": 1, "seifa_decile": 2,
}

# ── 状态端点测试 ───────────────────────────────────────────────────────────────
def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"


def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert data["model"] == "loaded"
    assert 0.0 <= data["test_prediction"] <= 1.0


# ── 预测端点测试 ───────────────────────────────────────────────────────────────
def test_predict_low_risk(client):
    r = client.post("/predict?patient_id=TEST-001", json=LOW_RISK_PATIENT)
    assert r.status_code == 200
    data = r.json()
    assert data["patient_id"] == "TEST-001"
    assert data["risk_level"] == "Low"
    assert data["risk_probability"] < 0.05
    assert len(data["top_risk_factors"]) > 0


def test_predict_high_risk(client):
    r = client.post("/predict?patient_id=TEST-002", json=HIGH_RISK_PATIENT)
    assert r.status_code == 200
    data = r.json()
    assert data["risk_level"] == "High"
    assert data["risk_probability"] > 0.15


def test_predict_response_schema(client):
    """验证返回结构包含所有必需字段。"""
    r = client.post("/predict", json=LOW_RISK_PATIENT)
    data = r.json()
    required_fields = [
        "patient_id", "risk_probability", "risk_probability_pct",
        "risk_level", "recommendation", "top_risk_factors",
        "model_version", "disclaimer",
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"


def test_shap_direction_consistency(client):
    """SHAP方向标签与符号一致。"""
    r = client.post("/predict", json=HIGH_RISK_PATIENT)
    for factor in r.json()["top_risk_factors"]:
        if factor["shap_value"] > 0:
            assert factor["direction"] == "increases_risk"
        else:
            assert factor["direction"] == "reduces_risk"


# ── 输入校验测试 ───────────────────────────────────────────────────────────────
def test_invalid_age_too_young(client):
    bad = {**LOW_RISK_PATIENT, "age": 10}   # 低于18岁
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_invalid_bmi_too_high(client):
    bad = {**LOW_RISK_PATIENT, "bmi": 999}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_invalid_blood_pressure(client):
    bad = {**LOW_RISK_PATIENT, "systolic_bp": 0}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_male_gestational_dm_rejected(client):
    """男性不能有妊娠期糖尿病。"""
    bad = {**LOW_RISK_PATIENT, "sex": "Male", "prev_gestational_dm": 1}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_invalid_smoking_status(client):
    bad = {**LOW_RISK_PATIENT, "smoking_status": "Occasionally"}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


# ── 批量预测测试 ───────────────────────────────────────────────────────────────
def test_batch_predict(client):
    payload = {
        "patients": [LOW_RISK_PATIENT, HIGH_RISK_PATIENT],
        "patient_ids": ["BATCH-001", "BATCH-002"],
    }
    r = client.post("/predict/batch", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["successful"] == 2
    assert data["failed"] == 0
    assert data["high_risk_count"] >= 1


def test_batch_mismatched_ids(client):
    """patient_ids 数量与 patients 不匹配应返回 422。"""
    payload = {
        "patients": [LOW_RISK_PATIENT, HIGH_RISK_PATIENT],
        "patient_ids": ["ONLY-ONE-ID"],
    }
    r = client.post("/predict/batch", json=payload)
    assert r.status_code == 422


def test_batch_empty_rejected(client):
    """空批次应返回 422。"""
    r = client.post("/predict/batch", json={"patients": []})
    assert r.status_code == 422
