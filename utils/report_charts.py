import os

import plotly.io as pio

# ==========================================================
# TEMP DIRECTORY
# ==========================================================

TEMP_FOLDER = "temp"

os.makedirs(

    TEMP_FOLDER,

    exist_ok=True

)

# ==========================================================
# EXPORT PLOTLY FIGURE
# ==========================================================

def save_plot(

    fig,

    filename,

    width=1400,

    height=800,

    scale=2

):

    """
    Export a Plotly figure to a high-resolution PNG.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure to export.

    filename : str
        Output image filename.

    width : int
        Image width in pixels.

    height : int
        Image height in pixels.

    scale : int
        Resolution multiplier.

    Returns
    -------
    str
        Full image path.
    """

    filepath = os.path.join(

        TEMP_FOLDER,

        filename

    )

    pio.write_image(

        fig,

        filepath,

        format="png",

        width=width,

        height=height,

        scale=scale,

        engine="kaleido"

    )

    return filepath


# ==========================================================
# EXPORT HISTORICAL TREND
# ==========================================================

def export_historical_chart(

    fig

):

    return save_plot(

        fig,

        "historical_trend.png"

    )


# ==========================================================
# EXPORT SHAP DRIVERS
# ==========================================================

def export_driver_chart(

    fig

):

    return save_plot(

        fig,

        "driver_analysis.png"

    )


# ==========================================================
# CLEAN TEMP FILES
# ==========================================================

def cleanup_temp_files():

    """
    Remove temporary exported charts.
    """

    if not os.path.exists(TEMP_FOLDER):

        return

    for file in os.listdir(TEMP_FOLDER):

        if file.endswith(".png"):

            try:

                os.remove(

                    os.path.join(

                        TEMP_FOLDER,

                        file

                    )

                )

            except Exception:

                pass