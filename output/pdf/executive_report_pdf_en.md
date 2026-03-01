---
geometry: "a4paper, margin=0.75cm, top=0.7cm, bottom=0.7cm"
classoption:
  - twocolumn
mainfont: "Latin Modern Roman"
fontsize: 8pt
linestretch: 0.98
pagestyle: plain
header-includes: |
  \usepackage{graphicx}
  \usepackage{caption}
  \captionsetup{font=scriptsize, skip=2pt, labelfont=bf}
  \setlength{\parskip}{2pt}
  \setlength{\parindent}{0pt}
  \setlength{\columnsep}{14pt}
---

# HOKURIKU TOURISM AI GOVERNANCE STRATEGY REPORT

**Project:** Demand Forecasting and Spatial Optimization in Hokuriku Tourism using the Distributed Human Data Engine (DHDE)  
**Date:** March 1, 2026

## Executive Summary

This report presents an integrated AI and data science framework for tourism policy optimization in Fukui and the wider Hokuriku region.

- **Core challenge:** Fukui remains **47th** in winter tourism volume; the root cause is **Planning Friction** rather than weak demand.
- **Quantified loss:** Across the 4-node monitored system, annual leakage reaches **865,917 lost potential visitors** and **~¥11.96B (~$77M)**.
- **Predictive validity:** At Tojinbo, the model predicts daily arrivals from digital intent with **$R^2=0.810$**, with weather adding **+5.6%** predictive gain.
- **Policy objective:** Combined supply- and demand-side AI nudges can support a realistic ranking shift from **47th to around 35th**.

## 1. Reframing the Problem: Structural Stagnation and Opportunity Loss

Conventional diagnosis emphasizes resource scarcity. Evidence here shows a conversion failure from digital intent to physical arrivals.

- High Google Search/Directions intent exists.
- Weather uncertainty blocks travel completion, especially in winter.
- Under-vibrancy (closed shops, low street vitality) reduces post-visit evaluation.

**Policy implication:** Prioritize conversion from existing intent, not only new resource creation.

## 2. Data Architecture: Distributed Human Data Engine (DHDE)

DHDE integrates four streams into one governance-ready analytical stack across Tojinbo, Fukui Station, Katsuyama, and Rainbow Line:

- Google Business Profile intent signals
- JMA weather observations
- AI camera ground-truth counts
- Hokuriku survey responses

## 3. Key Findings

### 3.1 Forecasting Physical Arrivals and Weather Shield Effect

- **Model fit:** $R^2 = 0.810$ (Adj. $R^2 = 0.802$)
- **Top predictor:** Google Directions intent ($r=0.781$)
- **Interpretation:** Weather operates as an economic gatekeeper and justifies weather-adaptive routing.

![Predicted vs Actual at Tojinbo](../deep_analysis_fig5_rf_prediction.png)
*Figure 1. Predicted demand and AI-camera observed arrivals align strongly at Tojinbo.*

### 3.2 Under-vibrancy Paradox and Sacred Quietude Threshold

- In 70,668 text responses, dissatisfied users mention “lonely/closed/deserted” expressions **11.4x** more often.
- At Eiheiji, fitted satisfaction curves indicate an optimal relative density near **47.2%**; beyond it, satisfaction declines.

![Vibrancy Threshold Contrast](../ultimate_fig2_vibrancy_threshold.png)
*Figure 2. Vibrancy threshold differs by destination type (natural vs sacred).* 

### 3.3 Economic Leakage Quantification

- **Lost visitors:** 865,917 annually
- **Opportunity loss:** ~¥11.96B annually
- **Seasonal fragility:** Winter demand is **6.29x** more weather-sensitive than summer

![Opportunity-gap Recovery Scenario](../rank_resurrection_projection.png)
*Figure 3. Estimated ranking recovery under leakage-closure scenario.*

## 4. Why Regional Cooperation is Mandatory

Cross-prefectural analysis shows Ishikawa activity is a significant lead indicator for Fukui arrivals (**$r=0.537$**), indicating one practical tourism sphere.

**Governance implication:** Single-prefecture optimization is structurally insufficient; Hokuriku-wide coordination is required.

## 5. Policy Design: Socio-Technical Nudge Loop

1. **Supply-side nudge (Merchant Vitality Alerts):** 72-hour forecasts trigger staffing/opening optimization on high-intent days.
2. **Demand-side nudge (Weather-resilient routing):** During adverse weather, route exposed-demand flows toward sheltered nodes.

![Weather Shield Governance Network](../weather_shield_network.png)
*Figure 4. Weather-shield routing architecture across the four-node governance system.*

**Conclusion:** DHDE provides quantified losses, validated forecasts, and implementable interventions to support measurable tourism recovery in Fukui.

**Reproducible code:** github.com/amilkh/hokuriku-tourism-ai-governance
