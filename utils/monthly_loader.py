# ==========================================================
# MONTHLY DATA LOADER
# ==========================================================
#
# Purpose:
# --------
# Loads the latest monthly monitoring dataset and
# automatically constructs lag variables required by
# the trained machine learning models.
#
# Used by:
# --------
# forecast_builder.py
#
# ==========================================================

import pandas as pd

from config.settings import MONTHLY_DATA_PATH


# ==========================================================
# LOAD MONTHLY DATA
# ==========================================================

def load_monthly_data():

    """
    Load monthly monitoring dataset.

    Returns
    -------
    DataFrame
    """

    df = pd.read_csv(MONTHLY_DATA_PATH)

    return df


# ==========================================================
# MONTH ORDER
# ==========================================================

MONTH_ORDER = {

    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12

}


# ==========================================================
# GET LATEST MONTHLY DATA
# ==========================================================

def get_zone_monthly_data(

    livelihood_zone

):

    """
    Returns monthly data for one livelihood zone.
    """

    df = load_monthly_data()

    df = df[

        df["livelihood_zone_corrected"] == livelihood_zone

    ].copy()

    df["month_number"] = df["month"].map(

        MONTH_ORDER

    )

    df = df.sort_values(

        [

            "year",
            "month_number"

        ]

    )

    df.reset_index(

        drop=True,
        inplace=True

    )

    return df


# ==========================================================
# CREATE LAG FEATURES
# ==========================================================

def create_monthly_lags(

    livelihood_zone,
    forecast_year,
    forecast_season

):

    """
    Automatically creates all lag variables required
    by the prediction models.

    Parameters
    ----------
    livelihood_zone : str

    forecast_year : int

    forecast_season : Gu / Deyr

    Returns
    -------
    Dictionary
    """

    df = get_zone_monthly_data(

        livelihood_zone

    )

    # ------------------------------------------------------
    # DETERMINE LAST MONTH OF FORECAST WINDOW
    # ------------------------------------------------------

    if forecast_season == "Gu":

        end_month = 6

    else:

        end_month = 10

    # ------------------------------------------------------
    # KEEP HISTORY ONLY
    # ------------------------------------------------------

    history = df[

        (

            (df["year"] < forecast_year)

            |

            (

                (df["year"] == forecast_year)

                &

                (df["month_number"] <= end_month)

            )

        )

    ].copy()

    history = history.sort_values(

        [

            "year",
            "month_number"

        ]

    )

    # ------------------------------------------------------
    # MONTHLY VARIABLES
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # CREATE FEATURES
    # ------------------------------------------------------

    features = {}

    # Keep the latest seven months:
    #
    # Month 7 (latest) -> current variable
    # Month 6          -> lag1
    # Month 5          -> lag2
    # ...
    # Month 1          -> lag6
    #
    # This reproduces exactly how the modelling dataset
    # was constructed using pandas shift().

    latest = history.tail(7)

    latest = latest.reset_index(

        drop=True

    )

    for variable in monthly_variables:

        values = latest[variable].tolist()

        # --------------------------------------------------
        # CURRENT VALUE
        # --------------------------------------------------

        if len(values) >= 1:

            features[variable] = values[-1]

        else:

            features[variable] = 0

        # --------------------------------------------------
        # LAG FEATURES
        # --------------------------------------------------

        for lag in range(1, 7):

            if len(values) > lag:

                features[f"{variable}_lag{lag}"] = values[-(lag + 1)]

            else:

                features[f"{variable}_lag{lag}"] = 0

    return features


# ==========================================================
# DISPLAY MONTHS USED
# ==========================================================

# ==========================================================
# FORECAST WINDOW
# ==========================================================

def get_forecast_window(

    livelihood_zone,
    forecast_year,
    forecast_season

):

    """
    Returns the monthly observations used
    for forecasting together with a dynamic
    reference describing the period.

    Returns
    -------
    dict

    {
        "data": DataFrame,
        "reference": "Jan 2026 - Jun 2026"
    }
    """

    df = get_zone_monthly_data(

        livelihood_zone

    )

    # ------------------------------------------------------
    # DETERMINE FORECAST WINDOW
    # ------------------------------------------------------

    if forecast_season == "Gu":

        end_month = 6

    else:

        end_month = 10

    history = df[

        (

            (df["year"] < forecast_year)

            |

            (

                (df["year"] == forecast_year)

                &

                (df["month_number"] <= end_month)

            )

        )

    ].copy()

    history = history.tail(7)

    # ------------------------------------------------------
    # CREATE REFERENCE LABEL
    # ------------------------------------------------------

    if history.empty:

        reference = "No monthly monitoring data available"

    else:

        first = history.iloc[0]

        last = history.iloc[-1]

        reference = (

            f"{first['month']} {first['year']}"

            " - "

            f"{last['month']} {last['year']}"

        )

    return {

        "data": history,

        "reference": reference

    }