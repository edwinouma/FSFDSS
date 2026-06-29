# ==========================================================
# PREDICTION ENGINE
# ==========================================================
#
# Purpose
# -------
# Loads trained machine learning models and
# generates food security forecasts.
#
# Used by
# -------
# Baseline Forecast
# Scenario Analysis
# Automated Report
#
# ==========================================================

import joblib

from config.settings import (

    FCS_MODEL_PATH,
    RCSI_MODEL_PATH,
    HHS_MODEL_PATH

)

from utils.feature_builder import (

    create_features,
    fcs_features,
    rcsi_features,
    hhs_features

)


# ==========================================================
# LOAD TRAINED MODELS
# ==========================================================

fcs_model = joblib.load(FCS_MODEL_PATH)

rcsi_model = joblib.load(RCSI_MODEL_PATH)

hhs_model = joblib.load(HHS_MODEL_PATH)


# ==========================================================
# MODEL STATUS
# ==========================================================

def get_model_status():

    return {

        "FCS Model": type(fcs_model).__name__,
        "rCSI Model": type(rcsi_model).__name__,
        "HHS Model": type(hhs_model).__name__

    }


# ==========================================================
# GENERIC PREDICTION
# ==========================================================

def predict_model(

    model,
    feature_list,
    model_inputs

):

    """
    Generic prediction function.
    """

    features = create_features(

        model_inputs

    )

    features = features.reindex(

        columns=feature_list,
        fill_value=0

    )

    prediction = model.predict(

        features

    )[0]

    return float(prediction)


# ==========================================================
# INDIVIDUAL PREDICTIONS
# ==========================================================

def predict_fcs(model_inputs):

    return predict_model(

        fcs_model,
        fcs_features,
        model_inputs

    )


def predict_rcsi(model_inputs):

    return predict_model(

        rcsi_model,
        rcsi_features,
        model_inputs

    )


def predict_hhs(model_inputs):

    return predict_model(

        hhs_model,
        hhs_features,
        model_inputs

    )


# ==========================================================
# COMPLETE FORECAST
# ==========================================================

def predict_all(

    model_inputs,

    monthly_reference=None,

    seasonal_reference=None

):

    """
    Generates a complete forecast package.

    Returns
    -------
    Dictionary

    Contains

    Forecast metadata

    Predictions

    Data sources
    """

    results = {

        # ----------------------------------------------
        # Forecast Metadata
        # ----------------------------------------------

        "Forecast Year":

            model_inputs.get(

                "year"

            ),

        "Forecast Season":

            model_inputs.get(

                "season"

            ),

        "Livelihood Zone":

            model_inputs.get(

                "livelihood_zone_corrected"

            ),

        "Livelihood System":

            model_inputs.get(

                "livelihood_system"

            ),

        # ----------------------------------------------
        # Data References
        # ----------------------------------------------

        "Monthly Data Used":

            monthly_reference,

        "Seasonal Data Used":

            seasonal_reference,

        # ----------------------------------------------
        # Forecast Results
        # ----------------------------------------------

        "FCS":

            predict_fcs(

                model_inputs

            ),

        "rCSI":

            predict_rcsi(

                model_inputs

            ),

        "HHS":

            predict_hhs(

                model_inputs

            )

    }

    return results


# ==========================================================
# BASELINE VS SCENARIO
# ==========================================================

def compare_predictions(

    baseline_inputs,
    scenario_inputs,
    monthly_reference=None,
    seasonal_reference=None

):

    """
    Compare baseline and scenario forecasts.
    """

    baseline = predict_all(

        baseline_inputs,
        monthly_reference,
        seasonal_reference

    )

    scenario = predict_all(

        scenario_inputs,
        monthly_reference,
        seasonal_reference

    )

    return {

        "Baseline": baseline,

        "Scenario": scenario

    }