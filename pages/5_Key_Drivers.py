import streamlit as st
import plotly.graph_objects as go

from utils.shap_loader import load_shap
from utils.driver_categories import classify_driver

from config.theme import (

    PRIMARY_BLUE,
    SECONDARY_ORANGE,
    SUCCESS_GREEN,
    WARNING_ORANGE,
    DANGER_RED,
    LIGHT_GREY

)

# ==========================================================
# CATEGORY COLOURS
# ==========================================================

CATEGORY_COLOURS = {

    "Climate & Environment": SUCCESS_GREEN,
    "Market": WARNING_ORANGE,
    "Conflict": DANGER_RED,
    "Livelihood": PRIMARY_BLUE,
    "Spatial / Temporal": "#8E44AD",
    "Other": LIGHT_GREY

}

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🔍 Driver Analysis (SHAP)")

st.markdown(
    """
    Explore the most influential predictors driving the
    machine learning forecasts for each food security outcome.
    """
)

# ==========================================================
# USER SELECTION
# ==========================================================

indicator = st.selectbox(

    "Select Outcome Indicator",

    [

        "FCS",
        "rCSI",
        "HHS"

    ]

)

# ==========================================================
# LOAD SHAP
# ==========================================================

df = load_shap(indicator)

df["Category"] = df["Feature"].apply(

    classify_driver

)

# Keep only Top 30

df = df.head(30)

# ==========================================================
# TOP 3 DRIVER CARDS
# ==========================================================

st.markdown("---")

st.subheader("🏆 Most Influential Drivers")

c1, c2, c3 = st.columns(3)

for column, (_, row) in zip(

    [c1, c2, c3],

    df.head(3).iterrows()

):

    column.metric(

        label=row["Feature"],

        value=f"{row['Mean_Abs_SHAP']:.2f}"

    )

st.markdown("---")

# ==========================================================
# SHAP IMPORTANCE CHART
# ==========================================================

st.subheader("Top 30 Driver Importance")

plot_df = df.iloc[::-1]

bar_colours = [

    CATEGORY_COLOURS.get(

        category,

        LIGHT_GREY

    )

    for category in plot_df["Category"]

]

fig = go.Figure()

fig.add_trace(

    go.Bar(

        x=plot_df["Mean_Abs_SHAP"],

        y=plot_df["Feature"],

        orientation="h",

        marker=dict(

            color=bar_colours

        ),

        text=[

            f"{x:.2f}"

            for x in plot_df["Mean_Abs_SHAP"]

        ],

        textposition="outside",

        hovertemplate=(

            "<b>%{y}</b><br>"

            "Importance: %{x:.2f}"

            "<extra></extra>"

        )

    )

)

fig.update_layout(

    template="plotly_white",

    height=850,

    margin=dict(

        l=20,

        r=20,

        t=60,

        b=20

    ),

    title=dict(

        text=f"Top 30 Drivers for {indicator}",

        x=0.5,

        font=dict(

            size=22

        )

    ),

    xaxis=dict(

        title="Mean Absolute SHAP Value",

        showgrid=True,

        gridcolor=LIGHT_GREY

    ),

    yaxis=dict(

        title="",

        showgrid=False

    ),

    showlegend=False

)

st.plotly_chart(

    fig,

    use_container_width=True,

    theme=None,

    config={

        "displaylogo": False,

        "responsive": True,

        "toImageButtonOptions": {

            "format": "png",

            "filename": f"{indicator}_top_drivers",

            "scale": 2

        }

    }

)


# ==========================================================
# DRIVER CATEGORY CONTRIBUTION
# ==========================================================

st.markdown("---")

st.subheader("📊 Driver Category Contribution")

category_summary = (

    df

    .groupby(

        "Category",
        as_index=False

    )["Mean_Abs_SHAP"]

    .sum()

)

category_summary = category_summary.sort_values(

    "Mean_Abs_SHAP",

    ascending=False

)

category_plot = category_summary.iloc[::-1]

category_colours = [

    CATEGORY_COLOURS.get(

        category,

        LIGHT_GREY

    )

    for category in category_plot["Category"]

]

fig_category = go.Figure()

fig_category.add_trace(

    go.Bar(

        x=category_plot["Mean_Abs_SHAP"],

        y=category_plot["Category"],

        orientation="h",

        marker=dict(

            color=category_colours

        ),

        text=[

            f"{x:.2f}"

            for x in category_plot["Mean_Abs_SHAP"]

        ],

        textposition="outside",

        hovertemplate=(

            "<b>%{y}</b><br>"

            "Total SHAP: %{x:.2f}"

            "<extra></extra>"

        )

    )

)

fig_category.update_layout(

    template="plotly_white",

    height=420,

    margin=dict(

        l=20,

        r=20,

        t=60,

        b=20

    ),

    title=dict(

        text="Contribution by Driver Category",

        x=0.5,

        font=dict(

            size=20

        )

    ),

    xaxis=dict(

        title="Total Mean Absolute SHAP",

        showgrid=True,

        gridcolor=LIGHT_GREY

    ),

    yaxis=dict(

        title="",

        showgrid=False

    ),

    showlegend=False

)

st.plotly_chart(

    fig_category,

    use_container_width=True,

    theme=None,

    config={

        "displaylogo": False,

        "responsive": True

    }

)

