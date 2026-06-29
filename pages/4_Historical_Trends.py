import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import load_data
from config.theme import (
    PRIMARY_BLUE,
    SECONDARY_ORANGE,
    SUCCESS_GREEN,
    WARNING_ORANGE,
    DANGER_RED,
    LIGHT_GREY
)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📊 Historical Monitoring")

st.markdown(
    """
    Monitor historical food security outcome indicators across
    Somalia's livelihood zones and obtain automated trend insights.
    """
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# USER SELECTIONS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    indicator = st.selectbox(

        "Select Indicator",

        [

            "fcs",
            "rcsi",
            "hhs"

        ]

    )

with col2:

    zone = st.selectbox(

        "Select Livelihood Zone",

        sorted(df["livelihood_zone_corrected"].unique())

    )

# ==========================================================
# FILTER DATA
# ==========================================================

filtered = df[

    df["livelihood_zone_corrected"] == zone

].copy()

filtered = filtered.sort_values(

    ["year", "season_order"]

)

# ==========================================================
# SUMMARY STATISTICS
# ==========================================================

latest = filtered[indicator].iloc[-1]
average = filtered[indicator].mean()
minimum = filtered[indicator].min()
maximum = filtered[indicator].max()

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Latest", f"{latest:.2f}")
c2.metric("Average", f"{average:.2f}")
c3.metric("Minimum", f"{minimum:.2f}")
c4.metric("Maximum", f"{maximum:.2f}")

# ==========================================================
# HISTORICAL TREND
# ==========================================================

st.markdown("---")

fig = go.Figure()

# ----------------------------------------------------------
# CONTINUOUS SEASONAL TIME SERIES
# ----------------------------------------------------------

fig.add_trace(

    go.Scatter(

        x=filtered["Period"],

        y=filtered[indicator],

        mode="lines+markers",

        name="Observed",

        line=dict(

            color=PRIMARY_BLUE,
            width=3,
            shape="spline"

        ),

        marker=dict(

            size=9,

            color=[

                PRIMARY_BLUE if s == "Gu"
                else SECONDARY_ORANGE

                for s in filtered["season"]

            ],

            symbol=[

                "circle" if s == "Gu"
                else "diamond"

                for s in filtered["season"]

            ],

            line=dict(

                color="white",
                width=1

            )

        ),

        text=filtered["season"],

        hovertemplate=(

            "<b>%{x}</b><br>"
            "Season: %{text}<br>"
            f"{indicator.upper()}: %{{y:.2f}}"
            "<extra></extra>"

        )

    )

)

# ----------------------------------------------------------
# REFERENCE THRESHOLDS
# ----------------------------------------------------------

if indicator == "fcs":

    # Poor Zone
    fig.add_hrect(
        y0=0,
        y1=28,
        fillcolor="rgba(220,53,69,0.12)",
        line_width=0
    )

    # Borderline Zone
    fig.add_hrect(
        y0=28,
        y1=42,
        fillcolor="rgba(255,193,7,0.12)",
        line_width=0
    )

    # Acceptable Zone
    fig.add_hrect(
        y0=42,
        y1=max(filtered[indicator].max()*1.1, 60),
        fillcolor="rgba(40,167,69,0.10)",
        line_width=0
    )

    fig.add_hline(
        y=28,
        line_dash="dot",
        line_color=DANGER_RED,
        annotation_text="Poor"
    )

    fig.add_hline(
        y=42,
        line_dash="dot",
        line_color=SUCCESS_GREEN,
        annotation_text="Acceptable"
    )

elif indicator == "rcsi":

    fig.add_hrect(
        y0=0,
        y1=4,
        fillcolor="rgba(40,167,69,0.10)",
        line_width=0
    )

    fig.add_hrect(
        y0=4,
        y1=19,
        fillcolor="rgba(255,193,7,0.12)",
        line_width=0
    )

    fig.add_hrect(
        y0=19,
        y1=max(filtered[indicator].max()*1.1,25),
        fillcolor="rgba(220,53,69,0.12)",
        line_width=0
    )

    fig.add_hline(
        y=4,
        line_dash="dot",
        line_color=WARNING_ORANGE,
        annotation_text="Stress"
    )

    fig.add_hline(
        y=19,
        line_dash="dot",
        line_color=DANGER_RED,
        annotation_text="Crisis"
    )

