# -*- coding: utf-8 -*-
"""STAT3888 lectures 07 (PCA background) & 08 (PCA) — full 60+ slide decks."""
import os
from pptx_deck import Deck, HERE
from pptx import Presentation
F = lambda name: os.path.join(HERE, "figures", name)

# ================================================================= LECTURE 07
def lecture07():
    d = Deck(7, "PCA Background")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Principal Component Analysis: The Background",
            "The linear-algebra foundations — variance, covariance, projections, eigenvectors — that "
            "make PCA work. Build the intuition before the method.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why dimension reduction? The curse of dimensionality", 0),
        ("Variance: measuring spread", 0),
        ("Covariance and the covariance matrix", 0),
        ("Vectors, projections and linear combinations", 0),
        ("Eigenvectors and eigenvalues", 0),
        ("Putting it together: the geometry of PCA", 0),
    ], i())
    d.bullets("Recap", "From clustering to structure", [
        ("Weeks 1–2: we **grouped** observations (clustering)", 0),
        ("Now we shift to **summarising variables** — dimension reduction", 0),
        ("Nutrition data is **wide**: dozens of correlated intake & metabolite variables", 0),
        ("PCA compresses them into a few informative directions", 0),
    ], i())

    d.section("Part 1", "Why reduce dimensions?")
    d.definition("Definition", "Dimension reduction",
                 "**Dimension reduction** replaces many (correlated) variables with a few new variables "
                 "that retain most of the information.",
                 i(), extra=["Fewer variables → easier to visualise, store and model",
                             "Removes redundancy among correlated measurements",
                             "Can reduce noise and improve downstream models"])
    d.bullets("The curse", "Why high dimensions hurt", [
        ("**Distances lose meaning** — everything becomes far apart and roughly equidistant", 0),
        ("Models need **exponentially more data** as dimensions grow", 0),
        ("**Overfitting** becomes easy; visualisation becomes impossible beyond 3-D", 0),
        ("Many variables are **redundant** — they move together", 0),
    ], i())
    d.big_point("The opportunity", "If variables are correlated, the data doesn't really fill all "
                "those dimensions — it lives near a lower-dimensional surface.",
                i(), sub="PCA finds that surface: the few directions along which the data actually varies.")
    d.two_col("Two goals", "What dimension reduction is for",
              left_head="Visualisation",
              left=["Squeeze many variables into 2–3 axes",
                    "Plot participants and spot patterns",
                    "Communicate structure to non-experts"],
              right_head="Preprocessing",
              right=["Feed fewer, cleaner inputs to models",
                     "Reduce collinearity and noise",
                     "Speed up and stabilise learning"],
              idx=i())

    d.section("Part 2", "Variance: measuring spread")
    d.definition("Definition", "Variance",
                 "The **variance** of a variable is the average squared distance of its values from "
                 "their mean — a measure of spread.",
                 i(), extra=["Larger variance = data more spread out along that variable",
                             "PCA treats variance as **information** worth keeping",
                             "Zero variance = a constant, carrying no information"])
    d.formula("Formula", "Sample variance",
              "s² = (1/(n−1)) Σᵢ ( xᵢ − x̄ )²",
              ["Subtract the mean, square, average (with n−1 for an unbiased estimate)",
               "Units are squared; the **standard deviation** s is on the original scale",
               "PCA seeks new axes that **maximise** this quantity"],
              i())
    d.figure("Intuition", "Variance is spread", F("L07_variance.png"), i(),
             caption="Both clouds share the same centre, but the right has far more variance. PCA cares "
                     "about directions where variance is large.")
    d.bullets("Why variance = information", "The PCA worldview", [
        ("A direction with **high variance** separates observations — it's informative", 0),
        ("A direction with **near-zero variance** looks the same for everyone — drop it", 0),
        ("PCA ranks directions by variance and keeps the top few", 0),
    ], i())

    d.section("Part 3", "Covariance")
    d.definition("Definition", "Covariance",
                 "The **covariance** of two variables measures how they vary **together**: positive "
                 "if they rise together, negative if one falls as the other rises.",
                 i(), extra=["Cov > 0: move in the same direction (e.g. energy & fat)",
                             "Cov < 0: move oppositely",
                             "Cov ≈ 0: no linear relationship"])
    d.formula("Formula", "Sample covariance",
              "cov(x,y) = (1/(n−1)) Σᵢ (xᵢ−x̄)(yᵢ−ȳ)",
              ["Positive when both variables are above (or both below) their means together",
               "Symmetric: cov(x,y) = cov(y,x)",
               "cov(x,x) is just the variance of x"],
              i())
    d.figure("Three cases", "Covariance encodes co-movement", F("L07_covariance.png"), i(),
             caption="Negative, near-zero, and positive covariance. PCA works from exactly this "
                     "structure across all variable pairs.")
    d.definition("Definition", "Covariance matrix",
                 "The **covariance matrix** Σ collects the variance of every variable (diagonal) and "
                 "the covariance of every pair (off-diagonal).",
                 i(), extra=["For p variables it is p×p and symmetric",
                             "Diagonal = variances; off-diagonal = covariances",
                             "This single matrix is the raw material for PCA"])
    d.formula("Structure", "The p×p covariance matrix",
              "Σ = [ var(x₁)   cov(x₁,x₂) … ; cov(x₂,x₁)  var(x₂) … ;  ⋮ ]",
              ["Symmetric and (usually) positive semi-definite",
               "Captures the whole **linear** dependence structure of the data",
               "PCA = an eigen-decomposition of this matrix"],
              i())
    d.bullets("Correlation", "Covariance's scaled cousin", [
        ("**Correlation** = covariance divided by the two standard deviations", 0),
        ("Always between −1 and +1 — scale-free and interpretable", 0),
        ("Running PCA on the **correlation** matrix = PCA on **standardised** data", 0),
        ("Almost always what you want when variables have different units", 0),
    ], i())
    d.checkpoint("Energy (kJ) and fat (g) tend to rise together. Their covariance is…",
        ["Negative", "Zero", "Positive", "Undefined"], 2, i(),
        explain="Variables that increase together have positive covariance.")

    d.section("Part 4", "Vectors & projections")
    d.bullets("Vectors", "Data points as vectors", [
        ("Each observation with p variables is a **point / vector** in p-dimensional space", 0),
        ("A **direction** is a unit vector v (length 1) pointing some way through that space", 0),
        ("PCA is a hunt for the most **informative directions**", 0),
    ], i())
    d.definition("Definition", "Projection",
                 "The **projection** of a point onto a direction v is its 'shadow' on that line — how "
                 "far along v the point sits, given by the dot product xᵀv.",
                 i(), extra=["Projecting reduces a p-dim point to a single number (its coordinate on v)",
                             "The set of all projections is a new 1-D variable",
                             "PCA chooses v so this new variable has **maximum variance**"])
    d.figure("Geometry", "Projecting data onto a direction", F("L07_projection.png"), i(),
             caption="Grey lines drop each point onto the line. PCA picks the line (red) for which the "
                     "projected points (teal) are as spread out as possible.")
    d.formula("The optimisation", "PC1 maximises projected variance",
              "PC1 = argmaxᵥ  Var( X v )   subject to ‖v‖ = 1",
              ["Among all unit directions, find the one with the most spread after projection",
               "That direction is the **first principal component**",
               "The next PC does the same, but must be **orthogonal** to the first"],
              i())
    d.bullets("Linear combinations", "What a principal component is", [
        ("A PC is a **weighted sum** of the original variables: PC = w₁x₁ + w₂x₂ + …", 0),
        ("The weights **w** are called **loadings** — they define the direction", 0),
        ("The resulting values are the **scores** — each participant's PC coordinate", 0),
        ("So PCA = choosing loadings that maximise score variance", 0),
    ], i())

    d.section("Part 5", "Eigenvectors & eigenvalues")
    d.definition("Definition", "Eigenvector & eigenvalue",
                 "An **eigenvector** of a matrix is a direction that the matrix only **stretches** (not "
                 "rotates); its **eigenvalue** is the stretch factor.",
                 i(), extra=["For the covariance matrix, eigenvectors = principal component directions",
                             "Eigenvalues = the variance captured along each PC",
                             "Bigger eigenvalue = more important component"])
    d.formula("The equation", "Eigenvectors of the covariance matrix",
              "Σ v = λ v",
              ["**v** — an eigenvector (a principal direction)",
               "**λ** — its eigenvalue (variance along that direction)",
               "Solving this for Σ yields **all** the principal components at once"],
              i(), note="The eigenvector with the largest λ is PC1; the next largest is PC2; and so on.")
    d.figure("The payoff", "Eigenvectors of covariance = principal axes", F("L07_eigen.png"), i(),
             caption="PC1 (largest eigenvalue) runs along the cloud's longest axis; PC2 is orthogonal, "
                     "capturing the remaining spread.")
    d.bullets("Key facts", "Properties of the components", [
        ("Eigenvectors of a symmetric Σ are **orthogonal** → PCs are uncorrelated", 0),
        ("Eigenvalues are **non-negative** and sum to the total variance", 0),
        ("**Ordering** by eigenvalue ranks components by importance", 0),
        ("Proportion of variance explained by PCk = λₖ / Σλ", 0),
    ], i())
    d.checkpoint("In PCA, the eigenvalue associated with a principal component tells you…",
        ["Its direction", "How much variance it captures", "The number of clusters",
         "The correlation with Y"], 1, i(),
        explain="Each eigenvalue is the variance of the data along its eigenvector (that PC). Larger "
                "eigenvalue = more informative component.")

    d.section("Part 6", "Standardisation & geometry")
    d.figure("Scale first", "Why standardising matters for PCA", F("L07_standardize.png"), i(),
             caption="Before standardising, the high-variance variable (energy) hijacks PC1. After, "
                     "every variable competes fairly.")
    d.bullets("Standardise", "Correlation- vs covariance-based PCA", [
        ("On **raw** data, PCA chases the variable with the biggest numeric scale", 0),
        ("**Standardising** (z-scores) makes each variable have variance 1", 0),
        ("Then PCA works on the **correlation** structure — usually what you want", 0),
        ("Exception: if all variables share the same meaningful unit, raw PCA can be fine", 0),
    ], i())
    d.steps("The recipe", "PCA in five conceptual steps", [
        ("Standardise", "centre and scale every variable"),
        ("Covariance", "form the covariance (correlation) matrix"),
        ("Eigen-decompose", "find eigenvectors (directions) and eigenvalues (variances)"),
        ("Order & keep", "rank by eigenvalue, keep the top few PCs"),
        ("Project", "compute scores — the data in the new low-dim coordinates"),
    ], i(), note="Lecture 8 turns this recipe into practice, plots and interpretation.")
    d.big_point("The big picture", "PCA rotates the coordinate axes to line up with the directions of "
                "greatest variance — then throws away the boring ones.",
                i(), sub="No information about *which* variables matter is lost; it's re-expressed.")

    d.section("Part 7", "Consolidate")
    d.bullets("Vocabulary", "Terms you now own", [
        ("**Variance / covariance** — spread and co-movement", 0),
        ("**Covariance matrix** — all of it, in one p×p object", 0),
        ("**Projection / loading / score** — direction, weights, coordinates", 0),
        ("**Eigenvector / eigenvalue** — principal direction and its variance", 0),
    ], i())
    d.exercise("Covariance by hand", [
        "Two participants' (fibre, fullness) values: A = (2, 3), B = (4, 7); means are (3, 5).",
        "Compute the covariance of fibre and fullness from these two points.",
        "Is it positive or negative? What does the sign say about the relationship?",
        "Why must we **standardise** before PCA if fibre is in grams and fullness on a 1–10 scale?",
    ], i(), hint="cov = (1/(n−1)) Σ (xᵢ−x̄)(yᵢ−ȳ); here that's (1/1)[(−1)(−2)+(1)(2)].")
    d.exercise("Reason about directions", [
        "A data cloud is a long, thin ellipse tilted at 45°. Sketch where PC1 and PC2 point.",
        "Which PC has the larger eigenvalue, and why?",
        "If you kept only PC1, what information about the data would you lose?",
    ], i(), hint="PC1 follows the long axis (most variance); PC2 is perpendicular (the thin direction).")
    d.checkpoint("Why run PCA on standardised data when variables have different units?",
        ["To speed it up", "So no single variable dominates purely because of its scale",
         "To make it supervised", "To remove all correlation"], 1, i(),
        explain="Without standardising, a variable measured in large numbers (e.g. kJ) contributes "
                "huge variance and dominates the components for no good reason.")
    d.bullets("Common misconceptions", "Clear these up now", [
        ("PCA is **unsupervised** — it never looks at an outcome Y", 0),
        ("PCs are **new variables**, not a subset of the originals", 0),
        ("High variance ≠ 'important for prediction' — only 'spread out'", 0),
        ("PCA captures **linear** structure only (curved structure needs t-SNE, Lecture 9)", 0),
    ], i())
    d.section("Part 8", "Filling in the linear algebra")
    d.definition("Definition", "Dot product",
                 "The **dot product** xᵀv = Σⱼ xⱼvⱼ multiplies matching coordinates and sums them; it "
                 "measures how much x points along v.",
                 i(), extra=["If v is a unit vector, xᵀv is the length of x's shadow on v",
                             "Dot product zero ⇒ the vectors are **orthogonal** (perpendicular)",
                             "Projections — and hence PCA — are built from dot products"])
    d.definition("Definition", "Orthogonality & unit vectors",
                 "Two directions are **orthogonal** if their dot product is zero; a **unit vector** has "
                 "length one.",
                 i(), extra=["PCA constrains each direction to be a unit vector (‖v‖ = 1)",
                             "Successive PCs are mutually orthogonal → uncorrelated scores",
                             "Together the PCs form a rotated orthonormal coordinate system"])
    d.bullets("Matrix as transformation", "What Σv actually does", [
        ("Multiplying a vector by a matrix generally **rotates and stretches** it", 0),
        ("**Eigenvectors** are the special directions that get **stretched but not rotated**", 0),
        ("The **eigenvalue** is the stretch factor along that direction", 0),
        ("For covariance Σ, the stretch factor **is** the variance in that direction", 0),
    ], i())
    d.formula("Worked 2×2", "Eigenvalues of a small covariance matrix",
              "Σ = [ 2  0 ; 0  1 ]  →  λ = 2 (v = e₁),  λ = 1 (v = e₂)",
              ["A diagonal Σ has the coordinate axes themselves as eigenvectors",
               "Variance is 2 along x₁ and 1 along x₂ → PC1 is the x₁ axis",
               "Off-diagonal terms **tilt** the eigenvectors away from the axes"],
              i())
    d.bullets("Solving in general", "How eigenvalues are found (conceptually)", [
        ("Solve **det(Σ − λI) = 0** for the eigenvalues λ", 0),
        ("For each λ, solve **(Σ − λI)v = 0** for its eigenvector v", 0),
        ("You never do this by hand for real data — software does it instantly", 0),
        ("The **spectral theorem** guarantees a full set of orthogonal eigenvectors for symmetric Σ", 0),
    ], i())
    d.definition("Definition", "Singular value decomposition (SVD)",
                 "The **SVD** factorises the data matrix directly as X = U D Vᵀ; the columns of V are the "
                 "principal directions.",
                 i(), extra=["Software computes PCA via the SVD — it's numerically stabler",
                             "Singular values relate to eigenvalues (variances) of Σ",
                             "Same answer as eigen-decomposing the covariance matrix"])
    d.big_point("Why it always works", "For a symmetric covariance matrix, the principal components "
                "always exist, are orthogonal, and are unique (up to sign).",
                i(), sub="That guarantee — the spectral theorem — is what makes PCA reliable across "
                         "every data set.")
    d.bullets("A little history", "Where PCA came from", [
        ("**Karl Pearson (1901)** — 'lines and planes of closest fit' to data", 0),
        ("**Harold Hotelling (1933)** — formalised principal components", 0),
        ("Now a cornerstone of statistics, signal processing and machine learning", 0),
        ("The same math powers **eigenfaces**, image compression and genomics", 0),
    ], i())
    d.two_col("Where it's used", "PCA across fields",
              left_head="Science & health",
              left=["Genomics & metabolomics structure",
                    "Population genetics (ancestry axes)",
                    "Neuroimaging dimensionality"],
              right_head="Engineering & data",
              right=["Image & signal compression",
                     "Feature extraction for ML",
                     "Anomaly detection via residuals"],
              idx=i())
    d.checkpoint("Successive principal components are orthogonal. A consequence is that the PC scores are…",
        ["Perfectly correlated", "Uncorrelated with each other", "Always positive",
         "Equal in variance"], 1, i(),
        explain="Orthogonal directions produce scores with zero correlation — a key reason PCA removes "
                "redundancy.")
    d.formula("Covariance worked example", "Two variables, three points",
              "x = (1,2,3),  y = (2,4,6)  →  cov(x,y) = 2,  perfectly correlated",
              ["Both increase together in lock-step → large positive covariance",
               "Here y = 2x exactly, so one PC captures **all** the variance",
               "The second PC would have eigenvalue 0 — redundant dimension"],
              i())
    d.bullets("Connecting back", "Why this powers clustering too", [
        ("Cluster in **PC space** to beat the curse of dimensionality", 0),
        ("Uncorrelated PCs suit distance-based methods (k-means, GMM)", 0),
        ("Dropping low-variance PCs **denoises** before clustering", 0),
        ("PCA + clustering is a standard nutrition-data pipeline", 0),
    ], i())
    d.exercise("Eigen-intuition", [
        "For Σ = [[3, 0], [0, 1]], write down the two eigenvectors and eigenvalues by inspection.",
        "Which is PC1? How much of the total variance does it explain?",
        "Now imagine a small off-diagonal term appears. Qualitatively, what happens to the eigenvectors?",
    ], i(), hint="A diagonal matrix has the coordinate axes as eigenvectors; % variance = λ / Σλ.")
    d.bullets("Chapter checklist", "Before Lecture 8, be sure you can…", [
        ("Explain variance, covariance and the covariance matrix", 0),
        ("Describe a projection and a linear combination", 0),
        ("State what eigenvectors/eigenvalues mean for PCA", 0),
        ("Say why standardisation matters", 0),
    ], i())
    d.summary([
        "Dimension reduction fights the **curse of dimensionality** by exploiting correlation.",
        "**Variance** measures spread; PCA treats variance as information to keep.",
        "The **covariance matrix** encodes all pairwise linear structure.",
        "**Eigenvectors** of that matrix are the principal directions; **eigenvalues** are their variances.",
    ], i(), nextup="Lecture 08 — Principal Component Analysis in practice: scores, loadings and biplots.")

    out = os.path.join(HERE, "Lecture07_PCA_Background.pptx"); d.save(out); return out


