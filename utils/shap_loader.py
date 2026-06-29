# ==========================================================
# SHAP DATA LOADER
# ==========================================================

import pandas as pd

# ----------------------------------------------------------
# LOAD SHAP TABLES
# ----------------------------------------------------------

def load_fcs_shap():

    return pd.read_excel(
        "data/fcs_shap_summary.xlsx"
    )


def load_rcsi_shap():

    return pd.read_excel(
        "data/rcsi_shap_summary.xlsx"
    )


def load_hhs_shap():

    return pd.read_excel(
        "data/hhs_shap_summary.xlsx"
    )


# ----------------------------------------------------------
# GENERIC LOADER
# ----------------------------------------------------------

def load_shap(indicator):

    indicator = indicator.lower()

    if indicator == "fcs":
        return load_fcs_shap()

    elif indicator == "rcsi":
        return load_rcsi_shap()

    elif indicator == "hhs":
        return load_hhs_shap()

    else:
        raise ValueError(
            "Unknown indicator."
        )