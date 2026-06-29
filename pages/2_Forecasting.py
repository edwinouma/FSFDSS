# ==========================================================
# FOOD SECURITY FORECASTING
# ==========================================================

import streamlit as st
import pandas as pd

from utils.risk import (
    classify_fcs,
    classify_rcsi,
    classify_hhs,
    overall_risk
)

from config.settings import LIVELIHOOD_ZONES

from utils.forecast_builder import (
    build_forecast_inputs,
    forecast_summary
)

from utils.seasonal_loader import (
    get_latest_seasonal_values
)

from utils.prediction import predict_all


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📈 Forecasting & Risk Assessment")

st.markdown(
"""
Generate baseline food security forecasts and automatically
translate predicted food security outcomes into
decision-support risk categories.

The platform automatically retrieves the latest available
monthly monitoring data and seasonal livelihood information
before generating forecasts and assessing risk.
"""
)

# ==========================================================
# STEP 1
# ==========================================================

st.header("Step 1: Select Forecast")

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
# STEP 2
# ==========================================================

st.header("Step 2: Historical Monthly Monitoring Data")

monthly = forecast_summary(

    livelihood_zone,

    forecast_year,

    forecast_season

)

monthly_data = monthly["data"]

monthly_reference = monthly["reference"]

st.success(

    f"Historical Monthly Monitoring Data Used for Forecasting: {monthly_reference}"

)

with st.expander(

    "View Historical Monthly Monitoring Data Used for Forecasting",

    expanded=False

):

    st.dataframe(

        monthly_data,

        use_container_width=True

    )

# ==========================================================
# STEP 3
# ==========================================================

st.header("Step 3: Latest Seasonal Livelihood Information")

seasonal = get_latest_seasonal_values(

    livelihood_zone,

    forecast_year,

    forecast_season

)

st.info(

    f"Latest livelihood information loaded from **{seasonal['reference_label']}**."

)

seasonal_table = pd.DataFrame(

    {

        "Variable":[

            "Debt Level",

            "Herd Size",

            "Crop Production"

        ],

        "Value":[

            seasonal["debt_level"],

            seasonal["herd_size"],

            seasonal["crop_production"]

        ]

    }

)

st.dataframe(

    seasonal_table,

    use_container_width=True

)

# ==========================================================
# STEP 4
# ==========================================================

st.header("Step 4: Generate Baseline Forecast")

st.markdown(

"""
The forecast below uses:

- Latest available monthly monitoring data
- Latest seasonal livelihood information
- Trained XGBoost forecasting models

No assumptions are modified in the baseline forecast.
Use the **Scenario Analysis** page to evaluate alternative
future conditions.
"""

)

# ==========================================================
# GENERATE FORECAST
# ==========================================================

if st.button(

    "🚀 Generate Forecast",

    type="primary"

):

    model_inputs = build_forecast_inputs(

        livelihood_zone,

        forecast_year,

        forecast_season,

        seasonal["debt_level"],

        seasonal["herd_size"],

        seasonal["crop_production"]

    )

    results = predict_all(

        model_inputs,

        monthly_reference=monthly_reference,

        seasonal_reference=seasonal["reference_label"]

    )

    st.markdown("---")

    st.header("📊 Step 5: Forecast Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Food Consumption Score (FCS)",

            round(results["FCS"],2)

        )

    with col2:

        st.metric(

            "Reduced Coping Strategy Index (rCSI)",

            round(results["rCSI"],2)

        )

    with col3:

        st.metric(

            "Household Hunger Scale (HHS)",

            round(results["HHS"],2)

        )

    # ==========================================================
    # STEP 5
    # RISK ASSESSMENT
    # ==========================================================

    st.markdown("---")

    st.header("⚠ Step 6: Risk Assessment & Decision Support")

    fcs_class = classify_fcs(results["FCS"])

    rcsi_class = classify_rcsi(results["rCSI"])

    hhs_class = classify_hhs(results["HHS"])

    overall = overall_risk(

        results["FCS"],
        results["rCSI"],
        results["HHS"]

    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(

            "FCS Category",

            fcs_class

        )

    with col2:
        st.metric(

            "rCSI Category",

            rcsi_class

        )

    with col3:
        st.metric(

            "HHS Category",

            hhs_class

        )

    st.markdown("---")

    # ==========================================================
    # OVERALL RISK
    # ==========================================================

    st.subheader("Overall Risk Assessment")

    if overall.upper() == "LOW":

        st.success(

            "🟢 LOW RISK\n\n"
            "Forecasted food security conditions are generally stable.\n\n"
            "Decision Support:\n"
            "• Continue routine monitoring.\n"
            "• No immediate intervention is required.\n"
            "• Continue monitoring climatic, market and conflict indicators."

        )

    elif overall.upper() == "MODERATE":

        st.warning(

            "🟡 MODERATE RISK\n\n"
            "Forecasted conditions indicate emerging pressures.\n\n"
            "Decision Support:\n"
            "• Increase monitoring frequency.\n"
            "• Prepare contingency measures.\n"
            "• Closely monitor key drivers."

        )

    elif overall.upper() == "HIGH":

        st.warning(

            "🟠 HIGH RISK\n\n"
            "Forecasted deterioration requires increased preparedness.\n\n"
            "Decision Support:\n"
            "• Conduct rapid assessments.\n"
            "• Strengthen preparedness.\n"
            "• Consider targeted interventions."

        )

    else:

        st.error(

            "🔴 VERY HIGH RISK\n\n"
            "Immediate action is recommended.\n\n"
            "Decision Support:\n"
            "• Conduct field verification.\n"
            "• Mobilise humanitarian response.\n"
            "• Intensify monitoring."

        )

    st.markdown("---")

    info = pd.DataFrame(

        {

            "Item": [

                "Livelihood Zone",

                "Livelihood System",

                "Forecast Year",

                "Forecast Season",

                "Historical Monthly Data Used",

                "Seasonal Information Used"

            ],

            "Value": [

                results["Livelihood Zone"],

                results["Livelihood System"],

                results["Forecast Year"],

                results["Forecast Season"],

                results["Monthly Data Used"],

                results["Seasonal Data Used"]

            ]

        }

    )

    # ==========================================================
    # FORECAST INFORMATION
    # ==========================================================

    st.markdown("---")

    st.header("Step 7: Forecast Information")

    with st.expander(

            "View Forecast Information",

            expanded=False

    ):

        st.dataframe(

            info,

            use_container_width=True

        )

    st.success(

        "Baseline forecast generated successfully."

    )