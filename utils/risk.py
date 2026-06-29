# ==========================================================
# RISK CLASSIFICATION
# ==========================================================

def classify_fcs(fcs):

    if fcs < 28:
        return "Poor"

    elif fcs < 42:
        return "Borderline"

    else:
        return "Acceptable"


def classify_rcsi(rcsi):

    if rcsi < 4:
        return "Low"

    elif rcsi < 18:
        return "Moderate"

    else:
        return "High"


def classify_hhs(hhs):

    if hhs < 1:
        return "Minimal"

    elif hhs < 2:
        return "Moderate"

    else:
        return "Severe"


def overall_risk(fcs, rcsi, hhs):

    fcs_class = classify_fcs(fcs)

    rcsi_class = classify_rcsi(rcsi)

    hhs_class = classify_hhs(hhs)

    severe_count = 0

    if fcs_class == "Poor":
        severe_count += 1

    if rcsi_class == "High":
        severe_count += 1

    if hhs_class == "Severe":
        severe_count += 1

    if severe_count >= 2:
        return "HIGH"

    elif severe_count == 1:
        return "MODERATE"

    else:
        return "LOW"