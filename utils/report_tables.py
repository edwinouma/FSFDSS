import pandas as pd

# ==========================================================
# HISTORICAL NATIONAL INDICATORS
# ==========================================================

def national_indicator_table(latest_df):

    return pd.DataFrame({

        "Indicator": [

            "Food Consumption Score (FCS)",
            "Reduced Coping Strategy Index (rCSI)",
            "Household Hunger Scale (HHS)"

        ],

        "Historical Average": [

            latest_df["fcs"].mean(),
            latest_df["rcsi"].mean(),
            latest_df["hhs"].mean()

        ]

    })


# ==========================================================
# FORECAST SUMMARY TABLE
# ==========================================================

# ==========================================================
# FORECAST SUMMARY TABLE
# ==========================================================

def national_forecast_table(

    forecast_results,

    overall_risk

):

    return pd.DataFrame({

        "Forecast Indicator": [

            "Food Consumption Score (FCS)",
            "Reduced Coping Strategy Index (rCSI)",
            "Household Hunger Scale (HHS)",
            "Overall Risk"

        ],

        "Forecast": [

            round(forecast_results["national_fcs"], 2),
            round(forecast_results["national_rcsi"], 2),
            round(forecast_results["national_hhs"], 2),
            overall_risk

        ]

    })


# ==========================================================
# TOP SHAP DRIVERS
# ==========================================================

def top_driver_table(

    shap,

    n=10

):

    table = shap.head(n)[

        [

            "Feature",
            "Mean_Abs_SHAP"

        ]

    ].copy()

    table.columns = [

        "Driver",
        "Mean |SHAP|"

    ]

    return table