# ================================================================= LECTURE 08
def lecture08():
    d = Deck(8, "Principal Component Analysis")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Principal Component Analysis in Practice",
            "From the covariance matrix to scores, loadings, scree plots and biplots — and how to "
            "interpret, choose and use principal components on real data.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("PCA recap: the one-slide summary", 0),
        ("Scores and loadings — the two outputs", 0),
        ("How many components? The scree plot", 0),
        ("The biplot: variables and observations together", 0),
        ("PCA as compression and denoising", 0),
        ("Running & interpreting PCA in R; pitfalls", 0),
    ], i())
    d.bullets("Recap", "What we built last lecture", [
        ("PCA finds orthogonal directions of **maximum variance**", 0),
        ("They are the **eigenvectors** of the covariance/correlation matrix", 0),
        ("**Eigenvalues** say how much variance each captures", 0),
        ("Today: turn that into **outputs you can read and use**", 0),
    ], i())
    d.big_point("One-slide PCA", "PCA re-expresses your correlated variables as a smaller set of "
                "uncorrelated 'principal components', ordered by how much variation they explain.",
                i(), sub="Keep the top few and you've compressed the data with minimal loss.")

    d.section("Part 1", "The two outputs: scores & loadings")
    d.figure("Finding PC1", "PC1 is the max-variance direction", F("L08_maxvar.png"), i(),
             caption="Rotating a line and measuring the projected variance: the peak (right) defines "
                     "PC1's direction (left).")
    d.definition("Definition", "Loadings",
                 "**Loadings** are the weights that define each principal component as a linear "
                 "combination of the original variables.",
                 i(), extra=["They describe **what each PC means** in terms of the variables",
                             "Large |loading| = that variable strongly shapes the PC",
                             "Signs show whether variables push the PC up or down together"])
    d.definition("Definition", "Scores",
                 "**Scores** are the coordinates of each observation on the principal components — the "
                 "data re-expressed in the new axes.",
                 i(), extra=["One score per observation per PC",
                             "Plotting PC1 vs PC2 scores is the classic PCA picture",
                             "Scores are what you feed into downstream models"])
    d.figure("Scores plot", "4-D data in 2-D", F("L08_scores.png"), i(),
             caption="Each point is a flower's scores on PC1 and PC2. Two components already separate "
                     "the species — that's the power of PCA.")
    d.figure("Loadings", "How variables build each PC", F("L08_loadings.png"), i(),
             caption="A loadings heatmap. Here PC1 loads on petal measurements; reading loadings is how "
                     "you give each PC a meaning.")
    d.bullets("Interpreting a PC", "Naming components from loadings", [
        ("Look at which variables have **large-magnitude** loadings on that PC", 0),
        ("Variables with the **same sign** move together along the PC", 0),
        ("Give the PC a **name** — e.g. 'overall size', 'protein-vs-carb contrast'", 0),
        ("This is exactly how you'll interpret **dietary indices** in the project", 0),
    ], i())
    d.checkpoint("A PC has large positive loadings on all fat-related variables and near-zero on others. "
                 "You would call it…",
        ["A protein axis", "An overall 'fat intake' component", "Random noise", "PC0"], 1, i(),
        explain="When one group of related variables dominates a component's loadings, the PC represents "
                "that theme — here, overall fat intake.")

    d.section("Part 2", "How many components to keep?")
    d.definition("Definition", "Proportion of variance explained",
                 "Each PC explains a fraction of the total variance equal to its eigenvalue divided by "
                 "the sum of all eigenvalues.",
                 i(), extra=["The fractions sum to 100% across all PCs",
                             "The **cumulative** proportion tells you how much you've retained",
                             "Trade-off: fewer PCs = more compression but more lost variance"])
    d.figure("The scree plot", "Variance captured per component", F("L08_scree.png"), i(),
             caption="Bars = variance per PC; the line = cumulative. Look for the 'elbow' and/or the "
                     "point where the cumulative curve crosses a threshold (e.g. 90%).")
    d.table("Rules of thumb", "Choosing the number of PCs",
            ["Rule", "Keep components…"],
            [["Cumulative variance", "until you reach e.g. 80–90% explained"],
             ["Scree / elbow", "before the curve flattens"],
             ["Kaiser criterion", "with eigenvalue > 1 (on standardised data)"],
             ["Interpretability", "as many as you can meaningfully name"]],
            i(), col_widths=[3.6,7.9])
    d.bullets("Judgement", "No single correct answer", [
        ("For **visualisation**, you usually keep just 2–3", 0),
        ("For **preprocessing**, keep enough to retain most variance (say 90%)", 0),
        ("Rules of thumb **disagree** — use them together, then decide", 0),
        ("Document your choice and its variance retained", 0),
    ], i())
    d.checkpoint("Your first two PCs explain 55% and 25% of variance. Cumulative for PC1–PC2 is…",
        ["25%", "55%", "80%", "30%"], 2, i(),
        explain="Cumulative variance adds them: 55% + 25% = 80% retained by the first two components.")

    d.section("Part 3", "The biplot")
    d.definition("Definition", "Biplot",
                 "A **biplot** overlays observation **scores** (points) and variable **loadings** "
                 "(arrows) on the same PC1–PC2 axes.",
                 i(), extra=["Arrow direction shows how a variable aligns with the PCs",
                             "Arrows pointing the same way = positively correlated variables",
                             "Points far along an arrow score high on that variable"])
    d.figure("Two views at once", "The biplot", F("L08_biplot.png"), i(),
             caption="Petal-length and petal-width arrows point together (correlated) and drive PC1; "
                     "observations spread along them.")
    d.steps("Reading a biplot", "What to look for", [
        ("Arrow length", "longer = better represented in this 2-D view"),
        ("Arrow angle", "small angle between arrows = correlated variables"),
        ("Right angle", "≈ uncorrelated variables"),
        ("Point position", "where an observation sits relative to the arrows"),
    ], i())
    d.bullets("Biplot cautions", "Read with care", [
        ("The biplot only shows the **first two** PCs — variance beyond them is hidden", 0),
        ("Short arrows are **poorly represented** — don't over-interpret them", 0),
        ("Always report **how much variance** PC1 & PC2 capture on the axes", 0),
    ], i())

    d.section("Part 4", "PCA as compression")
    d.figure("Reconstruction", "Rebuilding data from a few PCs", F("L08_reconstruction.png"), i(),
             caption="A handwritten digit reconstructed from 2, 5, 10, 20 principal components. A "
                     "fraction of the 64 dimensions recovers most of the image.")
    d.bullets("Compression & denoising", "Two practical superpowers", [
        ("**Compression** — store scores on a few PCs instead of all variables", 0),
        ("**Denoising** — low-variance PCs often capture noise; dropping them cleans data", 0),
        ("**Preprocessing** — feed PCs into clustering or classification to fight collinearity", 0),
        ("Reconstruction error shrinks as you keep more PCs", 0),
    ], i())
    d.big_point("Elegant duality", "The same eigen-decomposition that maximises retained variance also "
                "minimises reconstruction error.",
                i(), sub="Keeping the top PCs is the best possible linear compression of your data.")

    d.section("Part 5", "PCA in R")
    d.code("Fitting", "prcomp is all you need", [
        "# ALWAYS standardise unless variables share meaningful units",
        "pca <- prcomp(diet_numeric, center = TRUE, scale. = TRUE)",
        "",
        "summary(pca)          # proportion & cumulative variance",
        "pca$rotation          # loadings (variables x PCs)",
        "pca$x                 # scores (observations x PCs)",
    ], i())
    d.code("Visualising", "Scree, scores and biplot", [
        "library(factoextra)",
        "fviz_eig(pca)                     # scree plot",
        "fviz_pca_ind(pca, col.ind = group)# score plot, coloured",
        "fviz_pca_biplot(pca)              # biplot",
        "",
        "get_eigenvalue(pca)               # eigenvalues & % variance",
    ], i())
    d.bullets("Workflow", "Using PCs downstream", [
        ("Fit PCA on the **training** data; apply the **same** rotation to test data (`predict`)", 0),
        ("Keep the PCs that reach your variance target", 0),
        ("Cluster or classify on the **scores**, not the raw variables", 0),
        ("Interpret results back through the **loadings**", 0),
    ], i())
    d.bullets("Worked example", "PCA on the nutrition data", [
        ("Standardise ~30 intake variables; run **prcomp**", 0),
        ("Scree shows PC1–PC4 capture ~85% of variance", 0),
        ("Loadings: PC1 = 'overall intake', PC2 = 'plant vs animal' contrast", 0),
        ("Plot participants on PC1–PC2; overlay a health outcome by colour", 0),
        ("Feed the 4 PCs into clustering for cleaner dietary patterns", 0),
    ], i())

    d.section("Part 6", "Pitfalls & limitations")
    d.bullets("Pitfall 1", "Forgetting to standardise", [
        ("Raw PCA lets the biggest-scale variable dominate PC1", 0),
        ("Nearly always set **scale. = TRUE** for mixed-unit data", 0),
    ], i())
    d.bullets("Pitfall 2", "Over-interpreting components", [
        ("PCs are **mathematical constructs**; not every one has a tidy meaning", 0),
        ("Sign is **arbitrary** — a PC and its negative are the same component", 0),
        ("Low-variance PCs are often noise — don't chase stories in them", 0),
    ], i())
    d.bullets("Pitfall 3", "Assuming linearity", [
        ("PCA captures **linear** structure only", 0),
        ("Curved / manifold structure needs **t-SNE or UMAP** (next lecture)", 0),
        ("PCA is also sensitive to **outliers** — clean first", 0),
    ], i())
    d.checkpoint("PC1 explains 5% of the variance in your data. This suggests…",
        ["PC1 is very important", "The variables are largely uncorrelated — little to compress",
         "You must keep only PC1", "The data is noise-free"], 1, i(),
        explain="If even the top component captures little variance, no single direction dominates — "
                "the variables are nearly uncorrelated and PCA won't compress much.")
    d.exercise("Run and read a PCA", [
        "Run **prcomp(scale = TRUE)** on the nutrition variables. How many PCs reach 90% variance?",
        "Examine PC1's loadings — which variables dominate, and what would you name it?",
        "Plot PC1 vs PC2 scores coloured by a health group. Do groups separate?",
        "Compare clustering on the **PC scores** vs the raw variables — any difference?",
    ], i(), hint="summary(pca) gives cumulative variance; pca$rotation[,1] holds PC1's loadings.")
    d.exercise("Interpret a biplot", [
        "In a biplot, two variable arrows point in nearly the same direction. What does that imply?",
        "A third arrow is at right angles to them. What does that imply?",
        "An observation sits far out along the first two arrows. Describe its profile.",
        "Why should you check the % variance on the axes before trusting the picture?",
    ], i(), hint="Small angle → correlated; right angle → uncorrelated; position along an arrow → high on "
                 "that variable.")
    d.bullets("Beyond PCA", "A look ahead", [
        ("**t-SNE / UMAP** — non-linear reduction for visualisation (Lecture 9)", 0),
        ("**Factor analysis** — models shared latent factors, not just variance", 0),
        ("**Kernel PCA** — PCA in a transformed space for non-linear structure", 0),
        ("PCA remains the **first tool to reach for** — fast, linear, interpretable", 0),
    ], i())
    d.bullets("Key ideas recap", "Hold onto these", [
        ("**Loadings** define PCs; **scores** place observations on them", 0),
        ("Choose the number of PCs with the **scree plot** and variance retained", 0),
        ("The **biplot** shows variables and observations together", 0),
        ("PCA = best linear **compression**; always **standardise** first", 0),
    ], i())

    d.section("Part 7", "Related methods & a full case study")
    d.two_col("PCA vs factor analysis", "Close cousins, different goals",
              left_head="PCA",
              left=["Maximises **variance** explained",
                    "Components are exact linear combos",
                    "Descriptive / compression focus",
                    "No underlying model of the data"],
              right_head="Factor analysis",
              right=["Models shared **latent factors** + noise",
                     "Aims to explain **correlations**",
                     "Assumes a generative model",
                     "Common in psychology / surveys"],
              idx=i())
    d.definition("Definition", "Component rotation (varimax)",
                 "**Rotation** re-orients retained components to make loadings closer to 0 or ±1, so "
                 "each PC loads on fewer variables and is easier to name.",
                 i(), extra=["Trades the max-variance property for **interpretability**",
                             "Varimax is the most common rotation",
                             "Popular when the goal is naming interpretable indices"])
    d.bullets("PCA helps clustering", "Why they pair so well", [
        ("Clustering in high dimensions is unreliable (curse of dimensionality)", 0),
        ("Reduce to a handful of PCs first, then cluster on **scores**", 0),
        ("Removes correlated redundancy and much of the noise", 0),
        ("Standard recipe: **standardise → PCA → k-means/GMM**", 0),
    ], i())
    d.bullets("Eigenfaces & images", "PCA in the wild", [
        ("Treat each image as a long vector of pixels", 0),
        ("PCA on many faces yields **'eigenfaces'** — the main directions of variation", 0),
        ("Any face ≈ average + a few eigenface scores → strong compression", 0),
        ("The exact idea behind the digit reconstruction we just saw", 0),
    ], i())
    d.definition("Definition", "Reproducibility of PCA",
                 "To reproduce a PCA you must record the **centring/scaling**, the **number of PCs**, and "
                 "apply the **training rotation** to any new data.",
                 i(), extra=["Never re-fit PCA separately on test data — that leaks and shifts axes",
                             "Use `predict(pca, newdata)` to project new observations",
                             "Report % variance retained alongside every PCA figure"])
    d.big_point("Case study", "Nutrition data: 32 intake variables → 5 principal components "
                "capturing 88% of variation.",
                i(), sub="From an unwieldy wide table to five interpretable dietary indices you can "
                         "plot, cluster and model.")
    d.steps("Case study workflow", "PCA end-to-end on the project data", [
        ("Clean & standardise", "impute, z-score all 32 intake variables"),
        ("Fit PCA", "prcomp(scale.=TRUE); inspect the scree plot"),
        ("Keep 5 PCs", "they reach 88% cumulative variance"),
        ("Name them", "PC1 'overall intake', PC2 'plant vs animal', PC3 'sugar load'…"),
        ("Use downstream", "cluster on scores; regress health outcome on PCs"),
    ], i())
    d.table("Case study output", "Interpreting the retained components",
            ["PC", "% variance", "Dominant loadings → name"],
            [["PC1", "41%", "all intakes + → 'overall intake'"],
             ["PC2", "19%", "veg/fruit + vs meat − → 'plant vs animal'"],
             ["PC3", "13%", "sugar, refined carbs → 'sugar load'"],
             ["PC4", "9%", "dairy, calcium → 'dairy'"],
             ["PC5", "6%", "alcohol → 'alcohol'"]],
            i(), col_widths=[1.3,2.4,7.8])
    d.bullets("Reporting PCA", "What a good write-up includes", [
        ("A **scree plot** and the variance retained by your chosen PCs", 0),
        ("A **loadings table/heatmap** with your interpretation of each PC", 0),
        ("A **score (or bi-) plot** coloured by a meaningful grouping", 0),
        ("A sentence on **standardisation** and how many PCs you kept and why", 0),
    ], i())
    d.checkpoint("You standardised, ran PCA on training data, and now have test data. You should…",
        ["Re-run prcomp on the test data", "Project test data with the training rotation (predict)",
         "Skip PCA on test data", "Average the two PCAs"], 1, i(),
        explain="Apply the *training* PCA to test data via predict() so both live in the same "
                "coordinate system — re-fitting would change the axes and leak information.")
    d.two_col("When PCA is the wrong tool", "Know its limits",
              left_head="PCA struggles when",
              left=["Structure is **non-linear** / curved",
                    "You care about **rare** low-variance signals",
                    "Variables are **categorical**",
                    "Outliers dominate the variance"],
              right_head="Reach instead for",
              right=["**t-SNE / UMAP** (non-linear viz)",
                     "**Supervised** methods for prediction",
                     "**MCA** for categorical data",
                     "**Robust PCA** with outliers"],
              idx=i())
    d.exercise("Design a PCA analysis", [
        "Your team has 40 metabolite variables and wants to visualise participant structure.",
        "Write the full pipeline from raw data to a 2-D score plot (name each step).",
        "State how you'll decide the number of PCs and how you'll interpret PC1.",
        "How will you check the 2-D picture isn't hiding important variation?",
    ], i(), hint="Clean → standardise → prcomp → scree → keep PCs → scores plot; check cumulative "
                 "variance of PC1–PC2.")
    d.bullets("Exam pointers", "What tends to be tested", [
        ("Distinguish **scores** vs **loadings**", 0),
        ("Read a **scree plot** and compute cumulative variance", 0),
        ("Interpret a **biplot** (angles, lengths, positions)", 0),
        ("Explain **why standardise** and what eigenvalues mean", 0),
    ], i())
    d.checkpoint("Which pair correctly matches PCA outputs to their meaning?",
        ["Scores = variable weights; loadings = observation coordinates",
         "Scores = observation coordinates; loadings = variable weights",
         "Both describe variables", "Both describe observations"], 1, i(),
        explain="Scores place each observation on the PCs; loadings are the variable weights that "
                "define each PC.")
    d.bullets("Cheat-sheet", "PCA in R, one screen", [
        ("**Fit**: `prcomp(X, scale. = TRUE)`", 0),
        ("**Variance**: `summary()` or `get_eigenvalue()`", 0),
        ("**Loadings**: `pca$rotation` · **Scores**: `pca$x`", 0),
        ("**Plots**: `fviz_eig`, `fviz_pca_ind`, `fviz_pca_biplot`", 0),
        ("**New data**: `predict(pca, newdata)`", 0),
    ], i())
    d.big_point("The bridge to Week 3's end", "You can now take wide, correlated nutrition data and "
                "compress it into a few meaningful axes — ready to visualise, cluster, or model.",
                i(), sub="Next we handle structure PCA can't: non-linear, curved patterns.")
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *An Introduction to Statistical Learning*, Ch. 12", 0),
        ("Hastie et al., *The Elements of Statistical Learning*, §14.5", 0),
        ("R: the **factoextra** and **FactoMineR** vignettes", 0),
    ], i())
    d.summary([
        "PCA turns correlated variables into a few uncorrelated **components** ranked by variance.",
        "**Loadings** tell you what each PC means; **scores** re-express the observations.",
        "Use the **scree plot** and cumulative variance to choose how many PCs to keep.",
        "PCA is the best linear **compression** — powerful for visualisation, denoising and preprocessing.",
    ], i(), nextup="Lecture 09 — Dimension reduction beyond PCA: MDS, t-SNE and when to use them.")

    out = os.path.join(HERE, "Lecture08_PCA.pptx"); d.save(out); return out


if __name__ == "__main__":
    for f in (lecture07, lecture08):
        p=f(); print(f"{os.path.basename(p)}  —  {len(Presentation(p).slides._sldIdLst)} slides")
