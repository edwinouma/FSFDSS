import streamlit as st

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="FSFDSS",

    page_icon="🌍",

    layout="wide"

)

# ==========================================================
# HERO BANNER
# ==========================================================

st.markdown(

"""
<div style="
background: linear-gradient(90deg,#0B4F6C,#1E88E5);
padding:35px;
border-radius:12px;
margin-bottom:25px;
">

<h1 style="
color:white;
text-align:center;
margin-bottom:5px;
">

🌍 Food Security Forecasting and Decision Support System

</h1>

<h3 style="
color:#E8F4FD;
text-align:center;
margin-top:0px;
">

Machine Learning for Food Security Forecasting,
Early Warning and Decision Support

</h3>

<p style="
color:white;
font-size:18px;
text-align:center;
">

Forecasting Food Consumption Score (FCS),
Reduced Coping Strategy Index (rCSI),
and Household Hunger Scale (HHS)
across Somalia's livelihood zones.

</p>

</div>

""",

unsafe_allow_html=True

)

# ==========================================================
# QUICK OVERVIEW
# ==========================================================

st.info(

"""
### Welcome to FSFDSS

The Food Security Forecasting and Decision Support System (FSFDSS)
is an integrated web-based platform developed to support evidence-based
food security analysis through machine learning.

The platform combines historical food security data with environmental,
market, conflict and livelihood indicators to generate transparent,
interpretable and operational forecasts for Somalia.
"""

)


# ==========================================================
# PLATFORM HIGHLIGHTS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(

        "Forecast Indicators",

        "3"

    )

with c2:

    st.metric(

        "Analytical Modules",

        "7"

    )

with c3:

    st.metric(

        "Machine Learning",

        "XGBoost"

    )

with c4:

    st.metric(

        "Model Interpretation",

        "SHAP"

    )

st.markdown("---")

# ==========================================================
# PLATFORM OBJECTIVES
# ==========================================================

st.header("🎯 Platform Objectives")

