# P2 Analysis Report — Australian Diabetes Risk Prediction Model

**Dataset:** Synthetic GP screening cohort (N=8,000) calibrated to AIHW 2023 national statistics  
**Target:** Type 2 diabetes diagnosis (binary)  
**Analyst:** Portfolio project — Health Data Analyst / Data Scientist

---

## Chart 01 — Target Variable Distribution (Class Imbalance)

![01_target_distribution](01_target_distribution.png)

### What the chart shows
The left panel shows raw patient counts: 7,581 without diabetes vs 419 with diabetes. The right pie chart confirms the class split: **94.8% negative, 5.2% positive** — an 18:1 imbalance ratio.

### Analysis
This imbalance is not a data quality issue — it **accurately reflects reality**. The AIHW 2023 Chronic Disease report estimates Type 2 diabetes prevalence at approximately 5.3% of the Australian adult population. Our synthetic cohort was specifically calibrated to this figure.

The critical implication for modelling is this: **a naive classifier that labels every patient as "no diabetes" would achieve 94.8% accuracy while being completely useless clinically.** This is why accuracy is an inappropriate metric here. Throughout this project, we use:

- **ROC-AUC** — measures the model's ability to rank high-risk patients above low-risk patients across all thresholds
- **PR-AUC (Precision-Recall AUC)** — more informative than ROC-AUC when positives are rare, because it focuses on how well the model finds the minority class

This distinction — knowing *why* to choose PR-AUC over accuracy — is a fundamental data science judgement call that separates a competent analyst from a beginner.

### Clinical relevance
In a GP clinic screening 1,000 adult patients, approximately 52 would have undiagnosed T2DM. Missing these patients (false negatives) has serious long-term consequences: delayed diagnosis leads to complications including neuropathy, retinopathy, and cardiovascular disease. The model must be tuned to **maximise recall (sensitivity)** for the positive class, accepting lower precision as a trade-off.

---

## Chart 02 — Numeric Feature Distributions by Diabetes Status

![02_numeric_distributions](02_numeric_distributions.png)

### What the chart shows
Each panel shows the probability density of a numeric feature, split by diabetes diagnosis (blue = no diabetes, red/orange = diabetes). The x-axis range is the same for both groups, making the distributional shift directly visible.

### Analysis

**Age** shows the largest and most clinically meaningful shift. The diabetic group distribution is centred around the mid-60s, while the non-diabetic group peaks in the 30s–40s. The mean difference is **18.4 years** (65.99 vs 47.58). This is consistent with AIHW data showing diabetes prevalence rises from ~1% in adults under 35 to over 20% in those over 65.

**BMI** and **waist circumference** both show right-shifted distributions in the diabetic group. BMI mean difference is +4.19 kg/m² and waist circumference +7.59 cm. Importantly, both distributions overlap substantially — many non-diabetic patients also have high BMI, which is why BMI alone is insufficient for screening. This is exactly why a multivariate model is needed.

**Fasting glucose** and **HbA1c** show modest but meaningful distributional shifts (+0.62 mmol/L and +0.33% respectively). The overlap between groups reflects real-world clinical complexity: many people with pre-diabetes or early T2DM have glucose values in the "normal" range. This explains why the AUSDRISK screening tool — which predates routine glucose testing — emphasises lifestyle and anthropometric factors.

**Systolic blood pressure** is markedly elevated in the diabetic group (+14.2 mmHg). This reflects the well-documented relationship between insulin resistance, hypertension, and metabolic syndrome.

**Physical activity** shows an inverse pattern: diabetic patients report fewer active days per week (1.59 vs 2.33). The direction is expected, though the magnitude is modest, reflecting the multifactorial nature of diabetes risk.

### Key takeaway
No single feature cleanly separates the two groups. This validates the need for a **multivariate machine learning approach** rather than simple threshold-based screening.

---

## Chart 03 — Diabetes Prevalence by Categorical Feature

![03_categorical_rates](03_categorical_rates.png)

