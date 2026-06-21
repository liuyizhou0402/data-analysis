"""
数据验证 Schema
================
Pydantic 模型定义 API 的输入和输出结构。

企业级意义：
- 输入校验在数据进入模型前发生，拦截非法值
- 自动生成 API 文档（Swagger UI）
- 类型错误返回 422，而非模型崩溃
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal
from enum import Enum


class SexEnum(str, Enum):
    male   = "Male"
    female = "Female"


class EthnicityEnum(str, Enum):
    european              = "European"
    asian                 = "Asian"
    indigenous_australian = "Indigenous_Australian"
    other                 = "Other"


class SmokingEnum(str, Enum):
    never      = "Never"
    ex_smoker  = "Ex-smoker"
    current    = "Current"


class RemotenessEnum(str, Enum):
    major_city      = "Major City"
    inner_regional  = "Inner Regional"
    outer_regional  = "Outer Regional"
    remote          = "Remote"


class PatientInput(BaseModel):
    """
    单个患者的临床和人口学特征。
    所有字段均有临床范围校验。
    """
    # 人口学
    age:       int   = Field(..., ge=18, le=110,  description="Age in years (18–110)")
    sex:       SexEnum
    ethnicity: EthnicityEnum
    remoteness: RemotenessEnum

    # 人体测量
    bmi:      float = Field(..., ge=10.0, le=80.0,  description="Body Mass Index (kg/m²)")
    waist_cm: float = Field(..., ge=40.0, le=200.0, description="Waist circumference (cm)")

    # 临床测量
    systolic_bp:          int   = Field(..., ge=60,  le=250,  description="Systolic blood pressure (mmHg)")
    fasting_glucose_mmol: float = Field(..., ge=2.0, le=30.0, description="Fasting plasma glucose (mmol/L)")
    hba1c_pct:            float = Field(..., ge=3.0, le=20.0, description="HbA1c (%)")
    cholesterol_mmol:     float = Field(..., ge=1.0, le=15.0, description="Total cholesterol (mmol/L)")

    # 生活方式
    physical_activity_days_pw: int   = Field(..., ge=0, le=7,  description="Days/week of physical activity")
    smoking_status:            SmokingEnum
    alcohol_risk_level:        int   = Field(..., ge=0, le=2,  description="0=none, 1=low, 2=risky")
    diet_quality_score:        int   = Field(..., ge=1, le=10, description="Diet quality score (1=poor, 10=excellent)")

    # 病史
    family_history_diabetes: int = Field(..., ge=0, le=1, description="First-degree relative with T2DM (0/1)")
    prev_gestational_dm:     int = Field(..., ge=0, le=1, description="Previous gestational diabetes (0/1)")
    hypertension:            int = Field(..., ge=0, le=1, description="Hypertension diagnosis (0/1)")
    cvd_history:             int = Field(..., ge=0, le=1, description="Cardiovascular disease history (0/1)")
    depression_anxiety:      int = Field(..., ge=0, le=1, description="Depression or anxiety diagnosis (0/1)")

    # 社会经济
    seifa_decile: int = Field(..., ge=1, le=10,
                              description="SEIFA socioeconomic decile (1=most disadvantaged)")

    @field_validator("prev_gestational_dm")
    @classmethod
    def gestational_dm_only_female(cls, v, info):
        # 男性不会有妊娠糖尿病
        if info.data.get("sex") == SexEnum.male and v == 1:
            raise ValueError("prev_gestational_dm cannot be 1 for Male patients")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 52, "sex": "Male", "ethnicity": "Asian",
                "remoteness": "Inner Regional",
                "bmi": 28.8, "waist_cm": 94.0, "systolic_bp": 138,
                "fasting_glucose_mmol": 5.6, "hba1c_pct": 5.7,
                "cholesterol_mmol": 5.8,
                "physical_activity_days_pw": 2, "smoking_status": "Ex-smoker",
                "alcohol_risk_level": 1, "diet_quality_score": 5,
                "family_history_diabetes": 1, "prev_gestational_dm": 0,
                "hypertension": 0, "cvd_history": 0,
                "depression_anxiety": 0, "seifa_decile": 5,
            }
        }
    }


class RiskLevel(str, Enum):
    low      = "Low"
    moderate = "Moderate"
    high     = "High"


class RiskFactor(BaseModel):
    feature:   str
    shap_value: float
    direction: Literal["increases_risk", "reduces_risk"]


class PredictionResponse(BaseModel):
    """API 返回结构"""
    patient_id:         str
    risk_probability:   float = Field(..., description="Predicted T2DM probability (0–1)")
    risk_probability_pct: str = Field(..., description="Human-readable probability")
    risk_level:         RiskLevel
    recommendation:     str
    top_risk_factors:   list[RiskFactor] = Field(..., description="Top SHAP contributors")
    model_version:      str = "xgb-v1.0"
    disclaimer:         str = ("This tool supports clinical decision-making only. "
                               "Final diagnosis requires clinical assessment.")


class BatchInput(BaseModel):
    """批量预测：多个患者一次请求"""
    patients: list[PatientInput] = Field(..., min_length=1, max_length=500)
    patient_ids: list[str] | None = None
