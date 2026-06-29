# ==========================================================
# FORECAST BUILDER
# ==========================================================

from utils.monthly_loader import (
    create_monthly_lags,
    get_forecast_window
)

# ==========================================================
# LIVELIHOOD SYSTEM MAPPING
# ==========================================================

LIVELIHOOD_SYSTEMS = {

    "Addun Pastoral": "Pastoral",

    "Central/NE Hawd Pastoral": "Pastoral",

    "East Golis Pastoral": "Pastoral",

    "Gedo Pastoral": "Pastoral",

    "Guban Pastoral": "Pastoral",

    "NE Northern Inland Pastoral": "Pastoral",

    "NW Hawd Pastoral": "Pastoral",

    "NW Northern Inland Pastoral": "Pastoral",

    "West Golis Pastoral": "Pastoral",

    "Bay Agropastoral": "Agropastoral",

    "Southern Agropastoral": "Agropastoral",

    "Cowpea Belt Agropastoral": "Agropastoral",

    "Shabelle Riverine": "Riverine",

    "Juba Riverine": "Riverine",

    "Coastal Deeh Pastoral and Fishing":
        "Pastoral and Fishing"

}


# ==========================================================
# BUILD FORECAST INPUTS
# ==========================================================

def build_forecast_inputs(

    livelihood_zone,

    forecast_year,

    forecast_season,

    debt_level,

    herd_size,

    crop_production

):

    # ------------------------------------------------------
    # MONTHLY FEATURES
    # ------------------------------------------------------

    monthly_features = create_monthly_lags(

        livelihood_zone,

        forecast_year,

        forecast_season

    )

    # ------------------------------------------------------
    # DETERMINE LIVELIHOOD SYSTEM
    # ------------------------------------------------------

    livelihood_system = LIVELIHOOD_SYSTEMS.get(

        livelihood_zone,

        "Unknown"

    )

    # ------------------------------------------------------
    # BUILD INPUTS
    # ------------------------------------------------------

    model_inputs = {

        "livelihood_zone_corrected": livelihood_zone,

        "livelihood_system": livelihood_system,

        "year": forecast_year,

        "season": forecast_season,

        "debt_level": debt_level,

        "herd_size": herd_size,

        "crop_production": crop_production

    }

    # ------------------------------------------------------
    # MERGE MONTHLY VARIABLES
    # ------------------------------------------------------

    model_inputs.update(

        monthly_features

    )

    # ======================================================
    # AVAILABILITY FLAGS
    # ======================================================

    # Seasonal variables

    model_inputs["debt_level_available"] = int(

        debt_level is not None

    )

    model_inputs["herd_size_available"] = int(

        herd_size is not None

    )

    model_inputs["crop_production_available"] = int(

        crop_production is not None

    )

    # Monthly lag variables

    monthly_variables = [

        "rainfall",

        "ndvi",

        "river_level",

        "cmb",

        "goat_price",

        "rice_price",

        "sorghum_price",

        "water_price",

        "conflict_incidents",

        "conflict_fatalities"

    ]

    for variable in monthly_variables:

        for lag in range(1, 7):

            column = f"{variable}_lag{lag}"

            value = model_inputs.get(column)

            model_inputs[f"{column}_available"] = int(

                value is not None

            )

    # Current river level

    model_inputs["river_level_available"] = int(

        model_inputs.get("river_level") is not None

    )

    return model_inputs


# ==========================================================
# FORECAST SUMMARY
# ==========================================================

def forecast_summary(

    livelihood_zone,

    forecast_year,

    forecast_season

):

    """
    Returns the monthly monitoring data and
    reference period used for forecasting.

    Returns
    -------
    dict

    {
        "data": DataFrame,
        "reference": "Jan 2026 - Jun 2026"
    }
    """

    return get_forecast_window(

        livelihood_zone,

        forecast_year,

        forecast_season

    )


# ==========================================================
# BUILD SCENARIO INPUTS
# ==========================================================

def build_scenario_inputs(

    livelihood_zone,

    forecast_year,

    forecast_season,

    baseline_debt,

    baseline_herd,

    baseline_crop,

    scenario_debt,

    scenario_herd,

    scenario_crop

):

    baseline = build_forecast_inputs(

        livelihood_zone,

        forecast_year,

        forecast_season,

        baseline_debt,

        baseline_herd,

        baseline_crop

    )

    scenario = build_forecast_inputs(

        livelihood_zone,

        forecast_year,

        forecast_season,

        scenario_debt,

        scenario_herd,

        scenario_crop

    )

    return baseline, scenario