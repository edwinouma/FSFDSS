import streamlit as st
import pandas as pd
from config.settings import LIVELIHOOD_ZONES
from utils.forecast_builder import (

    build_forecast_inputs,

    forecast_summary

)

from utils.seasonal_loader import (

    get_latest_seasonal_values

)

from config.scenario_settings import (

    DEFAULT_MIN_CHANGE,
    DEFAULT_MAX_CHANGE,
    DEFAULT_STEP,
    DEFAULT_VALUE,

    CONFLICT_MIN_CHANGE,
    CONFLICT_MAX_CHANGE,
    CONFLICT_STEP

)

from utils.prediction import compare_predictions
from utils.charts import plot_historical_forecast

from utils.risk import (

    classify_fcs,

    classify_rcsi,

    classify_hhs

)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🧪 Scenario Analysis")

st.markdown(
    """
    Evaluate how changes in climate, market, conflict and livelihood
    conditions may influence predicted food security outcomes.
    """
)

# ==========================================================
# BASELINE SELECTION
# ==========================================================

st.header("Current Baseline Conditions")

st.markdown(
    """
    Select a livelihood zone. The platform automatically loads the
    latest available monthly monitoring data and seasonal livelihood information to serve as the baseline
    scenario.
    """
)

col1, col2, col3 = st.columns(3)

with col1:

    livelihood_zone = st.selectbox(

        "Livelihood Zone",

        LIVELIHOOD_ZONES

    )

with col2:

    forecast_year = st.number_input(

        "Forecast Year",

        min_value=2025,

        max_value=2035,

        value=2026

    )

with col3:

    forecast_season = st.selectbox(

        "Forecast Season",

        [

            "Gu",

            "Deyr"

        ]

    )

# ==========================================================
# LOAD LATEST OBSERVATION
# ==========================================================

monthly = forecast_summary(

    livelihood_zone,

    forecast_year,

    forecast_season

)

monthly_reference = monthly["reference"]

monthly_data = monthly["data"]

seasonal = get_latest_seasonal_values(

    livelihood_zone,

    forecast_year,

    forecast_season

)

# ==========================================================
# BASELINE INFORMATION
# ==========================================================

st.success(

    f"Historical Monthly Monitoring Data Used: {monthly_reference}"

)

with st.expander(

    "View Historical Monthly Monitoring Data",

    expanded=False

):

    st.dataframe(

        monthly_data,

        use_container_width=True

    )

st.info(

    f"Latest seasonal livelihood information loaded from **{seasonal['reference_label']}**."

)

st.info(
    """
The baseline scenario is automatically constructed using:

• Historical monthly monitoring data

• Latest seasonal livelihood information

Observed food security outcomes are not displayed because
the selected forecast season has not yet occurred.
"""
)

# ==========================================================
# BASELINE CONDITIONS
# ==========================================================

st.markdown("---")

st.subheader("Baseline Conditions")

# ----------------------------------------------------------
# CLIMATE & ENVIRONMENT
# ----------------------------------------------------------

with st.expander("🌧 Climate & Environment", expanded=True):

    climate = pd.DataFrame({

        "Variable": [

            "Rainfall",
            "NDVI",
            "River Level"

        ],

        "Value": [

            monthly_data.iloc[-1]["rainfall"],
            monthly_data.iloc[-1]["ndvi"],
            monthly_data.iloc[-1]["river_level"]
        ]

    })

    st.dataframe(

        climate,

        use_container_width=True,

        hide_index=True

    )

# ----------------------------------------------------------
# MARKET
# ----------------------------------------------------------

with st.expander("💰 Market", expanded=True):

    market = pd.DataFrame({

        "Variable": [

            "Cost of Minimum Basket",
            "Goat Price",
            "Rice Price",
            "Sorghum Price",
            "Water Price"

        ],

        "Value": [

            monthly_data.iloc[-1]["cmb"],
            monthly_data.iloc[-1]["goat_price"],
            monthly_data.iloc[-1]["rice_price"],
            monthly_data.iloc[-1]["sorghum_price"],
            monthly_data.iloc[-1]["water_price"]
        ]

    })

    st.dataframe(

        market,

        use_container_width=True,

        hide_index=True

    )

# ----------------------------------------------------------
# CONFLICT
# ----------------------------------------------------------

with st.expander("⚔ Conflict", expanded=True):

    conflict = pd.DataFrame({

        "Variable": [

            "Conflict Incidents",
            "Conflict Fatalities"

        ],

        "Value": [

            monthly_data.iloc[-1]["conflict_incidents"],
            monthly_data.iloc[-1]["conflict_fatalities"]
        ]

    })

    st.dataframe(

        conflict,

        use_container_width=True,

        hide_index=True

    )

