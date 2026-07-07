import streamlit as st
import pandas as pd

from utils.data_loader import load_data

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📊 Dashboard")

st.markdown(
    """
    Executive summary of current food security conditions across
    Somalia. This dashboard provides a consolidated overview of
    the latest survey results, machine learning forecasts, key
    risk indicators and dominant drivers supporting operational
    decision-making.
    """
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# LATEST SURVEY
# ==========================================================

latest = (

    df

    .sort_values(

        ["year", "season_order"]

    )

    .iloc[-1]

)

latest_year = latest["year"]

latest_season = latest["season"]

latest_round = f"{latest_year} {latest_season}"

number_zones = df["livelihood_zone_corrected"].nunique()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.markdown("---")

st.header("Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Latest Survey",

    latest_round

)

c2.metric(

    "Livelihood Zones",

    number_zones

)

c3.metric(

    "Indicators",

    "3"

)

c4.metric(

    "Models",

    "XGBoost"

)

# ==========================================================
# NATIONAL OUTCOMES
# ==========================================================

st.markdown("---")

st.header("Latest National Situation")

latest_round_df = df[

    (df["year"] == latest_year)

    &

    (df["season"] == latest_season)

]

national_fcs = latest_round_df["fcs"].mean()

national_rcsi = latest_round_df["rcsi"].mean()

national_hhs = latest_round_df["hhs"].mean()

k1, k2, k3 = st.columns(3)

k1.metric(

    "Average FCS",

    f"{national_fcs:.2f}"

)

k2.metric(

    "Average rCSI",

    f"{national_rcsi:.2f}"

)

k3.metric(

    "Average HHS",

    f"{national_hhs:.2f}"

)

import plotly.graph_objects as go

# ==========================================================
# NATIONAL RISK ASSESSMENT
# ==========================================================

st.markdown("---")

st.header("National Food Security Outlook")

# ----------------------------------------------------------
# OVERALL RISK
# ----------------------------------------------------------

if national_fcs >= 42:

    overall_risk = "🟢 LOW"

    banner_colour = "#27AE60"

elif national_fcs >= 28:

    overall_risk = "🟡 MODERATE"

    banner_colour = "#F39C12"

else:

    overall_risk = "🔴 HIGH"

    banner_colour = "#E74C3C"

st.markdown(

    f"""

<div style="background-color:{banner_colour};
padding:18px;
border-radius:10px;
text-align:center;
font-size:28px;
font-weight:bold;
color:white;">

Current National Outlook<br>

{overall_risk}

</div>

""",

    unsafe_allow_html=True

)

# ==========================================================
# NATIONAL TREND
# ==========================================================

st.markdown("---")

st.header("National Trend Snapshot")

trend = (

    df

    .groupby(

        [

            "year",

            "season",

            "season_order"

        ]

    )[

        [

            "fcs",

            "rcsi",

            "hhs"

        ]

    ]

    .mean()

    .reset_index()

)

trend = trend.sort_values(

    [

        "year",

        "season_order"

    ]

)

trend["Period"] = (

    trend["year"].astype(str)

    + " "

    + trend["season"]

)

trend = trend.tail(6)

indicator = st.selectbox(

    "Trend Indicator",

    [

        "fcs",

        "rcsi",

        "hhs"

    ],

    key="dashboard_indicator"

)

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=trend["Period"],

        y=trend[indicator],

        mode="lines+markers",

        line=dict(

            width=4

        ),

        name=indicator.upper()

    )

)

