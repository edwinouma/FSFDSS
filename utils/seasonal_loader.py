# ==========================================================
# SEASONAL DATA LOADER
# ==========================================================
#
# Purpose
# -------
# Loads seasonal livelihood variables and
# automatically retrieves the latest available
# observations for forecasting.
#
# Used by
# -------
# forecast_builder.py
#
# ==========================================================

import pandas as pd

from config.settings import SEASONAL_DATA_PATH


# ==========================================================
# LOAD SEASONAL DATA
# ==========================================================

def load_seasonal_data():

    """
    Loads seasonal livelihood dataset.
    """

    df = pd.read_csv(

        SEASONAL_DATA_PATH

    )

    return df


# ==========================================================
# GET ZONE HISTORY
# ==========================================================

def get_zone_seasonal_data(

    livelihood_zone

):

    """
    Returns seasonal data for one livelihood zone.
    """

    df = load_seasonal_data()

    df = df[

        df["livelihood_zone_corrected"] == livelihood_zone

    ].copy()

    season_order = {

        "Gu": 1,

        "Deyr": 2

    }

    df["season_number"] = df["season"].map(

        season_order

    )

    df = df.sort_values(

        [

            "year",

            "season_number"

        ]

    )

    df.reset_index(

        drop=True,

        inplace=True

    )

    return df


# ==========================================================
# GET LATEST SEASONAL VALUES
# ==========================================================

def get_latest_seasonal_values(

    livelihood_zone,
    forecast_year,
    forecast_season

):

    """
    Returns the most recent seasonal livelihood
    observations available before the forecast.

    Returns
    -------
    dict

    debt_level

    herd_size

    crop_production

    reference_year

    reference_season

    reference_label
    """

    df = get_zone_seasonal_data(

        livelihood_zone

    )

    # ------------------------------------------------------
    # SELECT HISTORY
    # ------------------------------------------------------

    if forecast_season == "Gu":

        history = df[

            df["year"] < forecast_year

        ]

    else:

        history = df[

            (

                (df["year"] < forecast_year)

                |

                (

                    (df["year"] == forecast_year)

                    &

                    (df["season"] == "Gu")

                )

            )

        ]

    # ------------------------------------------------------
    # NO HISTORY AVAILABLE
    # ------------------------------------------------------

    if history.empty:

        return {

            "debt_level": None,

            "herd_size": None,

            "crop_production": None,

            "reference_year": None,

            "reference_season": None,

            "reference_label": "No historical livelihood data available"

        }

    # ------------------------------------------------------
    # LATEST AVAILABLE RECORD
    # ------------------------------------------------------

    latest = history.iloc[-1]

    return {

        "debt_level":

            latest.get("debt_level"),

        "herd_size":

            latest.get("herd_size"),

        "crop_production":

            latest.get("crop_production"),

        "reference_year":

            latest["year"],

        "reference_season":

            latest["season"],

        "reference_label":

            f"{latest['year']} {latest['season']}"

    }


# ==========================================================
# GET REFERENCE SUMMARY
# ==========================================================

def get_reference_summary(

    livelihood_zone,
    forecast_year,
    forecast_season

):

    """
    Returns a summary describing the
    seasonal reference being used.

    Used by the Streamlit interface.
    """

    reference = get_latest_seasonal_values(

        livelihood_zone,

        forecast_year,

        forecast_season

    )

    return {

        "Reference Season":

            reference["reference_label"],

        "Debt Level":

            reference["debt_level"],

        "Herd Size":

            reference["herd_size"],

        "Crop Production":

            reference["crop_production"]

    }