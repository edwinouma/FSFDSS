import streamlit as st
import pandas as pd

from utils.data_loader import load_data

from utils.shap_loader import load_shap
from utils.driver_categories import classify_driver
from utils.report_generator import generate_report
from utils.report_tables import (national_indicator_table)
from utils.report_tables import (national_forecast_table)
from utils.report_tables import (top_driver_table)


from utils.report_text import executive_summary

from utils.national_forecast import generate_national_forecast

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📄 Automated Food Security Situation & Forecast Report")

st.markdown(
"""
Generate an automated food security situation and forecast report
using historical monitoring, machine learning forecasts, model
interpretation and decision-support recommendations.

The report provides an operational summary suitable for
technical review, early warning and decision-making.
"""
)

# ==========================================================
# FORECAST SETTINGS
# ==========================================================

st.header("Forecast Settings")

col1, col2 = st.columns(2)

with col1:

    forecast_year = st.number_input(

        "Forecast Year",

        min_value=2025,

        max_value=2035,

        value=2026

    )

with col2:

    forecast_season = st.selectbox(

        "Forecast Season",

        [

            "Gu",

            "Deyr"

        ]

    )

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

latest = (

    df

    .sort_values(

        ["year","season_order"]

    )

    .iloc[-1]

)

latest_year = latest["year"]

latest_season = latest["season"]

latest_round = f"{latest_year} {latest_season}"

latest_df = df[

    (df["year"]==latest_year)

    &

    (df["season"]==latest_season)

]

national_fcs = latest_df["fcs"].mean()

national_rcsi = latest_df["rcsi"].mean()

national_hhs = latest_df["hhs"].mean()

# ==========================================================
# SHAP
# ==========================================================

shap = load_shap("FCS")

shap["Category"] = shap["Feature"].apply(

    classify_driver

)

dominant = (

    shap

    .groupby("Category")["Mean_Abs_SHAP"]

    .sum()

    .sort_values(

        ascending=False

    )

    .index[0]

)

top_driver = shap.iloc[0]["Feature"].replace("_"," ").title()

# ==========================================================
# NATIONAL FORECAST
# ==========================================================

national = generate_national_forecast(

    forecast_year,

    forecast_season

)

# ==========================================================
# REPORT OBJECTS
# ==========================================================

indicator_table = national_indicator_table(

    latest_df

)

driver_table = top_driver_table(

    shap,

    n=10

)

# ==========================================================
# FORECAST TABLE
# ==========================================================

forecast_summary = national_forecast_table(

    national,

    national["overall_risk"]

)

summary = executive_summary(

    latest_round,

    forecast_year,

    forecast_season,

    national_fcs,

    national_rcsi,

    national_hhs,

    national["national_fcs"],

    national["national_rcsi"],

    national["national_hhs"],

    national["overall_risk"],

    dominant,

    top_driver

)

# ==========================================================
# GENERATE REPORT
# ==========================================================

st.markdown("---")

st.subheader("Generate Automated Situation Report")

st.markdown(

"""
The report summarises the latest national food security
conditions, machine learning results, key drivers and
recommended actions.

The generated report is suitable for technical review,
decision support and documentation.
"""

)

if st.button(

    "📄 Generate Situation Report",

    use_container_width=True

):
    filename = (
        f"FSFDSS_Situation_and_Forecast_Report_"
        f"{forecast_year}_{forecast_season}.docx"
    )

    report_path = generate_report(

        filename=filename,

        latest_round=latest_round,

        forecast_year=forecast_year,

        forecast_season=forecast_season,

        monthly_reference=national["monthly_reference"],

        seasonal_reference=national["seasonal_reference"],

        national_fcs=national_fcs,

        national_rcsi=national_rcsi,

        national_hhs=national_hhs,

        forecast_results=national,

        overall_risk=national["overall_risk"],

        dominant=dominant,

        top_driver=top_driver,

        indicator_table=indicator_table,

        forecast_table=forecast_summary,

        driver_table=driver_table,

        summary=summary

    )

    st.success(

        "Situation report generated successfully."

    )

    # ==========================================================
    # REPORT PREVIEW
    # ==========================================================

    st.markdown("---")

    st.subheader("📖 Report Preview")

    st.markdown(summary)

    st.markdown("---")

    st.subheader("National Indicators")

    st.dataframe(

        indicator_table,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    st.subheader("Top Machine Learning Drivers")

    st.dataframe(

        driver_table,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    st.subheader("Early Warning Priorities")

    st.markdown("""

    - Monitor rainfall performance and vegetation conditions (NDVI).

    - Monitor staple food prices and the Cost of the Minimum Basket (CMB).

    - Track livestock market conditions, particularly goat prices.

    - Monitor conflict incidents and conflict-related fatalities.

    - Assess household livelihood resilience, including debt level, herd size and crop production.

    """)

    st.markdown("---")

    st.subheader("Recommendations")

    st.markdown("""

    1. Continue seasonal monitoring of food security indicators.

    2. Strengthen environmental monitoring to support early warning.

    3. Increase surveillance of market prices and household purchasing power.

    4. Maintain routine monitoring of conflict trends in vulnerable livelihood zones.

    5. Update machine learning forecasts whenever new monthly data become available.

    6. Use forecasting results alongside IPC analytical processes to support evidence-based decision-making.

    """)

    with open(

            report_path,

            "rb"

    ) as file:
        st.download_button(

            label="⬇ Download Situation Report (.docx)",

            data=file,

            file_name=filename,

            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            use_container_width=True

        )

st.markdown("---")

st.info(

"""
The report is automatically generated using the latest
historical monitoring results together with machine learning
outputs from the Food Security Forecasting and Decision
Support System (FSFDSS).

The report is intended to support operational decision-making
and should be interpreted alongside expert judgement and
existing food security analytical frameworks such as IPC.
"""

)