### What the chart shows
Each panel shows the diabetes prevalence rate (%) for each category of a categorical variable. The dashed grey horizontal line represents the overall average (5.2%). Bars above the line indicate elevated risk; below indicates reduced risk.

### Analysis

**Ethnicity** reveals the most striking finding: **Indigenous Australians** have a diabetes prevalence of approximately 18–20% in this cohort — roughly **3.5× the national average**. This mirrors AIHW data showing Indigenous Australians are 3× more likely to have diabetes than non-Indigenous Australians, driven by historical, social, and structural determinants of health including food security, access to healthcare, and intergenerational trauma. Any clinical AI tool deployed in Australia must explicitly account for this disparity.

Asian Australians also show elevated prevalence (~7-8%), consistent with research showing that metabolic risk thresholds (particularly BMI) are lower for people of Asian background — a factor acknowledged in Australian clinical guidelines.

**Family history of diabetes** is the strongest binary risk factor: patients with a positive family history show roughly **3× the prevalence** of those without. This aligns with AUSDRISK scoring, where family history receives among the highest point values.

**Smoking status** follows expected clinical patterns: current smokers show the highest prevalence, ex-smokers intermediate, never-smokers the lowest. Smoking is associated with insulin resistance and impaired beta-cell function.

**Hypertension** is strongly associated with diabetes — nearly double the prevalence compared to normotensive patients — consistent with shared metabolic pathways (insulin resistance, abdominal obesity).

**Remoteness** shows a gradient: Remote > Outer Regional > Inner Regional > Major City. This reflects the interplay of socioeconomic disadvantage, reduced healthcare access, and higher proportions of Indigenous Australians in remote areas.

### Key takeaway
Categorical features encode important **social determinants of health**. Ignoring them in favour of purely clinical biomarkers would produce a less equitable model. However, including ethnicity raises fairness considerations that require ongoing monitoring (see Model Card).

---

## Chart 04 — Feature Correlation Matrix

![04_correlation_matrix](04_correlation_matrix.png)

### What the chart shows
A lower-triangular correlation heatmap of all numeric features plus the target variable. Blue = positive correlation, red = negative correlation. Cells show Pearson correlation coefficients.

### Analysis

**With the target (diabetes_diagnosis):**  
Age has the highest correlation (r = 0.229), followed by BMI (r = 0.207) and systolic BP (r = 0.204). These are modest correlations individually — reinforcing that no single feature is sufficient for prediction and that a multivariate model is warranted.

**Between features (multicollinearity):**  
BMI and waist circumference are strongly correlated (r ≈ 0.71). This is expected: both measure adiposity, just differently (overall vs central). In a logistic regression, this multicollinearity would inflate standard errors for these coefficients, making individual coefficient interpretation unreliable. However, since our logistic regression uses L2 regularisation (C=0.1), this is partially mitigated.

Age correlates positively with BMI (r ≈ 0.31), systolic BP (r ≈ 0.40), and cholesterol (r ≈ 0.33) — all physiologically expected.

Physical activity days shows a negative correlation with age (r ≈ -0.09) and BMI (r ≈ -0.14), consistent with its protective role.

**SEIFA decile** (socioeconomic advantage) shows near-zero correlation with clinical features, but small negative correlation with diabetes (-0.019). This reflects the modest socioeconomic gradient in diabetes prevalence after controlling for clinical factors.

### Key takeaway
The correlation matrix confirms two things: (1) features are individually weak predictors requiring multivariate combination, and (2) BMI and waist are the main collinear pair to monitor for coefficient stability.

---

## Chart 05 — Clinical Feature Boxplots: Diabetes vs No Diabetes

![05_clinical_boxplots](05_clinical_boxplots.png)

### What the chart shows
Side-by-side boxplots for six key clinical features, comparing diabetic (red) vs non-diabetic (blue) patients. The box spans the interquartile range (IQR: 25th–75th percentile), the line inside is the median, and whiskers extend to 1.5×IQR.

### Analysis

**Age:** The most visually striking separation. The diabetic median (~67 years) sits at the 75th percentile of the non-diabetic distribution. There is still significant overlap, but age is clearly the strongest individual discriminator — consistent with its top SHAP ranking.