st.markdown(
    """
    The Food Security Forecasting and Decision Support System (FSFDSS)
    was developed to support evidence-based food security analysis
    through machine learning forecasting and interactive decision support.
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        label="🍽 Forecast Outcome",

        value="FCS"

    )

    st.caption(

        "Predict Food Consumption Score across livelihood zones."

    )

with col2:

    st.metric(

        label="🥣 Forecast Outcome",

        value="rCSI"

    )

    st.caption(

        "Forecast household coping behaviour using the Reduced Coping Strategy Index."

    )

with col3:

    st.metric(

        label="⚠ Forecast Outcome",

        value="HHS"

    )

    st.caption(

        "Estimate Household Hunger Scale to identify food access constraints."

    )

with col4:

    st.metric(

        label="🧠 Machine Learning",

        value="XGBoost"

    )

    st.caption(

        "Optimised gradient boosting models trained on historical food security data."

    )

st.markdown("---")

# ==========================================================
# PLATFORM CAPABILITIES
# ==========================================================

st.header("🚀 Platform Capabilities")

cap1, cap2 = st.columns(2)

with cap1:

    st.success(

        """
        ✔ Forecast food security outcomes

        ✔ Assess forecast risk
        
        ✔ Monitor historical trends
        
        ✔ Explain predictions using SHAP

        """
    )

with cap2:

    st.success(

        """
        ✔ Evaluate alternative scenarios

        ✔ Generate executive reports

        ✔ Support IPC analysis

        ✔ Strengthen early warning systems

        """
    )

st.markdown("---")

# ==========================================================
# SYSTEM WORKFLOW
# ==========================================================

st.header("⚙️ System Workflow")

st.markdown(
"""
The Food Security Forecasting and Decision Support System (FSFDSS)
transforms multi-source food security information into actionable
forecasts through an integrated machine learning workflow.
"""
)

st.markdown("""

<style>

.workflow-card{

width:18%;

min-height:300px;

padding:20px;

border-radius:14px;

text-align:center;

font-family:Arial,sans-serif;

color:#1F2937;

box-shadow:0 6px 15px rgba(0,0,0,0.18);

transition:0.3s;

}

.workflow-title{

font-size:21px;

font-weight:bold;

margin-top:10px;

margin-bottom:18px;

}

.workflow-body{

font-size:15px;

line-height:1.8;

}

.arrow{

font-size:48px;

font-weight:bold;

color:#1976D2;

padding:0 6px;

}

</style>

<div style="display:flex;
align-items:center;
justify-content:space-between;
margin-top:25px;
margin-bottom:20px;">

<div class="workflow-card"
style="background:#E8F5E9;border-top:6px solid #2E7D32;">

<div style="font-size:48px;">📥</div>

<div class="workflow-title">

Data Sources

</div>

<div class="workflow-body">

IPC<br>

Climate<br>

Markets<br>

Conflict<br>

Livelihood

</div>

</div>

<div class="arrow">

➜

</div>

<div class="workflow-card"
style="background:#E3F2FD;border-top:6px solid #1976D2;">

<div style="font-size:48px;">⚙️</div>

<div class="workflow-title">

Feature Engineering

</div>

<div class="workflow-body">

Cleaning<br>

Integration<br>

Lag Variables<br>

Encoding

</div>

</div>

<div class="arrow">

➜

</div>

<div class="workflow-card"
style="background:#FFF8E1;border-top:6px solid #F9A825;">

<div style="font-size:48px;">🧠</div>

<div class="workflow-title">

Machine Learning

</div>

<div class="workflow-body">

XGBoost<br>

Feature Selection<br>

SHAP Analysis<br>

Model Validation

</div>

</div>

<div class="arrow">

➜

</div>

<div class="workflow-card"
style="background:#E1F5FE;border-top:6px solid #0288D1;">

<div style="font-size:48px;">📈</div>

<div class="workflow-title">

Forecasting & Risk

</div>

<div class="workflow-body">

FCS<br>

rCSI<br>

HHS<br>

Risk Assessment

</div>

</div>

<div class="arrow">

➜

</div>

<div class="workflow-card"
style="background:#F3E5F5;border-top:6px solid #8E24AA;">

<div style="font-size:48px;">🎯</div>

<div class="workflow-title">

Decision Support

</div>

<div class="workflow-body">

Historical Trends<br>

Scenario Analysis<br>

Situation Reports<br>

Early Warning

</div>

</div>

</div>

""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# FLOW INDICATOR
# ==========================================================

st.markdown(
    """
### ➜ Data Sources → Feature Engineering → Machine Learning → Forecasting → Decision Support
"""
)

st.markdown("---")

# ==========================================================
# PLATFORM MODULES
# ==========================================================

st.header("🧩 Platform Modules")

st.markdown(
    """
    FSFDSS consists of seven integrated analytical modules designed to
    support food security monitoring, forecasting and decision-making.
    """
)

# ==========================================================
# ROW 1
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.subheader("📊 Executive Dashboard")

        st.write(
            """
    Provides a national overview of current food security conditions,
    including key outcome indicators, dominant drivers and strategic
    decision-support summaries.
    """
        )

with col2:

    with st.container(border=True):

        st.subheader("🔮 Baseline Forecasting")

        st.write(
            """
    Generates baseline machine learning forecasts for
    Food Consumption Score (FCS), Reduced Coping Strategy
    Index (rCSI) and Household Hunger Scale (HHS) using
    trained XGBoost forecasting models.
    """
        )

# ==========================================================
# ROW 2
# ==========================================================

col3, col4 = st.columns(2)

with col3:

    with st.container(border=True):

        st.subheader("📈 Forecasting & Risk Assessment")

        st.write(
            """
    Generates baseline forecasts for Food Consumption Score (FCS),
    Reduced Coping Strategy Index (rCSI) and Household Hunger Scale (HHS),
    and automatically translates model outputs into operational food
    security risk categories together with decision-support recommendations.
    """
        )

with col4:

    with st.container(border=True):

        st.subheader("📈 Historical Trends")

        st.write(
            """
    Visualises historical food security trends across livelihood
    zones, allowing users to explore seasonal and long-term
    changes in outcome indicators.
    """
        )

# ==========================================================
# ROW 3
# ==========================================================

col5, col6 = st.columns(2)

with col5:

    with st.container(border=True):

        st.subheader("🔍 Key Drivers")

        st.write(
            """
    Explains machine learning predictions using SHAP values,
    identifying the most influential environmental, market,
    conflict and livelihood drivers.
    """
        )

with col6:

    with st.container(border=True):

        st.subheader("🧪 Scenario Analysis")

        st.write(
            """
    Allows users to simulate alternative climate, market,
    conflict and livelihood conditions to evaluate their
    potential impact on future food security outcomes.
    """
        )

# ==========================================================
# FINAL MODULE
# ==========================================================

with st.container(border=True):

    st.subheader("📄 Automated Situation Report")

    st.write(
        """
    Produces a professional executive report summarising
    historical food security conditions, national machine
    learning forecasts, key drivers, early warning priorities
    and evidence-based recommendations for decision-makers.
    """
    )

st.markdown("---")

# ==========================================================
# DATA SOURCES
# ==========================================================

st.header("📚 Data Sources")

st.markdown(
    """
The forecasting models integrate historical food security outcomes with
environmental, market, conflict and livelihood indicators collected from
multiple national and international data sources.
"""
)

col1, col2 = st.columns(2)

with col1:

    st.success(
        """
**Food Security & Livelihood**

• IPC Outcome Data

• FSNAU Household Assessments

• Livelihood Zone Information

• Household Debt Levels

• Herd Size

• Crop Production
"""
    )

with col2:

    st.success(
        """
**Climate, Markets & Conflict**

• Rainfall

• NDVI

• River Levels

• Food & Livestock Prices

• Cost of Minimum Basket (CMB)

• Conflict Incidents & Fatalities
"""
    )

st.markdown("---")

# ==========================================================
# MACHINE LEARNING FRAMEWORK
# ==========================================================

st.header("🧠 Machine Learning Framework")

left, right = st.columns(2)

with left:

    st.info(
        """
### Forecasting Model

• XGBoost Regression

• Feature Selection

• Lag-Based Predictors

• Cross-Validation

• Hyperparameter Optimisation
"""
    )

with right:

    st.info(
        """
### Model Interpretation

• SHAP Analysis

• Driver Categorisation

• Historical Monitoring

• Scenario Simulation

• Decision Support
"""
    )

st.markdown("---")

# ==========================================================
# ABOUT THE STUDY
# ==========================================================

st.header("🎓 About the Study")

st.markdown(
    """
This platform was developed as part of a **Master of Science research project**
to improve food security forecasting for Somalia using machine learning.

The study integrates historical food security outcome indicators with
environmental, market, conflict and livelihood information to generate
operational forecasts for:

- **Food Consumption Score (FCS)**
- **Reduced Coping Strategy Index (rCSI)**
- **Household Hunger Scale (HHS)**

Beyond forecasting, the platform provides model interpretation, historical
monitoring, scenario analysis and automated reporting to strengthen
evidence-based food security decision-making and support early warning.
"""
)

st.markdown("---")

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.header("ℹ️ System Information")

info1, info2, info3 = st.columns(3)

with info1:

    st.metric(

        "Forecast Outcomes",

        "3"

    )

with info2:

    st.metric(

        "Machine Learning Model",

        "XGBoost"

    )

with info3:

    st.metric(

        "Decision Support Modules",

        "7"

    )

st.markdown("---")

st.success(
"""
### 🌍 Vision

To strengthen food security early warning and decision-making through
transparent, interpretable and operational machine learning forecasting
that complements expert judgement and established analytical frameworks
such as the Integrated Food Security Phase Classification (IPC).
"""
)

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    """
**Food Security Forecasting and Decision Support System (FSFDSS)**

Version 1.0

Developed as part of a Master of Science research project on
machine learning for food security forecasting in Somalia.

© 2026
"""
)