# ==========================================================
# TOP 10 DRIVER TABLE
# ==========================================================

st.markdown("---")

st.subheader("📋 Top 10 Most Influential Drivers")

top10 = df.head(10).copy()

top10.insert(

    0,

    "Rank",

    range(1, len(top10) + 1)

)

top10["Mean_Abs_SHAP"] = top10["Mean_Abs_SHAP"].round(3)

top10 = top10.rename(

    columns={

        "Feature": "Driver",

        "Mean_Abs_SHAP": "Importance",

        "Category": "Category"

    }

)

st.dataframe(

    top10,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# DOWNLOAD SHAP RESULTS
# ==========================================================

st.download_button(

    label="📥 Download Driver Rankings",

    data=top10.to_csv(index=False),

    file_name=f"{indicator.lower()}_driver_rankings.csv",

    mime="text/csv"

)

# ==========================================================
# QUICK SUMMARY
# ==========================================================

st.markdown("---")

c1, c2, c3 = st.columns(3)

c1.metric(

    "Drivers Displayed",

    len(df)

)

c2.metric(

    "Driver Categories",

    category_summary.shape[0]

)

c3.metric(

    "Top Driver",

    df.iloc[0]["Feature"]

)


# ==========================================================
# DECISION INSIGHT
# ==========================================================

st.markdown("---")

st.subheader("🧠 Decision Insight")

category_rank = category_summary.sort_values(

    "Mean_Abs_SHAP",

    ascending=False

).reset_index(drop=True)

dominant = category_rank.loc[0, "Category"]
second = category_rank.loc[1, "Category"]

st.info(

    f"""
The **{indicator}** prediction is primarily influenced by **{dominant.lower()}**
factors, followed by **{second.lower()}**.

This indicates that changes within these two domains are expected to have
the greatest influence on model predictions and should therefore receive
priority during routine food security monitoring.
"""
)

# ==========================================================
# KEY MONITORING PRIORITIES
# ==========================================================

st.markdown("---")

st.subheader("📌 Key Monitoring Priorities")

monitoring = {

    "Climate & Environment": [

        "Rainfall anomalies",

        "Vegetation conditions (NDVI)",

        "River water levels"

    ],

    "Market": [

        "Cost of Minimum Basket (CMB)",

        "Goat prices",

        "Rice prices",

        "Sorghum prices",

        "Water prices"

    ],

    "Conflict": [

        "Conflict incidents",

        "Conflict fatalities"

    ],

    "Livelihood": [

        "Household debt",

        "Herd size",

        "Crop production"

    ],

    "Spatial / Temporal": [

        "Livelihood zone characteristics",

        "Livelihood system",

        "Seasonal monitoring",

        "Temporal trends"

    ]

}

for category in [dominant, second]:

    st.markdown(

        f"### {category}"

    )

    for item in monitoring.get(category, []):

        st.markdown(

            f"- {item}"

        )

# ==========================================================
# OPERATIONAL RECOMMENDATIONS
# ==========================================================

st.markdown("---")

st.subheader("⚠ Operational Recommendations")

if indicator == "FCS":

    recommendations = [

        "Monitor changes in food consumption patterns across livelihood zones.",

        "Strengthen surveillance of market prices and household purchasing power.",

        "Closely monitor rainfall and vegetation conditions before the next assessment.",

        "Investigate areas showing persistent deterioration in food consumption."

    ]

elif indicator == "rCSI":

    recommendations = [

        "Monitor household reliance on food-based coping strategies.",

        "Increase market surveillance where staple food prices continue to rise.",

        "Track conflict-related disruptions affecting household access to food.",

        "Consider early response interventions if coping strategies continue increasing."

    ]

else:

    recommendations = [

        "Closely monitor households exhibiting increasing hunger levels.",

        "Strengthen nutrition and food assistance surveillance.",

        "Monitor climatic and market conditions that may worsen household hunger.",

        "Prioritise areas showing persistent increases in severe hunger."

    ]

for recommendation in recommendations:

    st.markdown(

        f"✅ {recommendation}"

    )

# ==========================================================
# METHODOLOGY NOTE
# ==========================================================

st.markdown("---")

with st.expander("ℹ About this Analysis"):

    st.markdown(

        """
        **Key Driver Analysis** is based on SHAP (SHapley Additive exPlanations)
        values computed from the final XGBoost models developed in this study.

        SHAP values quantify the relative contribution of each predictor variable
        to the model's predictions. Higher Mean Absolute SHAP values indicate
        greater influence on the predicted food security outcome.

        Driver categories are grouped into:

        - Climate & Environment
        - Market
        - Conflict
        - Livelihood
        - Spatial & Temporal

        These groupings correspond to the conceptual framework adopted in this
        study and facilitate interpretation for operational food security
        monitoring and decision-making.
        """

    )

# ==========================================================
# PLATFORM NOTE
# ==========================================================

st.markdown("---")

st.info(
"""
**Platform Note**

This page explains how the trained XGBoost models generate food security
forecasts by identifying the variables that contribute most strongly to model
predictions.

Driver importance is derived from SHAP (SHapley Additive exPlanations) values
computed during model development and therefore remains constant unless the
models are retrained.

To generate forecasts for future food security conditions, use the
**Forecasting & Risk Assessment** page. To evaluate the effects of changing
future assumptions, use the **Scenario Analysis** page.
"""
)