**BMI:** The diabetic group has a higher median (~32 vs ~28 kg/m²) and a wider spread. The substantial overlap confirms that BMI alone cannot diagnose diabetes risk — a 32 kg/m² BMI is shared by many non-diabetic individuals.

**Waist circumference:** Similar pattern to BMI with slightly tighter distributions. The clinical threshold for increased metabolic risk (≥90 cm for men, ≥80 cm for women) is embedded in both groups' IQR ranges.

**Fasting glucose:** Modest median shift (+0.62 mmol/L). The overlap is extensive. Notably, the diabetic group contains individuals with normal fasting glucose (<5.5 mmol/L), reflecting that many early T2DM cases are asymptomatic with near-normal fasting values — exactly the patients a screening model should flag.

**HbA1c:** Similar pattern to fasting glucose. The diabetic median (~5.7%) sits near the internationally recognised pre-diabetes threshold (≥5.7%). A model incorporating HbA1c alongside other risk factors should improve sensitivity for this population.

**Systolic BP:** A clear upward shift in the diabetic group (median ~155 vs ~138 mmHg). Several diabetic patients exceed the hypertension threshold (≥140 mmHg), consistent with metabolic syndrome clustering.

### Key takeaway
Boxplots visually confirm that no single clinical measurement provides clean separation. The model's strength is in combining all six — plus lifestyle and demographic factors — to produce a composite risk score.

---

## Chart 06 — Model Comparison: ROC, Precision-Recall, Confusion Matrix

![06_model_comparison](06_model_comparison.png)

### What the chart shows
Three panels: (left) ROC curves for both models; (centre) Precision-Recall curves; (right) XGBoost confusion matrix at 0.5 threshold.

### Analysis

**ROC Curves (left panel):**  
Both models perform well above the random baseline (diagonal dashed line). Logistic Regression achieves **AUC = 0.911** and XGBoost **AUC = 0.895**. The ROC curve plots the true positive rate (sensitivity) against the false positive rate (1-specificity) across all decision thresholds.

The fact that Logistic Regression marginally outperforms XGBoost is a meaningful finding. It suggests that the relationships between risk factors and diabetes outcome in this dataset are predominantly **linear and additive** — exactly what logistic regression models well. XGBoost's ability to capture non-linear interactions provides limited additional benefit here. This is consistent with the published literature on AUSDRISK-based prediction models.

**Precision-Recall Curves (centre panel):**  
Both curves drop sharply as recall increases above ~0.7, reflecting the fundamental challenge of high-precision identification in a heavily imbalanced dataset. The area under the PR curve (PR-AUC) is **0.414** for LR and **0.377** for XGBoost. A random classifier would achieve a PR-AUC equal to the prevalence rate (0.052) — so both models vastly outperform chance.

The practical implication: at a recall of 0.80 (catching 80% of diabetic patients), precision is roughly 20-25%, meaning about 3-4 healthy patients are flagged for every true case. This is clinically acceptable for a **screening tool** (where the cost of a false negative is high) but would need refinement before use as a diagnostic tool.

**Confusion Matrix (right panel):**  
At the 0.5 threshold, XGBoost correctly classifies 1,385 of 1,516 non-diabetic patients (specificity 91%) and identifies 53 of 84 diabetic patients (recall 63%). The 53 false negatives are the patients the model misses — a key focus for clinical deployment.

---

## Chart 07 — SHAP Summary Plot (Beeswarm)

![07_shap_summary](07_shap_summary.png)

### What the chart shows
Each dot represents one patient. Position on the x-axis shows the **SHAP value** — how much that feature pushed the prediction toward (positive) or away from (negative) diabetes. Dot colour represents the feature value: red = high, blue = low. Features are ranked by mean absolute SHAP value (most important at top).

### Analysis

**Age (top feature):** Red dots (older patients) cluster on the right (increase risk), blue dots (younger) cluster on the left (decrease risk). The wide horizontal spread indicates age has a large effect size and varies substantially across patients — confirming it as the dominant predictor.

