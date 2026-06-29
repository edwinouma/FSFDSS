import plotly.graph_objects as go

from utils.data_loader import load_data


# ==========================================================
# HISTORICAL + SCENARIO FORECAST
# ==========================================================

def plot_historical_forecast(

    zone,

    indicator,

    forecast_year,

    forecast_season,

    baseline_prediction,

    scenario_prediction

):

    """
    Displays historical food security outcomes together with
    the baseline and scenario forecast for the selected season.
    """

    # ------------------------------------------------------
    # LOAD HISTORICAL DATA
    # ------------------------------------------------------

    df = load_data()

    history = df[

        df["livelihood_zone_corrected"] == zone

    ].copy()

    history["season_order"] = history["season"].map(

        {

            "Gu": 1,

            "Deyr": 2

        }

    )

    # ------------------------------------------------------
    # PERIOD LABEL
    # ------------------------------------------------------

    history["Period"] = (

        history["year"].astype(str)

        + " "

        + history["season"]

    )

    # ------------------------------------------------------
    # FORECAST LABEL
    # ------------------------------------------------------

    forecast_period = f"{forecast_year} {forecast_season}"

    # ------------------------------------------------------
    # BUILD FIGURE
    # ------------------------------------------------------

    fig = go.Figure()

    # ======================================================
    # HISTORICAL TREND
    # ======================================================

    fig.add_trace(

        go.Scatter(

            x=history["Period"],

            y=history[indicator],

            mode="lines+markers",

            name="Historical",

            line=dict(

                width=3

            )

        )

    )

    # ======================================================
    # BASELINE FORECAST
    # ======================================================

    fig.add_trace(

        go.Scatter(

            x=[

                history.iloc[-1]["Period"],

                forecast_period

            ],

            y=[

                history.iloc[-1][indicator],

                baseline_prediction

            ],

            mode="lines+markers",

            name="Baseline Forecast",

            line=dict(

                dash="dash",

                width=3,

                color="#1f77b4"

            )

        )

    )

    # ======================================================
    # SCENARIO FORECAST
    # ======================================================

    fig.add_trace(

        go.Scatter(

            x=[

                history.iloc[-1]["Period"],

                forecast_period

            ],

            y=[

                history.iloc[-1][indicator],

                scenario_prediction

            ],

            mode="lines+markers",

            name="Scenario Forecast",

            line=dict(

                dash="dot",

                width=4,

                color="#d62728"

            )

        )

    )

    # ======================================================
    # FORECAST REGION
    # ======================================================

    ymax = max(

        history[indicator].max(),

        baseline_prediction,

        scenario_prediction

    ) * 1.08

    # ------------------------------------------------------
    # FORECAST SHADE
    # ------------------------------------------------------

    fig.add_vrect(

        x0=history.iloc[-1]["Period"],

        x1=forecast_period,

        fillcolor="rgba(255,215,0,0.12)",

        layer="below",

        line_width=0

    )

    # ------------------------------------------------------
    # DIVIDER
    # ------------------------------------------------------

    fig.add_vline(

        x=history.iloc[-1]["Period"],

        line_dash="dash",

        line_width=2

    )

    # ------------------------------------------------------
    # HISTORICAL LABEL
    # ------------------------------------------------------

    fig.add_annotation(

        x=history.iloc[len(history)//2]["Period"],

        y=ymax,

        text="<b>Historical</b>",

        showarrow=False,

        font=dict(

            size=14

        )

    )

    # ------------------------------------------------------
    # FORECAST LABEL
    # ------------------------------------------------------

    fig.add_annotation(

        x=forecast_period,

        y=ymax,

        text="<b>Forecast</b>",

        showarrow=False,

        font=dict(

            size=14,

            color="orange"

        )

    )

    # ------------------------------------------------------
    # BASELINE LABEL
    # ------------------------------------------------------

    fig.add_annotation(

        x=forecast_period,

        y=baseline_prediction,

        text="Baseline",

        showarrow=True,

        arrowhead=2,

        ax=35,

        ay=-25

    )

    # ------------------------------------------------------
    # SCENARIO LABEL
    # ------------------------------------------------------

    fig.add_annotation(

        x=forecast_period,

        y=scenario_prediction,

        text="Scenario",

        showarrow=True,

        arrowhead=2,

        ax=35,

        ay=25

    )

    # ======================================================
    # LAYOUT
    # ======================================================

    fig.update_layout(

        title=f"{indicator.upper()} Historical Trend with Baseline and Scenario Forecast",

        xaxis_title="Season",

        yaxis_title=indicator.upper(),

        hovermode="x unified",

        legend=dict(

            orientation="h",

            y=1.08

        ),

        height=550

    )

    return fig