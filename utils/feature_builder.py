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

# ----------------------------------------------------------
# LOAD ALL MODEL COLUMNS
# ----------------------------------------------------------

all_model_columns = joblib.load(
    "models/all_model_columns.pkl"
)

# ==========================================================
# CREATE FEATURES
# ==========================================================

def create_features(model_inputs):

    """
    Converts forecast inputs into the feature dataframe
    expected by the trained models.

    Parameters
    ----------
    model_inputs : dict

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
    # ALIGN WITH TRAINING COLUMNS
    # ------------------------------------------------------

    df = df.reindex(

        columns=all_model_columns,

        fill_value=0

    )

    return df