fig.update_layout(

    height=420,

    title=f"National {indicator.upper()} Trend",

    xaxis_title="Survey Round",

    yaxis_title=indicator.upper(),

    hovermode="x unified"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# QUICK NATIONAL STATISTICS
# ==========================================================

st.markdown("---")

st.header("National Summary")

c1, c2, c3 = st.columns(3)

c1.metric(

    "Highest Average FCS",

    f"{trend['fcs'].max():.1f}"

)

c2.metric(

    "Highest Average rCSI",

    f"{trend['rcsi'].max():.1f}"

)

c3.metric(

    "Highest Average HHS",

    f"{trend['hhs'].max():.2f}"

)


# ==========================================================
# EXECUTIVE INTELLIGENCE
# ==========================================================

st.markdown("---")

st.header("🧠 Executive Intelligence")

# ----------------------------------------------------------
# LOAD SHAP RESULTS
# ----------------------------------------------------------

from utils.shap_loader import load_shap
from utils.driver_categories import classify_driver

shap_df = load_shap("FCS")

shap_df["Category"] = shap_df["Feature"].apply(
    classify_driver
)

category_summary = (

    shap_df

    .groupby("Category")["Mean_Abs_SHAP"]

    .sum()

    .sort_values(ascending=False)

)

dominant = category_summary.index[0]
second = category_summary.index[1]

top_driver = shap_df.iloc[0]["Feature"]

# ----------------------------------------------------------
# EXECUTIVE INSIGHT
# ----------------------------------------------------------

st.subheader("Executive Insight")

st.info(

f"""

### National Situation

The latest national monitoring results suggest that food security
conditions remain **{overall_risk.lower()}** based on the most
recent survey observations.

Machine learning analysis indicates that **{dominant.lower()}**
drivers currently exert the greatest influence on predicted food
security outcomes, followed by **{second.lower()}** conditions.

Across the country, **{top_driver.replace('_',' ').title()}**
emerged as the single most influential predictor within the
XGBoost forecasting models.

"""

)

# ==========================================================
# EARLY WARNING PRIORITIES
# ==========================================================

st.markdown("---")

st.subheader("Early Warning Priorities")

priority_table = pd.DataFrame({

    "Priority":

    [

        "Environmental Monitoring",

        "Market Monitoring",

        "Conflict Monitoring",

        "Livelihood Monitoring"

    ],

    "Current Status":

    [

        "High",

        "Moderate",

        "Moderate",

        "High"

    ],

    "Recommended Action":

    [

        "Monitor rainfall, NDVI and seasonal performance.",

        "Track food prices and purchasing power.",

        "Monitor conflict incidents and fatalities.",

        "Assess debt, herd size and crop production."

    ]

})

st.dataframe(

    priority_table,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# TOP FIVE DRIVERS
# ==========================================================

st.markdown("---")

st.subheader("Top Five National Drivers")

top5 = shap_df.head(5).copy()

st.dataframe(

    top5,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# RECOMMENDED ACTIONS
# ==========================================================

st.markdown("---")

st.subheader("Recommended Strategic Actions")

recommendations = [

    "🌧 Continue close monitoring of rainfall and vegetation conditions.",

    "💰 Strengthen market surveillance, particularly staple food and livestock prices.",

    "⚔ Maintain routine monitoring of conflict incidents and displacement.",

    "🐄 Monitor livelihood resilience indicators including debt, herd size and crop production.",

    "📈 Update forecasts as new monthly data become available."

]

for recommendation in recommendations:

    st.markdown(recommendation)

# ==========================================================
# NATIONAL DECISION SUPPORT SUMMARY
# ==========================================================

st.markdown("---")

st.header("🎯 National Decision Support Summary")

# ----------------------------------------------------------
# RISK DESCRIPTION
# ----------------------------------------------------------

if "LOW" in overall_risk:

    outlook = "relatively stable"

elif "MODERATE" in overall_risk:

    outlook = "moderately stressed"

else:

    outlook = "highly stressed"

# ----------------------------------------------------------
# DRIVER DESCRIPTION
# ----------------------------------------------------------

driver_messages = {

    "Environmental":
        "Vegetation conditions, rainfall performance and environmental variability continue to exert the strongest influence on predicted food security outcomes.",

    "Market":
        "Food prices and household purchasing power remain important determinants of food security conditions.",

    "Conflict":
        "Conflict-related disruptions continue to influence food access and livelihood stability in affected areas.",

    "Livelihood":
        "Household livelihood assets, production and resilience indicators remain key determinants of food security outcomes.",

    "Spatial":
        "Geographical differences between livelihood zones continue to explain important variations in food security outcomes.",

    "Temporal":
        "Seasonality and inter-annual variability continue to influence predicted food security conditions."

}

primary_driver = driver_messages.get(

    dominant,

    "Multiple factors contribute to the observed food security situation."

)

secondary_driver = driver_messages.get(

    second,

    "Additional contextual factors remain important."

)

# ==========================================================
# SUMMARY
# ==========================================================

summary = f"""

The latest national assessment ({latest_round}) indicates that Somalia's
food security situation is currently <b>{outlook}</b>, based on the
combined evidence from historical monitoring and machine learning
forecasting.

The XGBoost forecasting models identify <b>{dominant.lower()}</b>
conditions as the primary drivers of predicted food security outcomes,
with **{second.lower()}** factors representing the next most influential
group.

At the individual predictor level, <b>{top_driver.replace('_',' ').title()}</b>
emerged as the strongest determinant of food security within the national
forecasting models.

{primary_driver}

{secondary_driver}

Overall, current evidence suggests that maintaining continuous monitoring
of environmental conditions, market dynamics, household livelihood
indicators and localized conflict remains essential for supporting timely
early warning and evidence-based food security decision-making before the
next assessment cycle.

"""

# ==========================================================
# EXECUTIVE BRIEFING NOTE
# ==========================================================

st.markdown(
    f"""
<div style="
background:#1F2937;
padding:28px;
border-left:8px solid {banner_colour};
border-radius:14px;
box-shadow:0 4px 12px rgba(0,0,0,0.35);
color:#F8F9FA;
">

<h2 style="
margin-top:0;
color:#FFFFFF;
font-size:30px;
">
🎯 National Situation Brief
</h2>

<p style="
font-size:17px;
line-height:1.9;
text-align:justify;
color:#E5E7EB;
">

{summary}

</p>

<hr>

<hr style="border:1px solid #374151;">

<table style="width:100%;color:#F9FAFB;font-size:15px;">

<tr>
<td><b>Assessment Round</b></td>
<td>{latest_round}</td>
</tr>

<tr>
<td><b>National Outlook</b></td>
<td>{overall_risk}</td>
</tr>

<tr>
<td><b>Primary Driver</b></td>
<td>{dominant}</td>
</tr>

<tr>
<td><b>Top Predictor</b></td>
<td>{top_driver.replace('_',' ').title()}</td>
</tr>

</table>

</div>
""",
    unsafe_allow_html=True
)