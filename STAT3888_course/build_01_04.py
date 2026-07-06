# -*- coding: utf-8 -*-
"""Assemble STAT3888 lecture decks 01-04."""
from slides import (build, title_slide, objectives_slide, content_slide, figure_slide,
                    exercise_slide, summary_slide, cols, card, code, formula, callout, HERE)
import os

# ============================================================ LECTURE 01
def lecture01():
    s = []
    s.append(title_slide(1, "Introduction to Statistical Machine Learning",
        "What this unit is about, how machines learn from data, and the interdisciplinary nutrition project."))
    s.append(objectives_slide([
        "Explain what <b>statistical machine learning</b> is and how it differs from classical statistics.",
        "Distinguish <b>supervised</b> from <b>unsupervised</b> learning with real examples.",
        "Describe the end-to-end <b>data-analysis workflow</b> you will follow all semester.",
        "Understand the <b>NUTM3888 joint project</b> and how you will be assessed."]))

    s.append(content_slide("What is statistical machine learning?",
        cols(
          card("The goal",
               "<p>Build algorithms that <b>learn patterns from data</b> to make predictions or "
               "discover structure — <i>without being explicitly programmed</i> for the task.</p>", "blue"),
          card("Statistics meets ML",
               "<p>Classical statistics asks <i>“is this effect real?”</i> (inference). "
               "ML asks <i>“how well can I predict the next case?”</i>. "
               "This unit lives at their <b>intersection</b>.</p>", "red")
        ) +
        callout("<b>Two cultures (Breiman, 2001):</b> the <i>data-modelling</i> culture assumes a stochastic "
                "model; the <i>algorithmic</i> culture treats the mechanism as unknown and optimises prediction. "
                "Good data scientists move fluidly between both.", "key"),
        kicker="Big picture"))

    s.append(figure_slide("The two families you will learn", "figures/L01_super_vs_unsuper.png",
        caption="Left: unsupervised — we only see the points and must find the groups. "
                "Right: supervised — each point carries a known label and we learn the rule.",
        kicker="Supervised vs unsupervised",
        side=card("How to tell them apart",
            "<p><b>Is there a target variable Y?</b></p>"
            "<p>✔ <b>Yes</b> → supervised (regression if Y is numeric, classification if categorical).</p>"
            "<p>✘ <b>No</b> → unsupervised (clustering, dimension reduction).</p>", "teal")))

    s.append(content_slide("The methods map of STAT3888",
        "<table><tr><th>Unsupervised (Weeks 1–3)</th><th>Supervised (Weeks 4–7)</th></tr>"
        "<tr><td>k-means, model-based &amp; hierarchical clustering</td><td>Logistic &amp; penalised logistic regression</td></tr>"
        "<tr><td>Principal component analysis</td><td>Discriminant analysis, k-NN</td></tr>"
        "<tr><td>Dimension reduction</td><td>Trees, random forests</td></tr>"
        "<tr><td>Graphical / log-linear models</td><td>Neural networks, support vector machines</td></tr></table>"
        + callout("Every method answers the same three questions: <b>what does it assume, "
                  "how is it fit, and how do we know it worked?</b> Keep asking these.", "tip")))

    s.append(figure_slide("The data-analysis workflow", "figures/L01_pipeline.png",
        caption="You will iterate this loop for your nutrition project — real projects cycle back often.",
        kicker="How we work"))

    s.append(content_slide("The joint project with NUTM3888",
        cols(
          card("The teams",
               "<p>Statistics/Data Science students team with <b>Nutrition (Metabolic Cybernetics)</b> "
               "students to answer a real question from a <b>nutrition &amp; metabolomics</b> data set.</p>", "blue"),
          card("Your edge",
               "<p>You bring the <b>statistical machine learning</b>. They bring the "
               "<b>domain question</b> and interpretation. Neither succeeds alone — this is "
               "interdisciplinary practice (GQ7).</p>", "red"))
        + callout("Data science is <b>inherently interdisciplinary</b>. The hardest part is rarely the "
                  "algorithm — it is framing the right question and communicating the answer.", "key")))

    s.append(content_slide("How you are assessed",
        "<table><tr><th>Component</th><th>Weight</th><th>When</th></tr>"
        "<tr><td>Final written exam</td><td>35%</td><td>Exam period</td></tr>"
        "<tr><td>Disciplinary assignment (individual)</td><td>15%</td><td>Week 11</td></tr>"
        "<tr><td>Major project — presentation</td><td>15%</td><td>Week 12</td></tr>"
        "<tr><td>Major project — manuscript</td><td>25%</td><td>Week 13</td></tr>"
        "<tr><td>Contribution / reflection / peer review</td><td>10%</td><td>Week 13</td></tr></table>"
        + callout("The project pitch (Week 6) and optional quiz (Week 9) are worth 0% but are "
                  "<b>critical rehearsals</b> — treat them seriously.", "warn")))

    s.append(exercise_slide("Warm-up: classify the task",
        "<p>For each scenario, decide <b>supervised</b> or <b>unsupervised</b>, and name the sub-type "
        "(regression / classification / clustering / dimension reduction):</p>"
        "<ol>"
        "<li>Predict a person's fasting glucose from 30 dietary intake variables.</li>"
        "<li>Group 500 participants into dietary <i>patterns</i> with no pre-defined labels.</li>"
        "<li>Flag whether a food diary entry is <i>plausible</i> or a data-entry error.</li>"
        "<li>Compress 200 correlated nutrient measurements into a handful of indices.</li>"
        "</ol>",
        hint="Ask first: <i>is there a target variable Y, and if so, is it numeric or categorical?</i>"))

    s.append(summary_slide([
        "ML learns <b>patterns from data</b>; it sits between classical inference and pure prediction.",
        "<b>Supervised</b> = labelled Y (regression/classification); <b>unsupervised</b> = structure discovery.",
        "The <b>workflow</b> — clean → model → evaluate → communicate — is iterative, not linear.",
        "Your project is <b>interdisciplinary</b>: the statistics is necessary but not sufficient."],
        nextup="Lecture 02 — Data cleaning: the unglamorous 80% of every project."))
    build(s, os.path.join(HERE, "lesson01.html"), "STAT3888 · Lecture 01 — Introduction")

