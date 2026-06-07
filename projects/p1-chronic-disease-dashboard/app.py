"""
Australian Chronic Disease Trends Dashboard
Data source: Synthetic data based on AIHW published statistics (2013-2023)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Australian Chronic Disease Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f7ff;
        border-left: 4px solid #1f77b4;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .metric-card h3 { margin: 0; font-size: 0.85rem; color: #555; font-weight: 500; }
    .metric-card p  { margin: 4px 0 0; font-size: 1.8rem; font-weight: 700; color: #1f4e79; }
    .section-header { font-size: 1.1rem; font-weight: 600; color: #1f4e79; margin-bottom: 4px; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DISEASE_LABELS = {
    "diabetes_prevalence_pct":       "Type 2 Diabetes",
    "cvd_prevalence_pct":            "Cardiovascular Disease",
    "mental_health_prevalence_pct":  "Mental Health Conditions",
    "obesity_prevalence_pct":        "Obesity",
}
STATE_COLOURS = px.colors.qualitative.Set2

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = "data/raw/"
    prev = pd.read_csv(base + "prevalence_by_state_age_sex.csv")
    adm  = pd.read_csv(base + "hospital_admissions_by_state.csv")
    exp  = pd.read_csv(base + "health_expenditure_by_state.csv")
    return prev, adm, exp

prev_df, adm_df, exp_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://www.aihw.gov.au/ResourcePackages/AIHW/assets/images/aihw-logo.svg",
        width=120,
    )
    st.title("Filters")

    selected_states = st.multiselect(
        "State / Territory",
        options=sorted(prev_df["state"].unique()),
        default=["NSW", "VIC", "QLD", "WA"],
    )
    year_range = st.slider(
        "Year range",
        min_value=int(prev_df["year"].min()),
        max_value=int(prev_df["year"].max()),
        value=(2015, 2023),
    )
    selected_sex = st.radio("Sex", ["All", "Male", "Female"])

    st.markdown("---")
    st.markdown(
        "**Data source:** Synthetic dataset based on "
        "[AIHW Chronic Disease reports](https://www.aihw.gov.au/reports-data/health-conditions-disability-deaths/chronic-disease) "
        "(2013–2023)"
    )

# ── Filter helpers ────────────────────────────────────────────────────────────
def filter_prev(df):
    mask = (
        df["state"].isin(selected_states)
        & df["year"].between(*year_range)
    )
    if selected_sex != "All":
        mask &= df["sex"] == selected_sex
    return df[mask]

def filter_state(df):
    return df[
        df["state"].isin(selected_states)
        & df["year"].between(*year_range)
    ]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 National Overview",
    "🗺️ State Comparison",
    "👥 Demographics",
    "🏥 Hospitals & Spending",
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — National Overview
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.header("Chronic Disease Trends in Australia")
    st.caption(
        "Tracking the prevalence of major chronic conditions across Australian "
        "states and territories, 2013–2023."
    )

    # KPI cards
    latest = prev_df[prev_df["year"] == prev_df["year"].max()]
    nat_avg = {col: latest[col].mean() for col in DISEASE_LABELS}
    oldest  = prev_df[prev_df["year"] == prev_df["year"].min()]
    nat_old = {col: oldest[col].mean() for col in DISEASE_LABELS}

    cols = st.columns(4)
    icons = ["🩺", "❤️", "🧠", "⚖️"]
    for i, (col_name, label) in enumerate(DISEASE_LABELS.items()):
        delta = nat_avg[col_name] - nat_old[col_name]
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{icons[i]} {label}</h3>
                <p>{nat_avg[col_name]:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(
                f"{'▲' if delta > 0 else '▼'} {abs(delta):.1f}pp since 2013"
            )

    st.markdown("---")

    # Trend line chart
    st.markdown('<p class="section-header">Prevalence trends over time</p>', unsafe_allow_html=True)
    disease_choice = st.selectbox(
        "Select condition",
        options=list(DISEASE_LABELS.keys()),
        format_func=lambda x: DISEASE_LABELS[x],
        key="trend_disease",
    )

    trend_df = (
        filter_prev(prev_df)
        .groupby(["year", "state"])[disease_choice]
        .mean()
        .reset_index()
    )
    fig_trend = px.line(
        trend_df, x="year", y=disease_choice, color="state",
        labels={"year": "Year", disease_choice: "Prevalence (%)", "state": "State"},
        markers=True,
        color_discrete_sequence=STATE_COLOURS,
    )
    fig_trend.update_layout(
        height=400, legend_title="State",
        hovermode="x unified", plot_bgcolor="white",
        yaxis=dict(gridcolor="#eee", title="Prevalence (%)"),
        xaxis=dict(gridcolor="#eee"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # All conditions area comparison (national average)
    st.markdown('<p class="section-header">All conditions — national average trend</p>', unsafe_allow_html=True)
    all_trend = (
        filter_prev(prev_df)
        .groupby("year")[list(DISEASE_LABELS.keys())]
        .mean()
        .reset_index()
        .melt(id_vars="year", var_name="condition", value_name="prevalence_pct")
    )
    all_trend["condition"] = all_trend["condition"].map(DISEASE_LABELS)

    fig_all = px.area(
        all_trend, x="year", y="prevalence_pct", color="condition",
        labels={"year": "Year", "prevalence_pct": "Prevalence (%)", "condition": "Condition"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_all.update_layout(
        height=350, plot_bgcolor="white",
        yaxis=dict(gridcolor="#eee"), xaxis=dict(gridcolor="#eee"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_all, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — State Comparison
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.header("State & Territory Comparison")

    compare_year = st.slider(
        "Select year for snapshot",
        min_value=int(prev_df["year"].min()),
        max_value=int(prev_df["year"].max()),
        value=2022,
        key="state_year",
    )

    snap = (
        prev_df[prev_df["year"] == compare_year]
        .groupby("state")[list(DISEASE_LABELS.keys())]
        .mean()
        .reset_index()
    )

    col_a, col_b = st.columns(2)
    with col_a:
        disease_bar = st.selectbox(
            "Condition to compare",
            options=list(DISEASE_LABELS.keys()),
            format_func=lambda x: DISEASE_LABELS[x],
            key="bar_disease",
        )
        fig_bar = px.bar(
            snap.sort_values(disease_bar, ascending=True),
            x=disease_bar, y="state", orientation="h",
            color=disease_bar,
            color_continuous_scale="Blues",
            labels={disease_bar: "Prevalence (%)", "state": ""},
            title=f"{DISEASE_LABELS[disease_bar]} prevalence by state ({compare_year})",
        )
        fig_bar.update_layout(height=380, plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        # Radar / spider chart for multi-disease comparison
        snap_norm = snap.copy()
        for col in DISEASE_LABELS:
            snap_norm[col] = (snap_norm[col] - snap_norm[col].min()) / (
                snap_norm[col].max() - snap_norm[col].min() + 1e-9
            )

        categories = list(DISEASE_LABELS.values())
        fig_radar = go.Figure()
        for _, row in snap_norm[snap_norm["state"].isin(selected_states)].iterrows():
            vals = [row[c] for c in DISEASE_LABELS] + [row[list(DISEASE_LABELS.keys())[0]]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["state"],
                opacity=0.6,
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title=f"Relative disease burden by state ({compare_year})",
            height=380,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Heatmap
    st.markdown('<p class="section-header">Disease burden heatmap (all states, selected year)</p>', unsafe_allow_html=True)
    heat_data = snap.set_index("state")[list(DISEASE_LABELS.keys())]
    heat_data.columns = [DISEASE_LABELS[c] for c in heat_data.columns]
    fig_heat = px.imshow(
        heat_data,
        color_continuous_scale="RdYlGn_r",
        aspect="auto",
        labels=dict(color="Prevalence (%)"),
        title=f"Chronic disease prevalence heatmap — {compare_year}",
    )
    fig_heat.update_layout(height=350)
    st.plotly_chart(fig_heat, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — Demographics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.header("Age & Sex Demographics")

    demo_df = filter_prev(prev_df)
    disease_demo = st.selectbox(
        "Condition",
        options=list(DISEASE_LABELS.keys()),
        format_func=lambda x: DISEASE_LABELS[x],
        key="demo_disease",
    )
    demo_year = st.slider(
        "Year", int(prev_df["year"].min()), int(prev_df["year"].max()),
        value=2022, key="demo_year"
    )

    age_sex = (
        prev_df[prev_df["year"] == demo_year]
        .groupby(["age_group", "sex"])[disease_demo]
        .mean()
        .reset_index()
    )

    col1, col2 = st.columns(2)
    with col1:
        # Grouped bar: age × sex
        fig_demo = px.bar(
            age_sex, x="age_group", y=disease_demo, color="sex",
            barmode="group",
            color_discrete_map={"Male": "#4c9be8", "Female": "#e87c4c"},
            labels={"age_group": "Age group", disease_demo: "Prevalence (%)", "sex": "Sex"},
            title=f"{DISEASE_LABELS[disease_demo]} by age & sex ({demo_year})",
            category_orders={"age_group": ["0-14","15-24","25-44","45-64","65-74","75+"]},
        )
        fig_demo.update_layout(height=380, plot_bgcolor="white",
                               yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig_demo, use_container_width=True)

    with col2:
        # Population pyramid
        pyr = (
            prev_df[prev_df["year"] == demo_year]
            .groupby(["age_group", "sex"])["population_estimate"]
            .sum()
            .reset_index()
        )
        pyr["pop_display"] = pyr.apply(
            lambda r: -r["population_estimate"] if r["sex"] == "Male"
            else r["population_estimate"], axis=1
        )
        fig_pyr = go.Figure()
        for sex, colour in [("Male", "#4c9be8"), ("Female", "#e87c4c")]:
            sub = pyr[pyr["sex"] == sex]
            fig_pyr.add_trace(go.Bar(
                y=sub["age_group"], x=sub["pop_display"],
                orientation="h", name=sex,
                marker_color=colour,
            ))
        fig_pyr.update_layout(
            title=f"Population pyramid — selected states ({demo_year})",
            barmode="overlay",
            xaxis=dict(title="Population",
                       tickvals=[-2e6, -1e6, 0, 1e6, 2e6],
                       ticktext=["2M", "1M", "0", "1M", "2M"]),
            yaxis=dict(
                title="Age group",
                categoryorder="array",
                categoryarray=["0-14","15-24","25-44","45-64","65-74","75+"],
            ),
            height=380, plot_bgcolor="white",
        )
        st.plotly_chart(fig_pyr, use_container_width=True)

    # Age trend over time
    st.markdown('<p class="section-header">How age-specific prevalence changed over time</p>', unsafe_allow_html=True)
    age_time = (
        prev_df[prev_df["state"].isin(selected_states)]
        .groupby(["year", "age_group"])[disease_demo]
        .mean()
        .reset_index()
    )
    fig_age_time = px.line(
        age_time, x="year", y=disease_demo, color="age_group",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={"year": "Year", disease_demo: "Prevalence (%)", "age_group": "Age group"},
        category_orders={"age_group": ["0-14","15-24","25-44","45-64","65-74","75+"]},
        title=f"{DISEASE_LABELS[disease_demo]} trend by age group",
    )
    fig_age_time.update_layout(
        height=380, hovermode="x unified", plot_bgcolor="white",
        yaxis=dict(gridcolor="#eee"), xaxis=dict(gridcolor="#eee"),
    )
    st.plotly_chart(fig_age_time, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — Hospitals & Spending
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.header("Hospital Activity & Health Expenditure")

    adm_f = filter_state(adm_df)
    exp_f = filter_state(exp_df)

    # Hospital KPI row
    latest_adm = adm_df[adm_df["year"] == adm_df["year"].max()]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total admissions (2023, national)",
                  f"{latest_adm['total_admissions'].sum():,.0f}")
    with c2:
        st.metric("Avg length of stay",
                  f"{latest_adm['avg_length_of_stay_days'].mean():.1f} days",
                  delta=f"{latest_adm['avg_length_of_stay_days'].mean() - adm_df[adm_df['year']==2013]['avg_length_of_stay_days'].mean():.1f} vs 2013")
    with c3:
        st.metric("Emergency admissions",
                  f"{latest_adm['emergency_admissions_pct'].mean():.1f}%")
    with c4:
        latest_exp = exp_df[exp_df["year"] == exp_df["year"].max()]
        st.metric("Per capita spend (national avg)",
                  f"${latest_exp['per_capita_expenditure_aud'].mean():,.0f} AUD")

    st.markdown("---")

    col_hosp, col_exp = st.columns(2)
    with col_hosp:
        fig_adm = px.bar(
            adm_f.groupby(["year", "state"])["total_admissions"].sum().reset_index(),
            x="year", y="total_admissions", color="state",
            labels={"year": "Year", "total_admissions": "Admissions", "state": "State"},
            title="Total hospital admissions by state",
            color_discrete_sequence=STATE_COLOURS,
        )
        fig_adm.update_layout(height=350, plot_bgcolor="white",
                              yaxis=dict(gridcolor="#eee"), barmode="stack")
        st.plotly_chart(fig_adm, use_container_width=True)

        # ALOS trend
        fig_alos = px.line(
            adm_f, x="year", y="avg_length_of_stay_days", color="state",
            markers=True,
            labels={"year": "Year", "avg_length_of_stay_days": "ALOS (days)"},
            title="Average length of stay trend",
            color_discrete_sequence=STATE_COLOURS,
        )
        fig_alos.update_layout(height=300, plot_bgcolor="white",
                               yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig_alos, use_container_width=True)

    with col_exp:
        # Expenditure over time
        fig_exp = px.line(
            exp_f, x="year", y="per_capita_expenditure_aud", color="state",
            markers=True,
            labels={"year": "Year", "per_capita_expenditure_aud": "Per capita spend (AUD)"},
            title="Per capita health expenditure",
            color_discrete_sequence=STATE_COLOURS,
        )
        fig_exp.update_layout(height=350, plot_bgcolor="white",
                              yaxis=dict(gridcolor="#eee"))
        st.plotly_chart(fig_exp, use_container_width=True)

        # Spending breakdown pie (latest year, selected states avg)
        latest_cat = exp_df[
            exp_df["year"] == exp_df["year"].max()
        ][["hospitals_pct", "primary_care_pct", "medications_pct",
           "aged_care_pct", "other_pct"]].mean()

        fig_pie = px.pie(
            names=["Hospitals", "Primary Care", "Medications", "Aged Care", "Other"],
            values=latest_cat.values,
            title="Health expenditure breakdown (2023 est.)",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Diagnosis mix bar
    st.markdown('<p class="section-header">Hospital admissions by diagnosis category</p>', unsafe_allow_html=True)
    diag_cols = [
        "cardiovascular_admissions_pct", "mental_health_admissions_pct",
        "diabetes_related_admissions_pct", "respiratory_admissions_pct",
        "cancer_admissions_pct",
    ]
    diag_labels = {
        "cardiovascular_admissions_pct": "Cardiovascular",
        "mental_health_admissions_pct": "Mental Health",
        "diabetes_related_admissions_pct": "Diabetes-related",
        "respiratory_admissions_pct": "Respiratory",
        "cancer_admissions_pct": "Cancer",
    }
    diag_trend = (
        adm_f.groupby("year")[diag_cols].mean().reset_index()
        .melt(id_vars="year", var_name="diagnosis", value_name="pct")
    )
    diag_trend["diagnosis"] = diag_trend["diagnosis"].map(diag_labels)
    fig_diag = px.bar(
        diag_trend, x="year", y="pct", color="diagnosis",
        labels={"year": "Year", "pct": "% of admissions", "diagnosis": "Diagnosis"},
        title="Admission diagnosis mix over time (selected states)",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig_diag.update_layout(height=380, plot_bgcolor="white",
                           yaxis=dict(gridcolor="#eee"), barmode="stack")
    st.plotly_chart(fig_diag, use_container_width=True)
