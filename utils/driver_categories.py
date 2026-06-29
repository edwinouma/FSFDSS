# ==========================================================
# DRIVER CATEGORY CLASSIFICATION
# ==========================================================

def classify_driver(feature):

    feature = feature.lower()

    # ------------------------------------------------------
    # CLIMATE
    # ------------------------------------------------------

    if any(

        variable in feature

        for variable in [

            "rainfall",
            "ndvi",
            "river_level"

        ]

    ):

        return "Climate"

    # ------------------------------------------------------
    # MARKET
    # ------------------------------------------------------

    elif any(

        variable in feature

        for variable in [

            "goat_price",
            "rice_price",
            "sorghum_price",
            "water_price",
            "cmb"

        ]

    ):

        return "Market"

    # ------------------------------------------------------
    # CONFLICT
    # ------------------------------------------------------

    elif any(

        variable in feature

        for variable in [

            "conflict_incidents",
            "conflict_fatalities"

        ]

    ):

        return "Conflict"

    # ------------------------------------------------------
    # LIVELIHOOD
    # ------------------------------------------------------

    elif any(

        variable in feature

        for variable in [

            "herd_size",
            "crop_production",
            "debt_level"

        ]

    ):

        return "Livelihood"

    # ------------------------------------------------------
    # SPATIAL / TEMPORAL
    # ------------------------------------------------------

    elif any(

        variable in feature

        for variable in [

            "livelihood_zone_corrected",
            "livelihood_system",
            "year",
            "season"

        ]

    ):

        return "Spatial / Temporal"

    # ------------------------------------------------------
    # OTHER
    # ------------------------------------------------------

    else:

        return "Other"