**Family history:** A distinctly bimodal pattern — two clusters separated by the zero line. Patients with a positive family history (red = value of 1) consistently show positive SHAP values; those without (blue = value of 0) show negative SHAP values. This clean separation reflects the strong, near-linear relationship between family history and outcome.

**BMI and waist circumference:** Red dots (high values) skew right, consistent with their positive risk associations. The spread is wide, indicating high patient-level variability in this feature's impact.

**Physical activity:** The pattern is **reversed** — red dots (high activity) cluster on the left (risk-reducing). This is the expected protective effect: more activity days per week is associated with lower diabetes risk. The model has correctly learned this inverse relationship.

**HbA1c and fasting glucose:** Moderate SHAP values with red (high values) increasing risk. The relatively compact spread reflects their modest individual predictive power in this dataset.

**Ethnicity (Indigenous Australian):** The SHAP values for this one-hot encoded feature are consistently positive (rightward) for patients who are Indigenous Australian, quantifying the excess risk captured in the model. This transparency is ethically important — it makes the model's handling of this disparity visible and auditable.

### Key takeaway
The beeswarm plot provides simultaneous insight into **direction, magnitude, and patient-level variability** of each feature's effect. It is the most information-dense SHAP visualisation and is particularly useful for clinical presentations.

---

## Chart 08 — SHAP Feature Importance (Bar Chart)

![08_shap_importance](08_shap_importance.png)

### What the chart shows
Mean absolute SHAP value for each feature, ranked in descending order. This provides a single-number summary of each feature's average impact on the model's predictions across all test patients.

### Analysis

The ranking closely mirrors the AUSDRISK clinical scoring system, providing strong face validity for the model:

| SHAP Rank | Feature | AUSDRISK alignment |
|-----------|---------|-------------------|
| 1 | Age | Highest-weighted AUSDRISK factor |
| 2 | Family history | Major AUSDRISK factor |
| 3 | BMI | AUSDRISK factor |
| 4 | Waist circumference | AUSDRISK factor |
| 5 | Physical activity | AUSDRISK factor |
| 6 | Systolic BP | Hypertension = AUSDRISK factor |

This correspondence is not coincidental — the synthetic data was generated using AUSDRISK-inspired coefficients. However, it serves an important purpose: it demonstrates that the model has learned clinically meaningful patterns, not spurious correlations.

**HbA1c** ranks 7th and **fasting glucose** ranks 9th, despite these being direct metabolic markers. This relatively lower ranking reflects that in this dataset, these variables were *not used* to generate the diabetes labels (to avoid label leakage), so the model has learned them as correlated predictors rather than causal factors.

**Ethnicity features** appear in the top 10, with the European and Indigenous Australian one-hot columns both present. This quantifies the model's sensitivity to ethnic background and flags the need for equity auditing.

---

## Chart 09 — SHAP Waterfall Plot (Highest-Risk Patient)

![09_shap_waterfall](09_shap_waterfall.png)

