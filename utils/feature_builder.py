# ==========================================================
# FEATURE BUILDER
# ==========================================================

import pandas as pd
import joblib

# ==========================================================
# LOAD FEATURE LISTS
# ==========================================================

fcs_features = joblib.load(
    "models/fcs_features.pkl"
)

rcsi_features = joblib.load(
    "models/rcsi_features.pkl"
)

hhs_features = joblib.load(
    "models/hhs_features.pkl"
)

# ==========================================================
# LOAD MODEL COLUMNS
# ==========================================================

fcs_model_columns = joblib.load(
    "models/fcs_model_columns.pkl"
)

rcsi_model_columns = joblib.load(
    "models/rcsi_model_columns.pkl"
)

hhs_model_columns = joblib.load(
    "models/hhs_model_columns.pkl"
)

# ==========================================================
# CREATE FEATURES
# ==========================================================

def create_features(
    model_inputs,
    outcome
):

    """
    Converts forecast inputs into the feature dataframe
    expected by the requested trained model.

    Parameters
    ----------
    model_inputs : dict

    outcome : str

        "fcs"
        "rcsi"
        "hhs"

    Returns
    -------
    pandas.DataFrame
    """

    # ------------------------------------------------------
    # COPY INPUTS
    # ------------------------------------------------------

    data = model_inputs.copy()

    # ------------------------------------------------------
    # CREATE DATAFRAME
    # ------------------------------------------------------

    df = pd.DataFrame([data])

    # ------------------------------------------------------
    # AUTOMATIC ONE-HOT ENCODING
    # ------------------------------------------------------

    categorical_columns = []

    if "livelihood_zone_corrected" in df.columns:

        categorical_columns.append(
            "livelihood_zone_corrected"
        )

    if "livelihood_system" in df.columns:

        categorical_columns.append(
            "livelihood_system"
        )

    if "season" in df.columns:

        categorical_columns.append(
            "season"
        )

    if len(categorical_columns) > 0:

        df = pd.get_dummies(

            df,

            columns=categorical_columns

        )

    # ------------------------------------------------------
    # ALIGN TO MODEL-SPECIFIC COLUMNS
    # ------------------------------------------------------

    if outcome.lower() == "fcs":

        df = df.reindex(

            columns=fcs_model_columns,

            fill_value=0

        )

    elif outcome.lower() == "rcsi":

        df = df.reindex(

            columns=rcsi_model_columns,

            fill_value=0

        )

    elif outcome.lower() == "hhs":

        df = df.reindex(

            columns=hhs_model_columns,

            fill_value=0

        )

    else:

        raise ValueError(

            f"Unknown outcome: {outcome}"

        )

    return df