# ============================================================ LECTURE 02
def lecture02():
    s = []
    s.append(title_slide(2, "Data Cleaning &amp; Preprocessing",
        "Garbage in, garbage out. How to turn a messy survey into an analysis-ready matrix."))
    s.append(objectives_slide([
        "Diagnose common data-quality problems: missingness, outliers, inconsistent types.",
        "Distinguish <b>MCAR / MAR / MNAR</b> missingness and choose a sensible response.",
        "Apply <b>standardisation</b> and other transforms, and know when they matter.",
        "Build a <b>reproducible</b> cleaning pipeline in R."]))

    s.append(content_slide("Why cleaning dominates real projects",
        callout("Surveys and lab data are <b>never</b> tidy: typos, impossible values, mixed units, "
                "duplicate rows, free-text where numbers belong, and gaps everywhere.", "warn")
        + cols(
          card("The tidy-data target",
               "<p>Each <b>row</b> = one observation, each <b>column</b> = one variable, "
               "each <b>cell</b> = one value. Your goal is a clean numeric/factor matrix.</p>", "blue"),
          card("Reproducibility",
               "<p>Never edit the raw file by hand. Every fix lives in a <b>script</b> so it can be "
               "re-run, reviewed, and trusted (GQ4).</p>", "teal"))))

    s.append(figure_slide("Step 1 — see the missingness", "figures/L02_missingness.png",
        caption="A missing-data map reveals patterns: variable V5 has a block of missing values "
                "(possible skip-logic), while others are scattered.",
        kicker="Diagnose",
        side=card("Three mechanisms",
            "<p><b>MCAR</b> — missing completely at random (rare, benign).</p>"
            "<p><b>MAR</b> — missingness depends on <i>observed</i> variables (handle by conditioning).</p>"
            "<p><b>MNAR</b> — depends on the <i>unobserved</i> value itself (dangerous, e.g. under-reporting high intake).</p>", "red")))

    s.append(content_slide("What to do about missing values",
        "<table><tr><th>Strategy</th><th>When</th><th>Risk</th></tr>"
        "<tr><td>Complete-case (drop rows)</td><td>Few, MCAR</td><td>Bias + lost power if not MCAR</td></tr>"
        "<tr><td>Mean/median imputation</td><td>Quick baseline</td><td>Shrinks variance, distorts correlations</td></tr>"
        "<tr><td>Model-based / kNN imputation</td><td>MAR</td><td>Needs care, can leak</td></tr>"
        "<tr><td>Multiple imputation (<code>mice</code>)</td><td>Principled inference</td><td>More complex</td></tr></table>"
        + callout("Rule of thumb: <b>impute using the training data only</b>, then apply the same rule to "
                  "test data — otherwise you leak information and over-state performance.", "key")))

    s.append(content_slide("Outliers, types & sanity checks",
        cols(
          card("Range &amp; logic checks",
               "<p>Energy intake of 80,000 kJ/day? Age of 200? Negative weight? "
               "Define <b>plausible ranges</b> and flag violations.</p>", "blue"),
          card("Robust detection",
               "<p>Prefer <b>median &amp; IQR</b> over mean &amp; SD when hunting outliers — the mean is "
               "itself dragged by the outlier.</p>", "red"))
        + callout("An outlier is not automatically an error. Investigate before you delete — it may be the "
                  "most interesting participant in the study.", "tip")))

    s.append(figure_slide("Step 2 — put variables on comparable scales", "figures/L02_scaling.png",
        caption="Energy (kJ) and Vitamin C (mg) live on different scales. Distance-based methods "
                "(k-means, PCA, k-NN) are dominated by the large-scale variable unless you standardise.",
        kicker="Transform",
        side=formula("z<sub>i</sub> = ( <span class='v'>x</span><sub>i</sub> − <span class='v'>x̄</span> ) / <span class='v'>s</span>")
             + card("Also common", "<p>log-transform skewed intakes; min–max scale to [0,1]; "
                    "encode categoricals as factors / dummies.</p>", "teal")))

    s.append(content_slide("A reproducible cleaning pipeline in R",
        code(
"library(tidyverse)\n\n"
"clean <- raw %>%\n"
"  janitor::clean_names() %>%              # tidy column names\n"
"  distinct() %>%                          # drop duplicate rows\n"
"  mutate(sex = factor(sex),\n"
"         energy_kj = na_if(energy_kj, 0)) %>%   # 0 = not recorded\n"
"  filter(between(age, 18, 100)) %>%       # logic check\n"
"  mutate(across(where(is.numeric),        # standardise numerics\n"
"                ~ as.numeric(scale(.))))\n\n"
"skimr::skim(clean)   # profile the result", "r")
        + callout("Chain each fix with <code>%>%</code> so the whole pipeline is one auditable object.", "tip")))

    s.append(exercise_slide("Clean this record",
        "<p>A dietary record reads:</p>"
        "<p><code>age = 24, sex = \"F \", energy_kj = 0, veg_serves = -1, "
        "vitc_mg = 4200, height_cm = 168</code></p>"
        "<ol>"
        "<li>Identify <b>three</b> data-quality problems.</li>"
        "<li>State whether each is likely an <i>error</i> or a <i>genuine</i> extreme, and how you would confirm.</li>"
        "<li>Write the <code>mutate()</code>/<code>filter()</code> lines that would handle them.</li>"
        "</ol>",
        hint="Whitespace in factors, a structural zero, an impossible negative, and an implausible vitamin C value."))

    s.append(summary_slide([
        "Cleaning is <b>most</b> of the work — do it in a script, never by hand.",
        "Diagnose missingness first; the <b>mechanism (MCAR/MAR/MNAR)</b> dictates the fix.",
        "Fit imputation and scaling on <b>training data only</b> to avoid leakage.",
        "Standardise before any <b>distance-based</b> method (next: clustering!)."],
        nextup="Lecture 03 — Unsupervised learning: introduction to clustering."))
    build(s, os.path.join(HERE, "lesson02.html"), "STAT3888 · Lecture 02 — Data Cleaning")

