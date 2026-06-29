# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

APP_TITLE = "Food Security Forecasting and Decision Support System"

COUNTRY = "Somalia"

VERSION = "1.0"

# ----------------------------------------------------------
# MODEL PATHS
# ----------------------------------------------------------

FCS_MODEL_PATH = "models/xgb_fcs.pkl"

RCSI_MODEL_PATH = "models/xgb_rcsi.pkl"

HHS_MODEL_PATH = "models/xgb_hhs.pkl"

# ----------------------------------------------------------
# LIVELIHOOD ZONES
# ----------------------------------------------------------

LIVELIHOOD_ZONES = [

    "Bay Agropastoral",
    "Central/NE Hawd Pastoral",
    "Coastal Deeh Pastoral and Fishing",
    "East Golis Pastoral",
    "Gedo Pastoral",
    "Gedo Riverine",
    "Guban Pastoral",
    "NE Northern Inland Pastoral",
    "NW Agropastoral",
    "NW Hawd Pastoral",
    "NW Northern Inland Pastoral",
    "Shabelle Agropastoral",
    "Shabelle Riverine",
    "West Golis Pastoral"

]

SEASONS = [
    "Gu",
    "Deyr"
]

# ==========================================================
# DATA
# ==========================================================

MONTHLY_DATA_PATH = "data/monthly_data.csv"

SEASONAL_DATA_PATH = "data/seasonal_data.csv"