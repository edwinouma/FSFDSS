# ==========================================================
# NATIONAL FORECAST
# ==========================================================
#
# Purpose
# -------
# Generates baseline forecasts for every livelihood zone
# and returns national forecast summaries.
#
# Used by
# -------
# Situation Report
# Dashboard
# Future API
#
# ==========================================================

import pandas as pd

from config.settings import LIVELIHOOD_ZONES

from utils.forecast_builder import (
    build_forecast_inputs,
    forecast_summary
)

from utils.seasonal_loader import (
    get_latest_seasonal_values
)

from utils.prediction import (
    predict_all
)

from utils.risk import (
    overall_risk
)


# ==========================================================
# GENERATE NATIONAL FORECAST
# ==========================================================

def generate_national_forecast(

    forecast_year,

    forecast_season

):

    """
    Generates forecasts for all livelihood zones.

    Returns
    -------
    dict

    {
        "forecast_table": DataFrame,
        "national_fcs": float,
        "national_rcsi": float,
        "national_hhs": float,
        "overall_risk": str,
        "monthly_reference": str,
        "seasonal_reference": str
    }

    """

    forecasts = []

    monthly_reference = None
    seasonal_reference = None

    # ------------------------------------------------------
    # LOOP THROUGH LIVELIHOOD ZONES
    # ------------------------------------------------------

    for livelihood_zone in LIVELIHOOD_ZONES:

        # ----------------------------------------------
        # Monthly Monitoring Information
        # ----------------------------------------------

        monthly = forecast_summary(

            livelihood_zone,
            forecast_year,
            forecast_season

        )

        # ----------------------------------------------
        # Seasonal Information
        # ----------------------------------------------

        seasonal = get_latest_seasonal_values(

            livelihood_zone,
            forecast_year,
            forecast_season

        )

        # ----------------------------------------------
        # Build Model Inputs
        # ----------------------------------------------

        model_inputs = build_forecast_inputs(

            livelihood_zone,

            forecast_year,

            forecast_season,

            seasonal["debt_level"],

            seasonal["herd_size"],

            seasonal["crop_production"]

        )

        # ----------------------------------------------
        # Prediction
        # ----------------------------------------------

        prediction = predict_all(

            model_inputs,

            monthly_reference=monthly["reference"],

            seasonal_reference=seasonal["reference_label"]

        )

        forecasts.append({

            "Livelihood Zone": livelihood_zone,

            "Livelihood System": prediction["Livelihood System"],

            "Forecast FCS": prediction["FCS"],

            "Forecast rCSI": prediction["rCSI"],

            "Forecast HHS": prediction["HHS"]

        })

        # Save one copy of the references.
        # They should normally be identical.

        if monthly_reference is None:

            monthly_reference = monthly["reference"]

        if seasonal_reference is None:

            seasonal_reference = seasonal["reference_label"]

    # ------------------------------------------------------
    # CREATE DATAFRAME
    # ------------------------------------------------------

    forecast_table = pd.DataFrame(

        forecasts

    )

    # ------------------------------------------------------
    # NATIONAL AVERAGES
    # ------------------------------------------------------

    national_fcs = forecast_table[

        "Forecast FCS"

    ].mean()

    national_rcsi = forecast_table[

        "Forecast rCSI"

    ].mean()

    national_hhs = forecast_table[

        "Forecast HHS"

    ].mean()

    # ------------------------------------------------------
    # OVERALL RISK
    # ------------------------------------------------------

    national_risk = overall_risk(

        national_fcs,

        national_rcsi,

        national_hhs

    )

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return {

        "forecast_table": forecast_table,

        "national_fcs": national_fcs,

        "national_rcsi": national_rcsi,

        "national_hhs": national_hhs,

        "overall_risk": national_risk,

        "monthly_reference": monthly_reference,

        "seasonal_reference": seasonal_reference

    }