# ============================================================ LECTURE 03
def lecture03():
    s = []
    s.append(title_slide(3, "Unsupervised Learning: Introduction to Clustering",
        "Finding groups in data when nobody tells you the labels."))
    s.append(objectives_slide([
        "Define the <b>clustering</b> problem and give nutrition examples.",
        "Explain the role of a <b>distance / dissimilarity</b> measure.",
        "Contrast <b>within-cluster</b> and <b>between-cluster</b> variation.",
        "List the main clustering families and how their assumptions differ."]))

    s.append(figure_slide("What clustering does", "figures/L03_clusters.png",
        caption="From an unlabelled cloud (left) we propose a partition into groups (right). "
                "There is no ‘true’ answer to check against — clustering is exploratory.",
        kicker="The problem"))

    s.append(content_slide("Why cluster nutrition data?",
        cols(
          card("Dietary patterns",
               "<p>Instead of studying 50 nutrients one at a time, group people into a few "
               "<b>eating patterns</b> (e.g. ‘prudent’ vs ‘Western’) and study those.</p>", "blue"),
          card("Metabolic subtypes",
               "<p>Cluster participants by metabolite profiles to reveal <b>subgroups</b> that respond "
               "differently — a hypothesis generator for the project.</p>", "red"))
        + callout("Clustering is <b>unsupervised</b>: we use it to <i>discover</i> and <i>describe</i> "
                  "structure, then validate biologically — not to predict a known label.", "key")))

    s.append(content_slide("Everything hinges on distance",
        "<p>A clustering algorithm needs a way to say how <b>far apart</b> two observations are.</p>"
        + formula("Euclidean:&nbsp; d(<span class='v'>x</span>,<span class='v'>y</span>) = "
                  "√ Σ<sub>j</sub> (<span class='v'>x</span><sub>j</sub> − <span class='v'>y</span><sub>j</sub>)²")
        + cols(
          card("Common choices",
               "<p><b>Euclidean</b> — straight-line, the default.</p>"
               "<p><b>Manhattan</b> — sum of absolute differences, robust.</p>"
               "<p><b>Correlation</b> — shape not magnitude (good for profiles).</p>", "teal"),
          card("Watch out",
               "<p>Distance is <b>scale-sensitive</b> — standardise first (Lecture 02!). "
               "The metric encodes what you mean by ‘similar’, so choose it deliberately.</p>", "red"))))

    s.append(figure_slide("What makes a clustering ‘good’?", "figures/L03_withinbetween.png",
        caption="We want points close to their own centre (small within-cluster variation) and "
                "centres far apart (large between-cluster variation).",
        kicker="The objective",
        side=formula("Total SS = <span class='v'>Within</span> + <span class='v'>Between</span>")
             + card("The trade-off","<p>Most algorithms minimise <b>within-cluster</b> variation. "
                    "Adding clusters always reduces it — so we need principled ways to choose "
                    "the number of clusters (Lecture 04).</p>", "blue")))

    s.append(content_slide("The families of clustering methods",
        "<table><tr><th>Family</th><th>Idea</th><th>This unit</th></tr>"
        "<tr><td>Partitioning</td><td>Split into k groups minimising within-SS</td><td><b>k-means</b> (L04)</td></tr>"
        "<tr><td>Model-based</td><td>Data from a mixture of distributions</td><td><b>GMM</b> (L05)</td></tr>"
        "<tr><td>Hierarchical</td><td>Build a tree of nested groups</td><td><b>agglomerative</b> (L06)</td></tr>"
        "<tr><td>Density-based</td><td>Clusters = dense regions</td><td>DBSCAN (mentioned)</td></tr></table>"
        + callout("No method is universally best. Each encodes assumptions about cluster "
                  "<b>shape, size and separation</b> — match the method to your data.", "tip")))

    s.append(exercise_slide("Reason about distance",
        "<p>Two participants have daily intakes (energy kJ, vitamin C mg):</p>"
        "<p>A = (8000, 60), B = (8000, 120), C = (16000, 60)</p>"
        "<ol>"
        "<li>Compute the Euclidean distance A–B and A–C on the <b>raw</b> scale.</li>"
        "<li>Which pair looks ‘closer’? Is that the answer you want?</li>"
        "<li>Recompute after standardising (assume SD = 4000 kJ and 30 mg). What changes, and why?</li>"
        "</ol>",
        hint="Raw distances are dominated by energy because its numbers are ~100× larger."))

    s.append(summary_slide([
        "Clustering finds <b>groups without labels</b> — an exploratory, hypothesis-generating tool.",
        "A <b>distance measure</b> defines ‘similar’; it is scale-sensitive, so standardise first.",
        "Good clusterings have <b>small within, large between</b> variation.",
        "Families differ by <b>assumptions</b>; we start with partitioning next."],
        nextup="Lecture 04 — K-means clustering: the workhorse partitioning method."))
    build(s, os.path.join(HERE, "lesson03.html"), "STAT3888 · Lecture 03 — Intro to Clustering")