elif indicator == "hhs":

    fig.add_hrect(
        y0=0,
        y1=1,
        fillcolor="rgba(40,167,69,0.10)",
        line_width=0
    )

    fig.add_hrect(
        y0=1,
        y1=4,
        fillcolor="rgba(255,193,7,0.12)",
        line_width=0
    )

    fig.add_hrect(
        y0=4,
        y1=max(filtered[indicator].max()*1.1,6),
        fillcolor="rgba(220,53,69,0.12)",
        line_width=0
    )

    fig.add_hline(
        y=1,
        line_dash="dot",
        line_color=WARNING_ORANGE,
        annotation_text="Moderate Hunger"
    )

    fig.add_hline(
        y=4,
        line_dash="dot",
        line_color=DANGER_RED,
        annotation_text="Severe Hunger"
    )

# ----------------------------------------------------------
# LAYOUT
# ----------------------------------------------------------

fig.update_layout(

    title=dict(

        text=f"{indicator.upper()} Historical Trend",

        x=0.5,

        font=dict(
            size=22
        )

    ),

    template="plotly_white",

    height=560,

    hovermode="x unified",

    showlegend=False,

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    ),

    xaxis=dict(

        title="Survey Period",

        showgrid=False,

        tickangle=-45

    ),

    yaxis=dict(

        title=indicator.upper(),

        showgrid=True,

        gridcolor=LIGHT_GREY,

        zeroline=False

    )

)

st.plotly_chart(

    fig,

    use_container_width=True,

    theme=None,

    config={

        "displaylogo": False,

        "responsive": True,

        "scrollZoom": True,

        "toImageButtonOptions": {

            "format": "png",

            "filename": f"{zone}_{indicator}_trend",

            "height": 650,

            "width": 1300,

            "scale": 2

        }

    }

)

# ==========================================================
# MONITORING INSIGHTS
# ==========================================================

st.markdown("---")

st.subheader("📌 Monitoring Insights")

recent = filtered.tail(4)

change = recent[indicator].iloc[-1] - recent[indicator].iloc[0]

if indicator == "fcs":

    if change > 2:

        interpretation = (
            "Food Consumption Score has improved over the most recent seasons, "
            "suggesting improving household food consumption."
        )

    elif change < -2:

        interpretation = (
            "Food Consumption Score has declined during recent seasons, "
            "indicating deteriorating food consumption that may require attention."
        )

    else:

        interpretation = (
            "Food Consumption Score has remained relatively stable over recent seasons."
        )

elif indicator == "rcsi":

    if change > 2:

        interpretation = (
            "Households appear to be relying increasingly on food-based coping strategies, "
            "suggesting worsening food security conditions."
        )

    elif change < -2:

        interpretation = (
            "Reduced Coping Strategy Index has declined, indicating reduced reliance on coping strategies."
        )

    else:

        interpretation = (
            "Coping behaviour has remained relatively stable across recent seasons."
        )

else:

    if change > 0.5:

        interpretation = (
            "Household Hunger Scale has increased in recent seasons, suggesting worsening household hunger."
        )

    elif change < -0.5:

        interpretation = (
            "Household Hunger Scale has declined, indicating improvements in household hunger."
        )

    else:

        interpretation = (
            "Household Hunger Scale has remained relatively stable."
        )

st.info(interpretation)

# ==========================================================
# HISTORICAL DATA TABLE
# ==========================================================

st.markdown("---")

st.subheader("Historical Records")

display_table = filtered[

    [

        "year",

        "season",

        indicator

    ]

].copy()

display_table.columns = [

    "Year",

    "Season",

    indicator.upper()

]

st.dataframe(

    display_table,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# DOWNLOAD
# ==========================================================

st.download_button(

    label="📥 Download Historical Data",

    data=display_table.to_csv(index=False),

    file_name=f"{zone}_{indicator}_historical_data.csv",

    mime="text/csv"

)

# ==========================================================
# PLATFORM NOTE
# ==========================================================

st.markdown("---")

st.info(
    """
**Platform Note**

This page presents **historical observed food security outcomes** and is intended
to support monitoring of seasonal trends over time. The results shown are based on
observed survey data and do **not** represent model forecasts.

To generate forecasts of future food security conditions, use the
**Forecasting & Risk Assessment** page. To evaluate the potential effects of
alternative assumptions, use the **Scenario Analysis** page.

Historical observations should always be interpreted alongside contextual
information on climate, markets, conflict and livelihoods.
"""
)