### What the chart shows
A waterfall plot for the single highest-risk patient in the test set. Starting from the **base value** (the model's average prediction across all patients, ~5.2%), each feature either increases or decreases the prediction. Red bars push the probability up; blue bars push it down. The final bar shows the predicted probability for this specific patient.

### Analysis

The base value of approximately 0.052 (5.2%) represents the population average — what the model would predict if it knew nothing about the individual patient.

For this particular patient (the highest-risk in the test set), several features compound:

- **Age** contributes the largest positive push: this patient is elderly, which alone drives the prediction substantially above baseline.
- **Family history** adds another large positive contribution: a first-degree relative with diabetes.
- **BMI/waist circumference** both contribute positively: this patient is obese with central adiposity.
- **Physical activity** contributes negatively (slight protective effect): even a small amount of activity partially offsets the other risk factors.
- **Fasting glucose** may contribute positively if elevated above normal range for this patient.

The cumulative effect of all these features pushes the final prediction to a very high probability (>95%), justifying the "High Risk" classification and the recommendation to refer for confirmatory testing.

### Clinical relevance
This visualisation is what a clinician would see in a deployed system. Rather than a black-box probability score, the waterfall plot answers the question: *"Why is this patient flagged as high risk?"* This transparency is what separates a deployable clinical AI tool from an academic model.

---

## Charts 10a, 10b, 10c — Individual Patient Risk Reports

### PT-001: Low Risk (0.04%)
![10_patient_PT-001](10_patient_PT-001_risk_report.png)

**Patient:** 28-year-old female, European, BMI 22.5, active (5 days/week), non-smoker, no family history.

This patient represents a best-case profile. The gauge needle points near zero. The SHAP bar chart shows almost all features contributing negatively (reducing risk from baseline), with only minor positive contributors. The model correctly assigns <1% probability and recommends routine review in 3 years. Clinically, no further action is warranted.

---

### PT-002: High Risk (59.5%)
![10_patient_PT-002](10_patient_PT-002_risk_report.png)

**Patient:** 52-year-old male, Asian ethnicity, BMI 28.8, waist 94 cm, ex-smoker, positive family history, elevated HbA1c (5.7%).

This case illustrates how risk factors compound. No single characteristic is extreme, yet their combination drives the prediction to 59.5%. The dominant SHAP contributors are: family history (+0.96), Asian ethnicity encoding (+0.39), and elevated HbA1c (+0.21). Age is actually a slight negative contributor here — because age 52, while not young, is substantially below the peak-risk elderly group the model has learned. The recommendation is appropriate: refer for confirmatory HbA1c/glucose testing and consider a diabetes prevention program.

**Analytical note:** This patient might be missed by simple rule-based screening (BMI is only slightly elevated, BP is normal). The multivariate model catches the compounding of family history + ethnicity + HbA1c that a clinician might underweight in a busy GP consultation.

---

### PT-003: High Risk (99.0%)
![10_patient_PT-003](10_patient_PT-003_risk_report.png)

**Patient:** 67-year-old Indigenous Australian male, BMI 34.2, waist 108 cm, BP 158 mmHg, sedentary, current smoker, positive family history, hypertension, CVD history, depression, SEIFA decile 2 (high disadvantage), Remote area.

This patient accumulates virtually every risk factor simultaneously. The SHAP chart shows the four largest positive contributors: **Indigenous Australian ethnicity** (which carries the largest single SHAP value, reflecting 3.5× population risk), waist circumference, family history, and BMI. The 99% predicted probability reflects the model having learned that this combination of biological, lifestyle, social, and demographic risk factors is almost invariably associated with diabetes in the training data.

**Equity note:** The model's high predicted risk for this patient is clinically appropriate — but it raises an important question about deployment: if the model is used to *triage* rather than *screen*, there is a risk that Indigenous patients in remote areas are flagged at high rates without corresponding access to the diabetes prevention programs they are being referred to. This is documented in the Model Card under "Fairness Considerations."

---

## Summary of Key Analytical Findings

| Finding | Evidence | Clinical Implication |
|---------|---------|---------------------|
| Age is the dominant risk predictor | SHAP rank #1, correlation 0.229 | Screening intensity should scale with age |
| Family history is the strongest binary discriminator | Clean SHAP bimodal split, rank #2 | Should always be captured at GP intake |
| LR ≥ XGBoost performance | AUC 0.911 vs 0.895 | Linear model sufficient; prefer interpretability |
| PR-AUC is the right metric | Class imbalance 18:1 | Never report accuracy alone for rare outcomes |
| Indigenous Australian excess risk is quantified | SHAP ethnicity contribution | Requires targeted prevention programs, not just flagging |
| BMI and waist are correlated (r=0.71) | Correlation matrix | Consider using only one in a parsimonious model |
| Model misses ~37% of diabetic patients at 0.5 threshold | Confusion matrix (recall 63%) | Threshold should be lowered for screening use case |

---

*This analysis was produced as part of a digital health AI portfolio targeting Australian health data scientist roles.*  
*Data source: Synthetic cohort calibrated to AIHW 2023 Chronic Disease statistics.*