# ============================================================ LECTURE 04
def lecture04():
    s = []
    s.append(title_slide(4, "K-means Clustering",
        "The workhorse partitioning algorithm: how it works, how to tune it, and where it breaks."))
    s.append(objectives_slide([
        "State the <b>k-means objective</b> and describe <b>Lloyd's algorithm</b>.",
        "Explain why k-means finds a <b>local</b> optimum and how random restarts help.",
        "Choose the number of clusters with the <b>elbow</b> and <b>silhouette</b> methods.",
        "Recognise the <b>assumptions</b> of k-means and when it fails."]))

    s.append(content_slide("The objective",
        "<p>K-means partitions <i>n</i> points into <i>k</i> clusters C<sub>1</sub>,…,C<sub>k</sub> to "
        "minimise the total <b>within-cluster sum of squares</b>:</p>"
        + formula("min<sub>C</sub> &nbsp; Σ<sub>k</sub> Σ<sub><span class='v'>x</span>∈C<sub>k</sub></sub> "
                  "‖ <span class='v'>x</span> − <span class='v'>μ</span><sub>k</sub> ‖²")
        + cols(
          card("In words","<p>Each cluster is summarised by its <b>centroid</b> μ<sub>k</sub> (the mean). "
               "We want every point close to its own centroid.</p>", "blue"),
          card("Why it's hard","<p>Searching all partitions is <b>NP-hard</b>. Lloyd's algorithm gives a fast, "
               "greedy approximation that usually works well.</p>", "red"))))

    s.append(figure_slide("Lloyd's algorithm in action", "figures/L04_iterations.png",
        caption="Assign each point to the nearest centroid, then move each centroid to its points' mean; "
                "repeat until nothing changes. Here a poor start converged to a sub-optimal split — "
                "motivating random restarts.",
        kicker="The algorithm"))

    s.append(content_slide("The algorithm, step by step",
        "<p><b>Input:</b> data X, number of clusters k.</p>"
        "<ol>"
        "<li><b>Initialise</b> k centroids (randomly, or better with <code>k-means++</code>).</li>"
        "<li><b>Assign</b> each point to its nearest centroid.</li>"
        "<li><b>Update</b> each centroid to the mean of its assigned points.</li>"
        "<li><b>Repeat</b> 2–3 until assignments stop changing.</li>"
        "</ol>"
        + callout("Each step can only <b>decrease</b> the within-SS, so the algorithm always converges — "
                  "but possibly to a <b>local</b> minimum that depends on the starting centroids.", "key")))

    s.append(content_slide("Local optima &amp; how to beat them",
        cols(
          card("The problem","<p>Different random starts can give different clusterings. A bad start "
               "gets stuck (see the ‘Converged’ panel on the previous slide).</p>", "red"),
          card("The fixes","<p>Run k-means from <b>many random starts</b> and keep the best "
               "(lowest within-SS). Use <b>k-means++</b> initialisation to spread starting "
               "centroids apart.</p>", "teal"))
        + code("set.seed(1)\n"
               "km <- kmeans(X, centers = 3, nstart = 25)  # 25 random restarts\n"
               "km$tot.withinss   # objective value\n"
               "km$cluster        # cluster labels", "r")))

    s.append(figure_slide("Choosing k: elbow &amp; silhouette", "figures/L04_elbow.png",
        caption="Left: within-SS always falls with k — look for the ‘elbow’ where the gain flattens. "
                "Right: the silhouette rewards well-separated clusters and often gives a clearer peak.",
        kicker="How many clusters?",
        side=formula("s(i) = ( b<sub>i</sub> − a<sub>i</sub> ) / max(a<sub>i</sub>, b<sub>i</sub>)")
             + card("Reading silhouette","<p>a<sub>i</sub> = mean distance to own cluster; "
                    "b<sub>i</sub> = mean distance to nearest other cluster. "
                    "Near <b>+1</b> = well clustered, near <b>0</b> = on a boundary.</p>", "blue")))

    s.append(figure_slide("Know the assumptions — and the failure mode", "figures/L04_failure.png",
        caption="K-means assumes roughly spherical, equal-size clusters and uses Euclidean distance. "
                "On these two interleaving ‘moons’ it carves a straight boundary and gets them wrong.",
        kicker="Limitations",
        side=card("When k-means struggles",
            "<p>• Non-convex / elongated shapes</p>"
            "<p>• Very different cluster sizes or densities</p>"
            "<p>• Unscaled variables</p>"
            "<p>→ Consider GMM (L05), hierarchical (L06) or density-based methods.</p>", "red")))

    s.append(exercise_slide("Run and diagnose k-means",
        "<p>Using the standardised nutrition data:</p>"
        "<ol>"
        "<li>Fit k-means for k = 2,…,8 with <code>nstart = 25</code> and record <code>tot.withinss</code>.</li>"
        "<li>Plot within-SS vs k. Where is the elbow?</li>"
        "<li>Compute the mean silhouette for each k (<code>cluster::silhouette</code>). Do the two methods agree?</li>"
        "<li>For your chosen k, profile the cluster means — can you give each cluster a nutrition <i>name</i>?</li>"
        "</ol>",
        hint="Naming clusters from their centroid profiles is exactly what you'll do in the project."))

    s.append(summary_slide([
        "K-means minimises <b>within-cluster sum of squares</b> via assign–update iterations.",
        "It converges to a <b>local</b> optimum — always use many <b>restarts</b> / k-means++.",
        "Choose k with the <b>elbow</b> and <b>silhouette</b>; let interpretability decide ties.",
        "It assumes <b>round, comparable</b> clusters — standardise, and switch methods when that fails."],
        nextup="Lecture 05 — Model-based clustering: soft assignments with Gaussian mixtures."))
    build(s, os.path.join(HERE, "lesson04.html"), "STAT3888 · Lecture 04 — K-means")

if __name__ == "__main__":
    lecture01(); lecture02(); lecture03(); lecture04()
    print("Built lesson01.html … lesson04.html")
