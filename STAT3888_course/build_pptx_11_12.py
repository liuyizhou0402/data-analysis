# -*- coding: utf-8 -*-
"""STAT3888 lectures 11 (logistic regression) & 12 (penalised logistic) — 60+ slide decks."""
import os
from pptx_deck import Deck, HERE
from pptx import Presentation
F = lambda name: os.path.join(HERE, "figures", name)

# ================================================================= LECTURE 11
def lecture11():
    d = Deck(11, "Logistic Regression")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Logistic Regression",
            "The workhorse classifier: modelling probabilities with the logit link, interpreting "
            "coefficients as odds, fitting by maximum likelihood, and evaluating with the ROC curve.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why not linear regression for classification?", 0),
        ("The logistic function and the logit link", 0),
        ("Odds, log-odds and coefficient interpretation", 0),
        ("Fitting by maximum likelihood", 0),
        ("The decision boundary & thresholds", 0),
        ("Evaluation: confusion matrix, ROC and AUC", 0),
    ], i())
    d.bullets("Recap", "The supervised framework", [
        ("Last lecture: fit **f: X → Y**, judge by generalisation, cross-validate", 0),
        ("Now our first named method for **classification**", 0),
        ("Y is **binary**: diseased/healthy, at-risk/not", 0),
        ("We predict a **probability**, then a class", 0),
    ], i())
    d.checkpoint("Logistic regression is used primarily for…",
        ["Predicting a continuous number", "Predicting a class / probability",
         "Clustering", "Dimension reduction"], 1, i(),
        explain="Despite its name, logistic regression is a **classification** method — it models the "
                "probability of a categorical outcome.")

    d.section("Part 1", "Why not linear regression?")
    d.big_point("The problem", "Fit a straight line to 0/1 outcomes and it predicts probabilities "
                "below 0 and above 1 — which are meaningless.",
                i(), sub="We need a model that always returns a valid probability in (0, 1).")
    d.figure("The fix", "Linear vs logistic on binary data", F("L11_linear_vs_logistic.png"), i(),
             caption="Linear regression (left) leaves the [0,1] range and extrapolates nonsense. "
                     "Logistic regression (right) produces a proper S-shaped probability.")
    d.bullets("What we need", "Requirements for a classifier", [
        ("Output a **probability** in (0, 1)", 0),
        ("Be **monotonic** in the predictors (more risk → higher probability)", 0),
        ("Keep the **interpretability** of regression coefficients", 0),
        ("Logistic regression delivers all three", 0),
    ], i())

    d.section("Part 2", "The logistic model")
    d.definition("Definition", "Logistic (sigmoid) function",
                 "The **logistic function** σ(η) = 1/(1 + e⁻η) maps any real number η into the "
                 "interval (0, 1).",
                 i(), extra=["η is the linear predictor β₀ + β₁x₁ + …",
                             "σ is S-shaped: flat, steep, flat",
                             "σ(0) = 0.5 — the natural decision threshold"])
    d.figure("The curve", "The sigmoid squashes η into a probability", F("L11_sigmoid.png"), i(),
             caption="Large positive η → probability near 1; large negative → near 0; η = 0 → 0.5.")
    d.formula("The model", "Logistic regression",
              "P(Y=1 | x) = 1 / ( 1 + e^−(β₀ + β₁x₁ + … + βₚxₚ) )",
              ["A **linear** predictor passed through the **sigmoid**",
               "Coefficients β act on the log-odds scale (next)",
               "Fitted by maximum likelihood, not least squares"],
              i())
    d.definition("Definition", "The logit link",
                 "The **logit** is the log-odds, log(p/(1−p)). Logistic regression makes the logit a "
                 "**linear** function of the predictors.",
                 i(), extra=["logit(p) = β₀ + β₁x₁ + … — linear on this scale",
                             "It's the inverse of the sigmoid",
                             "This is why logistic regression is a 'generalised linear model'"])
    d.figure("Two scales", "Probability, odds and log-odds", F("L11_odds.png"), i(),
             caption="The model is linear on the log-odds scale (left); on the odds scale a unit change "
                     "in x multiplies the odds (right).")

    d.section("Part 3", "Odds & interpreting coefficients")
    d.definition("Definition", "Odds",
                 "The **odds** of an event is p/(1−p): the probability it happens divided by the "
                 "probability it doesn't.",
                 i(), extra=["p = 0.5 → odds 1 ('even'); p = 0.8 → odds 4 ('4 to 1')",
                             "Odds range 0 to ∞; log-odds range −∞ to +∞",
                             "Coefficients are naturally read on the odds scale"])
    d.formula("Interpretation", "Coefficients are log odds-ratios",
              "e^βⱼ = odds ratio for a one-unit increase in xⱼ",
              ["A one-unit rise in xⱼ **multiplies** the odds by e^βⱼ (others held fixed)",
               "**βⱼ > 0** → e^βⱼ > 1 → the event becomes more likely",
               "**βⱼ = 0** → e^βⱼ = 1 → xⱼ has no effect on the odds"],
              i(), note="Report odds ratios with confidence intervals — the standard in health research.")
    d.bullets("Worked interpretation", "A nutrition example", [
        ("Model: P(high cholesterol) from saturated-fat intake", 0),
        ("Suppose β = 0.4 for fat (per 10 g/day)", 0),
        ("e^0.4 ≈ **1.49** → each extra 10 g/day raises the **odds** by ~49%", 0),
        ("Odds ratios, not probabilities, are what the coefficient gives you directly", 0),
    ], i())
    d.checkpoint("A predictor has coefficient β = 0 in a logistic model. Its odds ratio e^β is…",
        ["0", "1 (no effect)", "Infinite", "Negative"], 1, i(),
        explain="e^0 = 1, meaning a one-unit change multiplies the odds by 1 — i.e. no effect on the "
                "outcome's odds.")
    d.bullets("Careful interpretation", "Common traps", [
        ("Odds ratio ≠ **probability** ratio (only ≈ for rare events)", 0),
        ("Coefficients are **conditional** — 'holding other variables fixed'", 0),
        ("**Standardise** predictors to compare coefficient magnitudes", 0),
        ("Correlation among predictors makes coefficients unstable (→ Lecture 12)", 0),
    ], i())

    d.section("Part 4", "Fitting the model")
    d.definition("Definition", "Maximum likelihood estimation",
                 "**MLE** chooses the coefficients that make the observed 0/1 outcomes **most probable** "
                 "under the model.",
                 i(), extra=["No closed-form solution — solved numerically",
                             "Iteratively Reweighted Least Squares (IRLS) / Newton's method",
                             "Contrast with least squares used in linear regression"])
    d.formula("Objective", "Maximise the log-likelihood",
              "ℓ(β) = Σᵢ [ yᵢ log pᵢ + (1−yᵢ) log(1−pᵢ) ]",
              ["pᵢ = σ(β₀ + βᵀxᵢ) is the model's probability for case i",
               "Rewards high pᵢ when yᵢ = 1 and low pᵢ when yᵢ = 0",
               "Equivalent to minimising **cross-entropy / log-loss**"],
              i())
    d.bullets("How it's solved", "Under the hood (conceptually)", [
        ("Start with a guess for β", 0),
        ("Repeatedly update β to **increase** the log-likelihood", 0),
        ("Converges quickly for well-behaved data", 0),
        ("`glm(family = binomial)` does this for you in R", 0),
    ], i())
    d.bullets("Assumptions", "What logistic regression assumes", [
        ("The **logit is linear** in the predictors", 0),
        ("Observations are **independent**", 0),
        ("**Little multicollinearity** among predictors", 0),
        ("Enough events per predictor (rule of thumb: ≥ 10)", 0),
    ], i())

    d.section("Part 5", "Predictions & the decision boundary")
    d.figure("Geometry", "Where probability crosses 0.5", F("L11_boundary.png"), i(),
             caption="Logistic regression draws a **linear** decision boundary — the line where "
                     "P(Y=1) = 0.5. One side is predicted positive, the other negative.")
    d.definition("Definition", "Decision threshold",
                 "The **threshold** converts a predicted probability into a class label — default 0.5, "
                 "but adjustable to trade off error types.",
                 i(), extra=["Lower threshold → catch more positives (higher recall, more false alarms)",
                             "Higher threshold → fewer false alarms (higher precision, more misses)",
                             "Choose it from the **cost** of each error type"])
    d.bullets("Choosing a threshold", "It's a decision, not a default", [
        ("Screening for disease? **Lower** the threshold — don't miss cases (high recall)", 0),
        ("Costly intervention? **Raise** it — avoid false alarms (high precision)", 0),
        ("0.5 is a starting point, not a law", 0),
        ("The ROC curve shows all thresholds at once (next)", 0),
    ], i())
    d.checkpoint("Lowering the classification threshold from 0.5 to 0.3 will generally…",
        ["Increase recall, increase false positives", "Increase precision, reduce recall",
         "Have no effect", "Reduce both errors"], 0, i(),
        explain="A lower threshold labels more cases positive, catching more true positives (higher "
                "recall) but also producing more false positives.")

    d.section("Part 6", "Evaluation")
    d.figure("The ROC curve", "Performance across all thresholds", F("L11_roc.png"), i(),
             caption="The ROC curve plots true-positive vs false-positive rate as the threshold varies. "
                     "The area under it (AUC) summarises ranking quality.")
    d.definition("Definition", "AUC",
                 "The **area under the ROC curve** is the probability the model ranks a random positive "
                 "above a random negative.",
                 i(), extra=["AUC = 0.5 → no better than chance; 1.0 → perfect",
                             "Threshold-free — measures ranking, not a single cutoff",
                             "Robust to class imbalance"])
    d.bullets("Evaluating a classifier", "The full picture", [
        ("**Confusion matrix** — the raw counts at a chosen threshold", 0),
        ("**Precision / recall / F1** — especially under imbalance", 0),
        ("**ROC / AUC** — threshold-free ranking quality", 0),
        ("**Calibration** — do predicted probabilities match observed rates?", 0),
    ], i())
    d.code("In R", "Fit and evaluate a logistic model", [
        "fit <- glm(highchol ~ sat_fat + fibre + age,",
        "           data = training, family = binomial)",
        "summary(fit)                       # coefficients (log-odds)",
        "exp(coef(fit))                     # odds ratios",
        "",
        "prob <- predict(fit, test, type = 'response')",
        "pred <- ifelse(prob > 0.5, 1, 0)",
        "library(pROC); roc(test$highchol, prob)$auc   # AUC",
    ], i())
    d.big_point("Why it endures", "Logistic regression is fast, interpretable and calibrated — often "
                "the first classifier to try and the baseline to beat.",
                i(), sub="Its coefficients tell a story a clinician can act on — a rare and valuable "
                         "property.")
    d.exercise("Interpret a model", [
        "A logistic model gives β = 0.7 for a binary 'processed-food' predictor of obesity.",
        "Compute and interpret the odds ratio.",
        "The model's AUC is 0.82 — what does that mean in plain words?",
        "For a public-health screening tool, would you raise or lower the 0.5 threshold, and why?",
    ], i(), hint="e^0.7 ≈ 2.01 → roughly double the odds; AUC 0.82 = 82% chance a random obese person "
                 "is ranked above a random non-obese one; screening favours higher recall (lower threshold).")
    d.summary([
        "Logistic regression models **P(Y=1)** via the sigmoid of a linear predictor.",
        "It is linear on the **log-odds** scale; e^β is an **odds ratio**.",
        "Fit by **maximum likelihood**; the decision boundary is **linear**.",
        "Evaluate with the **confusion matrix, precision/recall and ROC/AUC**.",
    ], i(), nextup="Lecture 12 — Penalised logistic regression: ridge, lasso and elastic net.")
    # top-up section to reach 60+
    d.section("Part 7", "Extensions, diagnostics & consolidation")
    d.definition("Definition", "Generalised linear model (GLM)",
                 "A **GLM** links a linear predictor to a response distribution via a link function; "
                 "logistic regression is the GLM for binary data.",
                 i(), extra=["Link: logit; distribution: Bernoulli/binomial",
                             "Poisson regression (counts) is another GLM",
                             "One unifying framework, many response types"])
    d.bullets("Multiclass", "Beyond two classes", [
        ("**Multinomial logistic regression** handles >2 unordered classes", 0),
        ("**Ordinal logistic regression** for ordered categories (e.g. BMI band)", 0),
        ("**One-vs-rest** fits a binary model per class", 0),
        ("The same logit machinery, generalised", 0),
    ], i())
    d.bullets("Diagnostics", "Checking a fitted model", [
        ("**Residual / deviance** checks for lack of fit", 0),
        ("**Influence** measures for outlying observations", 0),
        ("**Multicollinearity** via the variance inflation factor (VIF)", 0),
        ("**Calibration plot** — predicted vs observed probabilities", 0),
    ], i())
    d.definition("Definition", "Separation",
                 "**Perfect separation** occurs when a predictor perfectly splits the classes; MLE "
                 "estimates then diverge to ±∞.",
                 i(), extra=["Symptom: huge coefficients and standard errors",
                             "Common with small samples or strong predictors",
                             "Remedy: penalisation (Lecture 12!) or Firth's correction"])
    d.two_col("Strengths & limits", "Logistic regression in balance",
              left_head="Strengths",
              left=["Interpretable odds ratios",
                    "Fast, well-calibrated",
                    "Probabilistic output",
                    "Strong baseline"],
              right_head="Limits",
              right=["Only **linear** boundaries",
                     "Struggles with many correlated predictors",
                     "Sensitive to separation",
                     "Needs feature engineering for non-linearity"],
              idx=i())
    d.bullets("Making it non-linear", "Extending the reach", [
        ("Add **polynomial** or **spline** terms of predictors", 0),
        ("Add **interaction** terms (effect of one depends on another)", 0),
        ("Still a linear model **in the transformed features**", 0),
        ("Or switch to trees / SVMs / neural nets (later lectures)", 0),
    ], i())
    d.checkpoint("Your logistic fit returns a coefficient of 40 with a standard error of 9000. Likely cause?",
        ["Great fit", "Perfect (or quasi-) separation", "Too little regularisation of the mean",
         "Wrong link function"], 1, i(),
        explain="Enormous coefficients with huge standard errors are the classic signature of "
                "separation — a predictor splits the classes too cleanly for plain MLE.")
    d.bullets("Case study", "Predicting metabolic risk", [
        ("Fit logistic model of metabolic-syndrome on intake + anthropometrics", 0),
        ("Report **odds ratios** with 95% CIs for each predictor", 0),
        ("Assess discrimination via **AUC** on a held-out set", 0),
        ("Check **calibration**; choose a threshold from clinical costs", 0),
    ], i())
    d.exercise("Plan a classification analysis", [
        "You must classify participants as insulin-resistant or not from 20 predictors.",
        "Write the workflow: split → recipe → glm → threshold → evaluate.",
        "Which metric leads your report, and why (classes are imbalanced)?",
        "How would you detect and handle separation if it arises?",
    ], i(), hint="Lead with AUC / recall under imbalance; handle separation with penalisation (next "
                 "lecture) or Firth's method.")
    d.bullets("Key ideas recap", "Hold onto these", [
        ("Sigmoid + linear predictor = valid probability", 0),
        ("**e^β = odds ratio**; linear on the log-odds scale", 0),
        ("Fit by **maximum likelihood**; boundary is linear", 0),
        ("Evaluate with **ROC/AUC** and the confusion matrix", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *ISLR*, §4.3 (logistic regression)", 0),
        ("Hastie et al., *ESL*, §4.4", 0),
        ("Harrell, *Regression Modeling Strategies* — clinical practice", 0),
    ], i())
    d.big_point("The takeaway", "When you need a fast, interpretable, probabilistic classifier, "
                "logistic regression is almost always the right first move.",
                i(), sub="Next: how to make it robust when predictors are many and correlated.")

    d.section("Part 8", "Probabilities, inference & context")
    d.definition("Definition", "Calibration",
                 "A classifier is **well-calibrated** if, among cases it gives probability p, about a "
                 "fraction p are truly positive.",
                 i(), extra=["Logistic regression is usually well-calibrated by construction",
                             "Check with a calibration (reliability) plot",
                             "Matters when the **probability itself** is used for decisions"])
    d.bullets("Statistical inference", "Beyond prediction", [
        ("Each coefficient has a **standard error**, z-test and p-value", 0),
        ("Report **odds ratios with 95% confidence intervals**", 0),
        ("The **Wald** and **likelihood-ratio** tests assess predictors", 0),
        ("**Deviance** compares nested models", 0),
    ], i())
    d.formula("Confidence intervals", "On the odds-ratio scale",
              "95% CI for OR = exp( β̂ ± 1.96 · SE(β̂) )",
              ["Compute the interval on the **log-odds** scale, then exponentiate",
               "If the CI for the OR excludes **1**, the effect is significant",
               "The standard way clinical results are reported"],
              i())
    d.bullets("Sample-size rules", "Enough data to trust the fit", [
        ("Rule of thumb: **≥ 10 events per predictor** (EPV)", 0),
        ("Too few events → unstable, over-optimistic coefficients", 0),
        ("Rare outcomes need **large** samples or penalisation", 0),
        ("Report EPV so readers can judge reliability", 0),
    ], i())
    d.two_col("Logistic vs the alternatives", "Placing it among classifiers",
              left_head="Logistic regression",
              left=["Linear boundary",
                    "Interpretable, calibrated",
                    "Great baseline"],
              right_head="Coming up",
              right=["**LDA/QDA** — generative, Gaussian (L13)",
                     "**Trees/forests** — non-linear (L15–16)",
                     "**SVM** — margins & kernels (L19–20)"],
              idx=i())
    d.checkpoint("To report a nutrition finding to clinicians, which output of a logistic model is most useful?",
        ["The raw log-odds", "Odds ratios with confidence intervals",
         "The number of iterations", "The training accuracy"], 1, i(),
        explain="Clinicians interpret odds ratios (with CIs) directly — they quantify how a predictor "
                "changes the odds of the outcome.")
    d.bullets("Chapter checklist", "You should be able to…", [
        ("Explain why linear regression fails for classification", 0),
        ("Interpret a coefficient as an **odds ratio**", 0),
        ("Describe MLE fitting and the linear boundary", 0),
        ("Evaluate with ROC/AUC and pick a threshold from costs", 0),
    ], i())
    d.big_point("Bridge to next lecture", "Plain logistic regression falters when predictors are many "
                "and correlated — so we penalise it.",
                i(), sub="Ridge, lasso and elastic net make it robust and even self-selecting.")
    out=os.path.join(HERE,"Lecture11_LogisticRegression.pptx"); d.save(out); return out


# ================================================================= LECTURE 12
def lecture12():
    d = Deck(12, "Penalised Logistic Regression")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Penalised Logistic Regression: Ridge, Lasso & Elastic Net",
            "Taming many correlated predictors by shrinking coefficients — controlling variance, doing "
            "automatic variable selection, and tuning the penalty by cross-validation.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why plain logistic regression struggles with many predictors", 0),
        ("Regularisation: the shrinkage idea", 0),
        ("Ridge (L2), lasso (L1) and elastic net", 0),
        ("The geometry: why lasso selects variables", 0),
        ("Choosing the penalty λ by cross-validation", 0),
        ("Practice in R with glmnet", 0),
    ], i())
    d.bullets("Recap", "Where plain logistic regression hurts", [
        ("Last lecture: logistic regression via maximum likelihood", 0),
        ("With **many** predictors (p large) it **overfits**", 0),
        ("With **correlated** predictors, coefficients become **unstable**", 0),
        ("**Separation** sends estimates to infinity", 0),
        ("Penalisation fixes all three", 0),
    ], i())
    d.checkpoint("Nutrition data often has many correlated intake variables. For logistic regression this causes…",
        ["Faster fitting", "Unstable, high-variance coefficients (overfitting)",
         "Guaranteed separation", "Lower AUC always"], 1, i(),
        explain="Many correlated predictors inflate coefficient variance and overfit — exactly what "
                "regularisation is designed to control.")

    d.section("Part 1", "The problem & the idea")
    d.big_point("The core idea", "Deliberately **shrink** the coefficients toward zero — accept a "
                "little bias in exchange for a large drop in variance.",
                i(), sub="A slightly biased but stable model generalises far better than an unbiased, "
                         "wildly variable one.")
    d.definition("Definition", "Regularisation",
                 "**Regularisation** adds a penalty on coefficient size to the loss, discouraging "
                 "over-large coefficients and thus overfitting.",
                 i(), extra=["Fit = minimise (−log-likelihood + λ · penalty)",
                             "**λ** controls the strength of shrinkage",
                             "λ = 0 recovers ordinary logistic regression"])
    d.figure("Why it helps", "Regularisation and the bias–variance trade-off", F("L12_bias_var_lambda.png"), i(),
             caption="As the penalty λ grows, variance falls and bias rises. Test error is minimised at "
                     "an intermediate λ — found by cross-validation.")
    d.formula("Penalised objective", "Loss plus penalty",
              "minimise   −ℓ(β)  +  λ · penalty(β)",
              ["**−ℓ(β)** — the usual logistic loss (fit to data)",
               "**penalty(β)** — grows with coefficient size",
               "**λ** — the dial: 0 = no penalty, large = heavy shrinkage"],
              i())

    d.section("Part 2", "Ridge, lasso & elastic net")
    d.definition("Definition", "Ridge (L2) penalty",
                 "**Ridge** penalises the **sum of squared** coefficients (Σβ²), shrinking them "
                 "smoothly toward — but never exactly to — zero.",
                 i(), extra=["Handles correlated predictors gracefully",
                             "Keeps **all** variables in the model",
                             "Great when many small effects matter"])
    d.definition("Definition", "Lasso (L1) penalty",
                 "**Lasso** penalises the **sum of absolute** coefficients (Σ|β|), shrinking some "
                 "**exactly to zero** — doing automatic variable selection.",
                 i(), extra=["Produces **sparse**, interpretable models",
                             "Picks a subset of predictors",
                             "Can struggle among highly correlated variables (picks one)"])
    d.figure("Shrinkage paths", "Lasso zeros coefficients; ridge doesn't", F("L12_paths.png"), i(),
             caption="As λ increases (left→right), lasso coefficients hit exactly zero one by one; "
                     "ridge coefficients shrink smoothly but stay non-zero.")
    d.figure("The geometry", "Why lasso selects variables", F("L12_l1_l2_geometry.png"), i(),
             caption="The lasso's diamond constraint has corners on the axes, so the solution often "
                     "lands where a coefficient is exactly zero. The ridge circle has no corners.")
    d.definition("Definition", "Elastic net",
                 "The **elastic net** combines L1 and L2 penalties, getting lasso's sparsity **and** "
                 "ridge's stability with correlated predictors.",
                 i(), extra=["Mixing parameter α: α=1 lasso, α=0 ridge, in-between = elastic net",
                             "Often the best default for wide, correlated data",
                             "Selects **groups** of correlated predictors together"])
    d.table("Compare", "The three penalties",
            ["Penalty", "Shrinks", "Selects variables?", "Correlated X"],
            [["Ridge (L2)", "smoothly", "no (keeps all)", "handles well"],
             ["Lasso (L1)", "to zero", "yes (sparse)", "picks one"],
             ["Elastic net", "both", "yes", "groups them"]],
            i(), col_widths=[2.4,2.2,3.2,3.7])
    d.checkpoint("You want an interpretable model that automatically drops irrelevant predictors. Choose…",
        ["Ridge", "Lasso", "Plain logistic", "PCA"], 1, i(),
        explain="Lasso's L1 penalty sets some coefficients exactly to zero, performing automatic "
                "variable selection for a sparse, interpretable model.")

    d.section("Part 3", "Choosing the penalty λ")
    d.big_point("λ is a hyperparameter", "It is not learned from the fit — it is **tuned** by "
                "cross-validation to minimise prediction error.",
                i(), sub="Too small → overfit; too large → underfit. CV finds the sweet spot.")
    d.figure("Tuning", "Cross-validation over λ", F("L12_cv_lambda.png"), i(),
             caption="Compute CV error across a grid of λ; pick the λ that minimises it (or the "
                     "'one-standard-error' λ for a simpler model).")
    d.bullets("Two common choices", "lambda.min vs lambda.1se", [
        ("**λ_min** — the value giving the lowest CV error", 0),
        ("**λ_1se** — the largest λ within one SE of the minimum → **simpler** model", 0),
        ("λ_1se trades a touch of accuracy for **parsimony** and robustness", 0),
        ("`cv.glmnet` reports both automatically", 0),
    ], i())
    d.bullets("Don't forget", "Practical must-dos", [
        ("**Standardise** predictors — penalties are scale-sensitive (glmnet does this by default)", 0),
        ("Tune λ **inside** cross-validation to avoid leakage", 0),
        ("Report which variables **survive** (for lasso/elastic net)", 0),
        ("Refit / interpret on the chosen λ", 0),
    ], i())

    d.section("Part 4", "In practice with glmnet")
    d.code("Fitting", "Penalised logistic regression in R", [
        "library(glmnet)",
        "X <- model.matrix(~ . - 1, data = predictors)   # numeric matrix",
        "y <- outcome",
        "",
        "# alpha = 1 lasso, 0 ridge, 0.5 elastic net; family = binomial",
        "cvfit <- cv.glmnet(X, y, family = 'binomial', alpha = 1)",
        "plot(cvfit)                       # CV error vs log(lambda)",
        "coef(cvfit, s = 'lambda.1se')     # selected coefficients",
    ], i())
    d.code("Predicting", "Use the tuned model", [
        "prob <- predict(cvfit, newx = Xtest, s = 'lambda.min', type = 'response')",
        "pred <- ifelse(prob > 0.5, 1, 0)",
        "",
        "# which predictors survived?",
        "sel <- coef(cvfit, s = 'lambda.1se')",
        "sel[sel[,1] != 0, ]",
    ], i())
    d.bullets("Interpreting a penalised model", "Read with care", [
        ("Coefficients are **shrunk** — smaller than unpenalised ones", 0),
        ("Lasso **zeros** mean 'not selected', not 'no association'", 0),
        ("Among correlated predictors, lasso's **choice** can be arbitrary", 0),
        ("For inference/odds ratios, be cautious — penalisation biases estimates", 0),
    ], i())

    d.section("Part 5", "Consolidation, pitfalls & wrap-up")
    d.two_col("Strengths & limits", "Penalised regression in balance",
              left_head="Strengths",
              left=["Controls **overfitting** with many predictors",
                    "Lasso gives **variable selection**",
                    "Stabilises **correlated** predictors (ridge/EN)",
                    "Handles p > n"],
              right_head="Limits",
              right=["λ must be **tuned**",
                     "Shrunk coefficients **biased** for inference",
                     "Lasso arbitrary among correlated X",
                     "Still a **linear** boundary"],
              idx=i())
    d.definition("Definition", "Bias–variance, revisited",
                 "Penalisation deliberately **adds bias** (shrinkage) to **cut variance**, lowering "
                 "total expected error.",
                 i(), extra=["Unpenalised MLE: low bias, high variance (with many predictors)",
                             "Penalised: a little bias, much less variance",
                             "The whole point is a lower **test** error"])
    d.bullets("When to use what", "A quick guide", [
        ("Many predictors, want **selection** → **lasso**", 0),
        ("Many correlated predictors, keep all → **ridge**", 0),
        ("Wide, correlated, want selection **and** stability → **elastic net**", 0),
        ("Few, well-chosen predictors → **plain** logistic may suffice", 0),
    ], i())
    d.definition("Definition", "p ≫ n problem",
                 "When predictors outnumber observations, ordinary regression has no unique solution — "
                 "penalisation makes it well-posed.",
                 i(), extra=["Common in genomics / metabolomics (thousands of features)",
                             "Ridge/lasso/elastic net give a unique, stable fit",
                             "A key reason these methods dominate high-dim biology"])
    d.checkpoint("glmnet standardises predictors by default because…",
        ["It's faster", "The penalty is scale-sensitive, so variables must be comparable",
         "It removes outliers", "It selects lambda"], 1, i(),
        explain="L1/L2 penalties act on coefficient magnitudes, which depend on predictor scale — "
                "standardising ensures each variable is penalised fairly.")
    d.big_point("Also fixes separation", "Because it forbids infinite coefficients, penalisation "
                "cleanly solves the separation problem that breaks plain logistic regression.",
                i(), sub="Another reason it's often the safer default in practice.")
    d.exercise("Build a penalised classifier", [
        "You have 60 correlated intake/metabolite predictors and 200 participants.",
        "Would you choose ridge, lasso or elastic net? Justify.",
        "Write the cv.glmnet call and say how you'd pick λ.",
        "How will you report which predictors matter, and with what caveat?",
    ], i(), hint="Correlated + want selection → elastic net; tune λ by cv.glmnet; report survivors at "
                 "lambda.1se, noting penalisation biases coefficient sizes.")
    d.exercise("Reason about geometry", [
        "Explain, using the constraint-region picture, why lasso produces exact zeros but ridge does not.",
        "What happens to two identical (perfectly correlated) predictors under lasso? Under ridge?",
        "Which penalty would you trust more for that correlated pair, and why?",
    ], i(), hint="The L1 diamond's corners lie on the axes (zeros); the L2 circle is smooth. Lasso picks "
                 "one of the correlated pair; ridge splits the weight between them.")
    d.bullets("Key ideas recap", "Hold onto these", [
        ("Penalise coefficient size to **trade bias for lower variance**", 0),
        ("**Ridge** shrinks smoothly; **lasso** selects; **elastic net** does both", 0),
        ("Tune **λ by cross-validation**; standardise predictors", 0),
        ("Essential for **many / correlated** predictors and **p ≫ n**", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *ISLR*, §6.2 (shrinkage methods)", 0),
        ("Hastie et al., *ESL*, §3.4 & Ch. 18 (high-dimensional)", 0),
        ("Hastie, Tibshirani & Wainwright, *Statistical Learning with Sparsity*", 0),
    ], i())

    d.section("Part 6", "Deeper into the mechanics")
    d.formula("Ridge objective", "L2-penalised logistic loss",
              "minimise  −ℓ(β)  +  λ Σⱼ βⱼ²",
              ["The penalty grows with the **square** of each coefficient",
               "Large coefficients are punished heavily → smooth shrinkage",
               "Never forces a coefficient exactly to zero"],
              i())
    d.formula("Lasso objective", "L1-penalised logistic loss",
              "minimise  −ℓ(β)  +  λ Σⱼ |βⱼ|",
              ["The penalty grows with the **absolute value** of each coefficient",
               "Its non-smooth corners at zero create **sparsity**",
               "Some coefficients become exactly zero → selection"],
              i())
    d.formula("Elastic net objective", "A weighted blend",
              "penalty = λ [ α Σ|βⱼ| + (1−α) Σβⱼ² ]",
              ["**α = 1** → pure lasso; **α = 0** → pure ridge",
               "Intermediate α blends selection and stability",
               "α is a second hyperparameter (often fixed, e.g. 0.5)"],
              i())
    d.definition("Definition", "Shrinkage",
                 "**Shrinkage** pulls coefficient estimates toward zero, reducing their variance at the "
                 "cost of a small bias.",
                 i(), extra=["The bias is usually far smaller than the variance saved",
                             "Predictions become more stable across samples",
                             "The essence of every penalised method"])
    d.bullets("Why sparsity matters", "The appeal of lasso", [
        ("Fewer variables → **simpler, cheaper** models", 0),
        ("Easier to **explain** to domain partners", 0),
        ("Highlights the **key drivers** of the outcome", 0),
        ("Reduces the cost of collecting many measurements in future", 0),
    ], i())
    d.checkpoint("Increasing λ toward infinity drives the coefficients toward…",
        ["Infinity", "The unpenalised MLE", "Zero (an intercept-only model)", "Random values"], 2, i(),
        explain="A very large penalty forces all coefficients toward zero, leaving essentially an "
                "intercept-only (null) model — maximum bias, minimum variance.")
    d.bullets("Grouped & structured penalties", "Beyond the basics", [
        ("**Group lasso** — select whole groups of related predictors together", 0),
        ("**Adaptive lasso** — different penalties per coefficient for better selection", 0),
        ("**Relaxed lasso** — refit selected variables without shrinkage", 0),
        ("A rich toolbox built on the same idea", 0),
    ], i())

    d.section("Part 7", "Workflow, case study & wrap-up")
    d.steps("End-to-end", "A penalised-regression workflow", [
        ("Split & standardise", "train/test split; scale predictors"),
        ("Build X, y", "design matrix and binary outcome"),
        ("cv.glmnet", "cross-validate over λ (and maybe α)"),
        ("Select λ", "lambda.min or lambda.1se"),
        ("Evaluate & report", "test AUC; list selected predictors"),
    ], i())
    d.big_point("Case study", "60 metabolomic predictors, 180 participants: elastic net selects 12 "
                "and achieves test AUC 0.86.",
                i(), sub="From an unfittable p-heavy problem to a compact, accurate, interpretable model.")
    d.table("Case study detail", "What the elastic net delivered",
            ["Aspect", "Plain logistic", "Elastic net"],
            [["Fits at all (p vs n)?", "unstable", "stable"],
             ["# predictors used", "60", "12"],
             ["Test AUC", "0.71 (overfit)", "0.86"],
             ["Interpretable?", "hard", "yes (12 drivers)"]],
            i(), col_widths=[3.6,3.9,4.0])
    d.bullets("Reporting", "A good penalised-model write-up", [
        ("State the **penalty type** (ridge/lasso/EN) and **α**", 0),
        ("Show the **CV curve** and the chosen **λ**", 0),
        ("List the **selected predictors** (and note selection instability)", 0),
        ("Report **test** performance, not training", 0),
    ], i())
    d.two_col("Common mistakes", "Avoid these",
              left_head="Don't",
              left=["Forget to standardise",
                    "Tune λ on the test set",
                    "Over-interpret shrunk coefficients",
                    "Assume lasso's choice is 'the' truth"],
              right_head="Do",
              right=["Let glmnet standardise",
                     "Tune λ inside CV",
                     "Report odds ratios cautiously",
                     "Check selection stability"],
              idx=i())
    d.definition("Definition", "Selection stability",
                 "**Selection stability** asks whether the same variables are chosen under resampling; "
                 "unstable selection warns against over-reading which variables 'matter'.",
                 i(), extra=["Assess by refitting on bootstrap samples",
                             "Report how often each predictor is selected",
                             "Especially important with correlated predictors"])
    d.checkpoint("Two predictors are almost perfectly correlated. Under lasso, you should expect…",
        ["Both kept with equal weight", "One kept (somewhat arbitrarily), the other zeroed",
         "Both zeroed", "The model to fail"], 1, i(),
        explain="Lasso tends to pick one variable from a correlated group and zero the rest — the "
                "choice can be arbitrary, which is why elastic net is often preferred there.")
    d.exercise("Compare ridge, lasso, elastic net", [
        "On the same wide, correlated dataset, fit ridge, lasso and elastic net with cv.glmnet.",
        "Compare test AUC and the number of predictors each retains.",
        "Which gives the best accuracy–parsimony trade-off?",
        "How stable is lasso's variable selection across bootstrap samples?",
    ], i(), hint="Vary alpha = 0, 0.5, 1; compare collect_metrics()/AUC and count non-zero coefficients "
                 "at lambda.1se; bootstrap to check stability.")
    d.bullets("Connections", "How this ties the unit together", [
        ("Regularisation is the **bias–variance** trade-off made actionable (Lecture 10)", 0),
        ("It fixes logistic regression's **separation** problem (Lecture 11)", 0),
        ("The same idea regularises **neural networks** (weight decay, Lecture 18)", 0),
        ("A unifying theme across modern machine learning", 0),
    ], i())
    d.big_point("The big lesson", "Sometimes the best model is not the one that fits the training data "
                "best — it's the one you deliberately hold back.",
                i(), sub="Controlled humility (shrinkage) beats unchecked flexibility.")
    d.bullets("Chapter checklist", "You should be able to…", [
        ("Explain why penalisation controls overfitting (bias–variance)", 0),
        ("Contrast ridge, lasso and elastic net", 0),
        ("Explain geometrically why lasso gives sparsity", 0),
        ("Tune λ by cross-validation with glmnet", 0),
    ], i())
    d.definition("Definition", "Degrees of freedom (effective)",
                 "Penalisation reduces a model's **effective degrees of freedom** — its effective "
                 "complexity — below the raw number of predictors.",
                 i(), extra=["More shrinkage → fewer effective degrees of freedom",
                             "Explains why penalised models resist overfitting",
                             "Links penalty strength directly to model complexity"])
    d.bullets("One line to remember", "Carry this out the door", [
        ("**Shrink to stabilise; use L1 to select; tune λ by CV; standardise.**", 0),
    ], i())
    d.summary([
        "Penalised logistic regression **shrinks** coefficients to control variance and overfitting.",
        "**Ridge** keeps all variables; **lasso** selects a sparse subset; **elastic net** blends both.",
        "The penalty **λ** is tuned by **cross-validation**; always standardise predictors.",
        "It's the go-to for **many, correlated** predictors, p ≫ n, and separation.",
    ], i(), nextup="Lecture 13 — Discriminant analysis: LDA and QDA.")
    out=os.path.join(HERE,"Lecture12_PenalisedLogistic.pptx"); d.save(out); return out


if __name__ == "__main__":
    for f in (lecture11, lecture12):
        p=f(); print(f"{os.path.basename(p)}  —  {len(Presentation(p).slides._sldIdLst)} slides")