# ----------------------------------------------------------
# LIVELIHOOD
# ----------------------------------------------------------

with st.expander("🐄 Livelihood", expanded=True):

    livelihood = pd.DataFrame({

        "Variable": [

            "Debt Level",
            "Herd Size",
            "Crop Production"

        ],

        "Value": [

            seasonal["debt_level"],
            seasonal["herd_size"],
            seasonal["crop_production"]

        ]

    })

    st.dataframe(

        livelihood,

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# INFORMATION
# ==========================================================

st.info(
    """
    The values displayed above represent the baseline conditions
    automatically constructed from the latest available monthly
    monitoring data and seasonal livelihood information.

    In the next step, you will be able to modify selected variables to
    evaluate how changes in climate, markets, conflict and livelihood
    conditions influence the predicted food security outcomes.
    """
)


# ==========================================================
# SCENARIO BUILDER
# ==========================================================

st.markdown("---")

st.header("Scenario Builder")

st.markdown(
    """
    Adjust selected variables to create an alternative scenario.
    Percentage changes are applied relative to the current baseline.
    """
)

# ==========================================================
# HELPER FUNCTION
# ==========================================================

def apply_change(value, percent):

    if pd.isna(value):

        return value

    return value * (1 + percent / 100)


# ==========================================================
# GENERIC SCENARIO SLIDER
# ==========================================================

def scenario_slider(

    label,
    current_value,
    minimum=DEFAULT_MIN_CHANGE,
    maximum=DEFAULT_MAX_CHANGE,
    step=DEFAULT_STEP,
    decimals=2

):

    return st.slider(

        f"{label} (Current: {current_value:.{decimals}f})",

        minimum,

        maximum,

        DEFAULT_VALUE,

        step

    )


# ==========================================================
# CLIMATE & ENVIRONMENT
# ==========================================================

with st.expander("🌧 Climate & Environment", expanded=True):

    rainfall_change = scenario_slider(

        "Rainfall (%)",

        monthly_data.iloc[-1]["rainfall"]

    )

    ndvi_change = scenario_slider(

        "NDVI (%)",

        monthly_data.iloc[-1]["ndvi"],

        decimals=3

    )

    river_change = scenario_slider(

        "River Level (%)",

        monthly_data.iloc[-1]["river_level"]

    )

with st.expander("💰 Market"):

    cmb_change = scenario_slider(

        "Cost of Minimum Basket (%)",

        monthly_data.iloc[-1]["cmb"]

    )

    goat_change = scenario_slider(

        "Goat Price (%)",

        monthly_data.iloc[-1]["goat_price"]

    )

    rice_change = scenario_slider(

        "Rice Price (%)",

        monthly_data.iloc[-1]["rice_price"]

    )

    sorghum_change = scenario_slider(

        "Sorghum Price (%)",

        monthly_data.iloc[-1]["sorghum_price"]

    )

    water_change = scenario_slider(

        "Water Price (%)",

        monthly_data.iloc[-1]["water_price"]

    )

with st.expander("⚔ Conflict"):

    incidents_change = scenario_slider(

        "Conflict Incidents (%)",

        monthly_data.iloc[-1]["conflict_incidents"],

        minimum=CONFLICT_MIN_CHANGE,

        maximum=CONFLICT_MAX_CHANGE,

        step=CONFLICT_STEP,

        decimals=0

    )

    fatalities_change = scenario_slider(

        "Conflict Fatalities (%)",

        monthly_data.iloc[-1]["conflict_fatalities"],

        minimum=CONFLICT_MIN_CHANGE,

        maximum=CONFLICT_MAX_CHANGE,

        step=CONFLICT_STEP,

        decimals=0

    )

with st.expander("🐄 Livelihood"):

    debt_change = scenario_slider(

        "Debt Level (%)",

        seasonal["debt_level"]

    )

    herd_change = scenario_slider(

        "Herd Size (%)",

        seasonal["herd_size"]

    )

    crop_change = scenario_slider(

        "Crop Production (%)",

        seasonal["crop_production"]

    )

# ==========================================================
# PREPARE MODEL INPUTS
# ==========================================================

baseline_inputs = build_forecast_inputs(

    livelihood_zone,

    forecast_year,

    forecast_season,

    seasonal["debt_level"],

    seasonal["herd_size"],

    seasonal["crop_production"]

)

st.markdown("### DEBUG")

st.write("Baseline input keys")

st.write(sorted(baseline_inputs.keys()))

# ==========================================================
# BUILD SCENARIO
# ==========================================================

scenario_inputs = baseline_inputs.copy()

scenario_inputs["rainfall"] = apply_change(
    baseline_inputs["rainfall"],
    rainfall_change
)

for lag in range(1,7):
    scenario_inputs[f"rainfall_lag{lag}"] = apply_change(
        baseline_inputs[f"rainfall_lag{lag}"],
        rainfall_change
    )

scenario_inputs["ndvi"] = apply_change(
    baseline_inputs["ndvi"],
    ndvi_change
)

for lag in range(1,7):
    scenario_inputs[f"ndvi_lag{lag}"] = apply_change(
        baseline_inputs[f"ndvi_lag{lag}"],
        ndvi_change
    )

scenario_inputs["river_level"] = apply_change(
    baseline_inputs["river_level"],
    river_change
)

for lag in range(1,7):
    scenario_inputs[f"river_level_lag{lag}"] = apply_change(
        baseline_inputs[f"river_level_lag{lag}"],
        river_change
    )

scenario_inputs["cmb"] = apply_change(
    baseline_inputs["cmb"],
    cmb_change
)

for lag in range(1,7):
    scenario_inputs[f"cmb_lag{lag}"] = apply_change(
        baseline_inputs[f"cmb_lag{lag}"],
        cmb_change
    )

scenario_inputs["goat_price"] = apply_change(
    baseline_inputs["goat_price"],
    goat_change
)

for lag in range(1,7):
    scenario_inputs[f"goat_price_lag{lag}"] = apply_change(
        baseline_inputs[f"goat_price_lag{lag}"],
        goat_change
    )

scenario_inputs["rice_price"] = apply_change(
    baseline_inputs["rice_price"],
    rice_change
)

for lag in range(1,7):
    scenario_inputs[f"rice_price_lag{lag}"] = apply_change(
        baseline_inputs[f"rice_price_lag{lag}"],
        rice_change
    )

scenario_inputs["sorghum_price"] = apply_change(
    baseline_inputs["sorghum_price"],
    sorghum_change
)

for lag in range(1,7):
    scenario_inputs[f"sorghum_price_lag{lag}"] = apply_change(
        baseline_inputs[f"sorghum_price_lag{lag}"],
        sorghum_change
    )

scenario_inputs["water_price"] = apply_change(
    baseline_inputs["water_price"],
    water_change
)

for lag in range(1,7):
    scenario_inputs[f"water_price_lag{lag}"] = apply_change(
        baseline_inputs[f"water_price_lag{lag}"],
        water_change
    )

scenario_inputs["conflict_incidents"] = apply_change(
    baseline_inputs["conflict_incidents"],
    incidents_change
)

for lag in range(1,7):
    scenario_inputs[f"conflict_incidents_lag{lag}"] = apply_change(
        baseline_inputs[f"conflict_incidents_lag{lag}"],
        incidents_change
    )

scenario_inputs["conflict_fatalities"] = apply_change(
    baseline_inputs["conflict_fatalities"],
    fatalities_change
)

for lag in range(1,7):
    scenario_inputs[f"conflict_fatalities_lag{lag}"] = apply_change(
        baseline_inputs[f"conflict_fatalities_lag{lag}"],
        fatalities_change
    )


scenario_inputs["debt_level"] = apply_change(
    seasonal["debt_level"],
    debt_change

)

scenario_inputs["herd_size"] = apply_change(

    seasonal["herd_size"],

    herd_change

)

scenario_inputs["crop_production"] = apply_change(

    seasonal["crop_production"],

    crop_change

)

# ==========================================================
# PREVIEW
# ==========================================================

st.markdown("---")

st.subheader("Scenario Preview")

preview = pd.DataFrame({

    "Variable": [

        "Rainfall",
        "NDVI",
        "River Level",
        "Cost of Minimum Basket",
        "Goat Price",
        "Rice Price",
        "Sorghum Price",
        "Water Price",
        "Conflict Incidents",
        "Conflict Fatalities",
        "Debt Level",
        "Herd Size",
        "Crop Production"

    ],

    "Baseline": [

        baseline_inputs["rainfall"],
        baseline_inputs["ndvi"],
        baseline_inputs["river_level"],
        baseline_inputs["cmb"],
        baseline_inputs["goat_price"],
        baseline_inputs["rice_price"],
        baseline_inputs["sorghum_price"],
        baseline_inputs["water_price"],
        baseline_inputs["conflict_incidents"],
        baseline_inputs["conflict_fatalities"],
        baseline_inputs["debt_level"],
        baseline_inputs["herd_size"],
        baseline_inputs["crop_production"]

    ],

    "Scenario": [

        scenario_inputs["rainfall"],
        scenario_inputs["ndvi"],
        scenario_inputs["river_level"],
        scenario_inputs["cmb"],
        scenario_inputs["goat_price"],
        scenario_inputs["rice_price"],
        scenario_inputs["sorghum_price"],
        scenario_inputs["water_price"],
        scenario_inputs["conflict_incidents"],
        scenario_inputs["conflict_fatalities"],
        scenario_inputs["debt_level"],
        scenario_inputs["herd_size"],
        scenario_inputs["crop_production"]

    ]

})

# ----------------------------------------------------------
# CALCULATE CHANGE
# ----------------------------------------------------------

preview["Change"] = (

    preview["Scenario"]

    - preview["Baseline"]

)

preview["% Change"] = (

    (preview["Change"] / preview["Baseline"]) * 100

)

# ----------------------------------------------------------
# TREND INDICATOR
# ----------------------------------------------------------

def get_trend(change):

    if pd.isna(change):

        return ""

    elif change > 0:

        return "🔺 Increase"

    elif change < 0:

        return "🔻 Decrease"

    else:

        return "➖ No Change"

preview["Trend"] = preview["Change"].apply(get_trend)

# ----------------------------------------------------------
# HANDLE DIVISION BY ZERO
# ----------------------------------------------------------

preview.replace(

    [float("inf"), float("-inf")],

    pd.NA,

    inplace=True

)

# ----------------------------------------------------------
# ROUND VALUES
# ----------------------------------------------------------

numeric_columns = [

    "Baseline",
    "Scenario",
    "Change",
    "% Change"

]

preview[numeric_columns] = preview[numeric_columns].round(2)

preview = preview[

    [

        "Variable",

        "Baseline",

        "Scenario",

        "Trend",

        "Change",

        "% Change"

    ]

]

# ----------------------------------------------------------
# DISPLAY
# ----------------------------------------------------------

changed_preview = preview[

    preview["Change"] != 0

].copy()

st.markdown("### Modified Variables")

if changed_preview.empty:

    st.success(

        "No variables have been modified. The scenario is identical to the baseline."

    )

else:

    st.dataframe(

        changed_preview,

        use_container_width=True,

        hide_index=True

    )

with st.expander("Show All Variables"):

    st.dataframe(

        preview,

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# RISK CLASSIFICATION
# ==========================================================
# Risk classification functions are imported from utils.risk
# to ensure consistent classification across the platform.


# ==========================================================
# MODEL PREDICTIONS
# ==========================================================

st.markdown("---")

st.header("📈 Prediction Comparison")

st.write("Rainfall slider:", rainfall_change)
st.write("NDVI slider:", ndvi_change)
st.write("Goat slider:", goat_change)

st.write("Baseline rainfall lag1:", baseline_inputs["rainfall_lag1"])
st.write("Scenario rainfall lag1:", scenario_inputs["rainfall_lag1"])

st.write("Baseline goat lag1:", baseline_inputs["goat_price_lag1"])
st.write("Scenario goat lag1:", scenario_inputs["goat_price_lag1"])

results = compare_predictions(

    baseline_inputs,

    scenario_inputs

)

baseline_pred = results["Baseline"]

scenario_pred = results["Scenario"]

# ----------------------------------------------------------
# BUILD RESULTS TABLE
# ----------------------------------------------------------

comparison = pd.DataFrame({

    "Outcome": [

        "FCS",

        "rCSI",

        "HHS"

    ],

    "Baseline": [

        baseline_pred["FCS"],

        baseline_pred["rCSI"],

        baseline_pred["HHS"]

    ],

    "Scenario": [

        scenario_pred["FCS"],

        scenario_pred["rCSI"],

        scenario_pred["HHS"]

    ]

})

comparison["Difference"] = (

    comparison["Scenario"]

    - comparison["Baseline"]

)

comparison["% Change"] = (

    comparison["Difference"]

    / comparison["Baseline"]

) * 100

comparison.replace(

    [float("inf"), float("-inf")],

    pd.NA,

    inplace=True

)

# ----------------------------------------------------------
# TREND
# ----------------------------------------------------------

comparison["Trend"] = comparison["Difference"].apply(get_trend)

# ----------------------------------------------------------
# RISK CLASSIFICATION
# ----------------------------------------------------------

comparison["Risk"] = [

    classify_fcs(comparison.iloc[0]["Scenario"]),

    classify_rcsi(comparison.iloc[1]["Scenario"]),

    classify_hhs(comparison.iloc[2]["Scenario"])

]

comparison = comparison[[

    "Outcome",

    "Baseline",

    "Scenario",

    "Risk",

    "Trend",

    "Difference",

    "% Change"

]]

comparison[

    [

        "Baseline",

        "Scenario",

        "Difference",

        "% Change"

    ]

] = comparison[

    [

        "Baseline",

        "Scenario",

        "Difference",

        "% Change"

    ]

].round(2)

# ----------------------------------------------------------
# KPI CARDS
# ----------------------------------------------------------

st.subheader("Predicted Food Security Outcomes")

c1, c2, c3 = st.columns(3)

for column, (_, row) in zip(

    [c1, c2, c3],

    comparison.iterrows()

):

    delta = row["Scenario"] - row["Baseline"]

    column.metric(

        label=row["Outcome"],

        value=f"{row['Scenario']:.2f}",

        delta=f"{delta:.2f}"

    )

# ----------------------------------------------------------
# COMPARISON TABLE
# ----------------------------------------------------------

st.markdown("---")

st.subheader("Prediction Comparison")

st.dataframe(

    comparison,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# DECISION SUPPORT
# ==========================================================

st.markdown("---")

st.header("🧠 Decision Support")

negative = comparison[

    comparison["Difference"] < 0

]["Outcome"].tolist()

positive = comparison[

    comparison["Difference"] > 0

]["Outcome"].tolist()

summary = []

if "FCS" in negative:

    summary.append(

        "- Food Consumption Score is projected to decline."

    )

if "rCSI" in positive:

    summary.append(

        "- Household reliance on coping strategies is projected to increase."

    )

if "HHS" in positive:

    summary.append(

        "- Household hunger is projected to worsen."

    )

if len(summary) == 0:

    st.success(

        "The simulated scenario does not produce a meaningful deterioration in the predicted food security outcomes."

    )

else:

    st.warning(

        "\n".join(summary)

    )

st.markdown("---")

st.subheader("Recommended Actions")

recommendations = []

if rainfall_change < 0:

    recommendations.append(

        "🌧 Strengthen monitoring of rainfall and vegetation conditions."

    )

if incidents_change > 0:

    recommendations.append(

        "⚔ Intensify conflict monitoring and assess implications for food access."

    )

if goat_change > 0 or rice_change > 0 or sorghum_change > 0:

    recommendations.append(

        "💰 Monitor market prices and household purchasing power."

    )

if debt_change > 0:

    recommendations.append(

        "🐄 Monitor household debt and livelihood resilience."

    )

if len(recommendations) == 0:

    st.info(

        "No major driver adjustments were introduced in the scenario."

    )

else:

    for recommendation in recommendations:

        st.markdown(

            recommendation

        )

# ==========================================================
# HISTORICAL FORECAST VISUALISATION
# ==========================================================

st.markdown("---")

st.header("📈 Historical Trend with Scenario Forecast")

st.markdown(
    """
    Compare historical observations with the baseline and
    simulated scenario forecasts.

    Solid lines represent observed historical values, while
    dashed lines represent projected outcomes under the
    baseline and simulated scenarios.
    """
)

# ----------------------------------------------------------
# INDICATOR
# ----------------------------------------------------------

forecast_indicator = st.selectbox(

    "Forecast Indicator",

    [

        "fcs",

        "rcsi",

        "hhs"

    ],

    key="forecast_indicator"

)

# ----------------------------------------------------------
# SELECT MODEL PREDICTIONS
# ----------------------------------------------------------

if forecast_indicator == "fcs":

    baseline_value = baseline_pred["FCS"]

    scenario_value = scenario_pred["FCS"]

elif forecast_indicator == "rcsi":

    baseline_value = baseline_pred["rCSI"]

    scenario_value = scenario_pred["rCSI"]

else:

    baseline_value = baseline_pred["HHS"]

    scenario_value = scenario_pred["HHS"]

# ----------------------------------------------------------
# BUILD FIGURE
# ----------------------------------------------------------

forecast_fig = plot_historical_forecast(

    zone=livelihood_zone,

    indicator=forecast_indicator,

    forecast_year=forecast_year,

    forecast_season=forecast_season,

    baseline_prediction=baseline_value,

    scenario_prediction=scenario_value

)

st.plotly_chart(

    forecast_fig,

    use_container_width=True

)

# ----------------------------------------------------------
# CAVEAT
# ----------------------------------------------------------

st.info(
    """
    **Forecast interpretation**

    The dashed lines represent scenario projections generated
    using the trained XGBoost models.

    Since XGBoost is not an autoregressive forecasting model,
    the projected seasonal values are scenario-based estimates
    rather than recursively generated multi-season forecasts.

    They should therefore be interpreted as plausible future
    outcomes under the specified assumptions rather than exact
    predictions of future observations.
    """
)