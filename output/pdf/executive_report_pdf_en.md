---
geometry: "a4paper, margin=0.85cm, top=0.8cm, bottom=0.8cm"
classoption:
  - twocolumn
mainfont: "Latin Modern Roman"
fontsize: 7pt
linestretch: 0.94
pagestyle: plain
header-includes: |
  \usepackage{graphicx}
  \usepackage{booktabs}
  \usepackage{caption}
  \usepackage{titlesec}
  \titlespacing*{\section}{0pt}{4pt}{2pt}
  \titlespacing*{\subsection}{0pt}{3pt}{1pt}
  \titlespacing*{\subsubsection}{0pt}{2pt}{1pt}
  \captionsetup{font=tiny, skip=1pt, labelfont=bf}
  \setlength{\parskip}{1.2pt}
  \setlength{\parindent}{0pt}
  \setlength{\columnsep}{12pt}
---

\twocolumn[{%
\begin{center}
{\normalsize\textbf{HOKURIKU TOURISM AI GOVERNANCE}}\\[2pt]
{\scriptsize Distributed Human Data Engine (DHDE) \textbullet{} Demand Forecasting \& Spatial Optimization}\\[1pt]
{\scriptsize Amil Khanzada \quad Univ.\ of Fukui / Kanazawa Univ.\ \quad March 2026}
\end{center}
\vspace{3pt}
}]

## Executive Summary

- **Core challenge:** Fukui ranks **47th of 47 prefectures in winter tourism**, not from low demand but from planning friction: high digital intent that fails to convert into physical visits.
- **Quantified loss:** **865,917 lost visitors/year** across 4 monitored nodes; estimated economic leakage of **~¥11.96B (~$77M/year)**.
- **Predictive validity:** Daily arrivals at Tojinbo predicted from Google intent at **$R^2 = 0.810$**; adding weather data contributes an additional +5.6% gain.
- **Policy objective:** A dual-nudge AI system can realistically move Fukui from **47th to around 35th nationally**.

\begin{center}
\small\begin{tabular}{ll}
\toprule
\textbf{Key Metric} & \textbf{Value} \\
\midrule
OLS $R^2$ / Adj $R^2$ & 0.810 / 0.802 \\
RF 5-fold CV $R^2$ & 0.557 ± 0.131 \\
Top predictor & Google Directions ($r=0.781$) \\
Lost visitors (4 nodes) & 865,917/year \\
Opportunity loss & ¥11.96B (~\$77M/year) \\
Winter sensitivity & 6.29× vs summer \\
Ishikawa--Fukui lead $r$ & 0.537 \\
Under-vibrancy ratio & 11.4× \\
Current winter rank & 47th of 47 \\
\bottomrule
\end{tabular}
\end{center}

## 1. Problem Reframing: Structural Stagnation

Traditional policy framing emphasizes resource scarcity. Evidence here identifies a different mechanism: conversion failure from digital planning intent to physical arrival.

- Strong Google Search and Directions intent already exists for Fukui destinations.
- Weather uncertainty (snow/rain/wind) blocks trip completion in winter at 6.29× the summer suppression rate.
- Under-vibrancy (closed shops, empty streets, low atmospheric density) suppresses post-visit satisfaction and repeat-visit intent.

**Policy focus:** Raise conversion from existing latent demand, not only create new attractions.

## 2. DHDE Architecture

DHDE unifies four sensor streams into one governance-grade analytical system across four geographically saturated nodes (Tojinbo, Fukui Station, Katsuyama, Rainbow Line), covering coastal, urban, mountain, and scenic corridors.

- **Digital intent:** Google Business Profile (search + directions, 47 locations)
- **Environmental filter:** JMA weather observations (temp, precip, snow, wind, humidity)
- **Ground truth:** AI camera visitor counts at each node (5-min intervals, ~170K rows)
- **Behavioral sensor:** Hokuriku survey (95,653 responses) + Fukui spending records (~1M rows)

## 3. Key Findings

### 3.1 Predicting Physical Arrivals and Weather Shield Effect

- **Model fit:** $R^2 = 0.810$ (Adj. $R^2 = 0.802$); 81% of daily visitor variance explained.
- **Top predictor:** Google Directions intent from prior days ($r = 0.781$).
- **Weather value:** Adding JMA observations lifts model accuracy by +5.6%, establishing weather as an economic gatekeeper and justifying weather-adaptive routing policy.
- **Robustness:** First-difference $R^2 = 0.708$; LDV $R^2 = 0.848$; DW = 1.893 (clean residuals).

\begin{center}
\includegraphics[width=0.92\linewidth]{../deep_analysis_fig5_rf_prediction.png}

{\scriptsize Figure 1. High alignment between model-predicted demand and AI-camera ground-truth arrivals at Tojinbo.}
\end{center}

### 3.2 Under-vibrancy Paradox and Sacred Quietude Threshold

- Morphological analysis of 70,668 free-text responses reveals Fukui's challenge is under-tourism, not overtourism: Spearman $r_s = +0.161$ ($p = 0.001$) between visitor count and satisfaction confirms more visitors yield higher satisfaction.
- Low-satisfaction visitors (1--2 star) mention "lonely/closed/deserted" signals **11.4× more** than high-satisfaction visitors (4--5 star).
- At Eiheiji (sacred site), satisfaction peaks at relative density **~47.2%**; exceeding this threshold reduces satisfaction. Policy must optimize density quality, not maximize volume.
- At Tojinbo (natural site), visitor density positively correlates with satisfaction: crowding creates vibrancy.

\begin{center}
\includegraphics[width=0.92\linewidth]{../ultimate_fig2_vibrancy_threshold.png}

{\scriptsize Figure 2. Contrasting vibrancy thresholds: natural sites benefit from density; sacred sites require capping.}
\end{center}

### 3.3 Economic Leakage Quantification (¥11.96B Opportunity Gap)

Opportunity Gap is defined as the sum of lost visitors on weather-degraded days, days where model-predicted demand (from Google intent) exceeded actual AI-camera arrivals, scaled by mean visitor spending (¥13,811, from $n=95{,}653$ survey responses).

- **Gap days:** 207 per year at primary node; extrapolated across 4 nodes.
- **Lost visitors (4 nodes):** 865,917 annually.
- **Estimated opportunity loss:** ~¥11.96B/year (~$77M).
- **Seasonal fragility:** Winter demand is **6.29× more weather-sensitive** than summer, the highest ROI intervention window.

\begin{center}
\includegraphics[width=0.92\linewidth]{../rank_resurrection_projection.png}

{\scriptsize Figure 3. Estimated prefecture ranking recovery under opportunity-gap closure scenario (47th to ~35th).}
\end{center}

## 4. Regional Coordination Imperative: Ishikawa--Fukui Pipeline

Cross-prefectural CCF analysis reveals that Ishikawa daily tourism activity intensity is a statistically significant lead indicator for same-day physical arrivals at Fukui monitoring sites ($r = 0.537$). Ishikawa and Fukui form one practical Hokuriku Impression Space: tourists plan multi-prefecture itineraries, so demand flows across prefecture lines with a measurable lag structure. Single-prefecture optimization is structurally insufficient; coordinated Hokuriku-wide data governance is mandatory for full impact.

\begin{center}
\includegraphics[width=0.92\linewidth]{../deep_analysis_fig8_ishikawa_ccf.png}

{\scriptsize Figure 4. Cross-correlation profile: Ishikawa tourism activity as a lead indicator for Fukui arrivals ($r=0.537$).}
\end{center}

## 5. Policy Design: Socio-Technical Nudge Loop

To recover the ¥11.96B annual leakage, two AI nudges operating on a shared 72-hour demand forecast:

1. **Supply-side nudge (Merchant Vitality Alerts):** Forecast-triggered staffing and opening-hour optimization reduces "closed shop" dissatisfaction on high-intent days, directly addressing the 11.4× under-vibrancy gap.
2. **Demand-side nudge (Weather-Resilient Routing):** During adverse weather, coastal and outdoor demand (Tojinbo) is algorithmically rerouted toward sheltered or indoor nodes (Katsuyama, Eiheiji), retaining visitor spend within the Hokuriku sphere rather than losing it to cancellation.

\begin{center}
\includegraphics[width=0.92\linewidth]{../weather_shield_network.png}

{\scriptsize Figure 5. Four-node Weather Shield governance network with demand-routing paths.}
\end{center}

## 6. Implementation Roadmap and KPIs

The framework is structured for phased deployment with measurable checkpoints at each stage.

\begin{center}
\small\begin{tabular}{lll}
\toprule
\textbf{Phase} & \textbf{Scope} & \textbf{Target KPI} \\
\midrule
Phase 1 (0--6 mo) & Tojinbo + Fukui Station & Forecast MAPE $<$15\% \\
Phase 2 (7--12 mo) & Supply-side nudge live & Peak-day open rate +20\% \\
Phase 3 (Year 2) & All 4 nodes + routing & Lost visitors $-$100K/yr \\
Phase 4 (Year 3) & Full governance loop & Winter rank: 47th $\to$ $\sim$35th \\
\bottomrule
\end{tabular}
\end{center}

**Data governance:** All four node datasets (camera, JMA, Google, survey) are ingested into a unified pipeline versioned in the DHDE repository. Each month of JMA data is merged via upsert script; Kolmogorov--Smirnov drift detection flags statistical shifts between 3-month rolling windows before retraining. Schema validation, outlier detection (IQR + Z-score), and date-gap auditing run automatically on every pipeline execution, with all results written to `analysis_metrics.txt` for automated KPI tracking.

**Kansei quality dimension:** Beyond visitor counts, the nudge system targets satisfaction outcomes. The 11.4$\times$ under-vibrancy ratio and the Eiheiji density threshold (47.2\%) are embedded as secondary KPIs, measured in post-visit satisfaction scores from ongoing survey collection.

**Grant justification:** The Ishikawa--Fukui pipeline ($r=0.537$) and the 6.29$\times$ winter sensitivity ratio together justify a Hokuriku-wide grant rather than single-prefecture funding. At ¥13,811 mean spend per visitor, recovering even 30\% of the 865,917 annual lost visitors yields a direct revenue impact of ¥3.58B, substantially exceeding the expected AI infrastructure investment over a 3-year horizon.

## Conclusion

DHDE closes the full governance loop: quantified leakage, validated prediction, implementable nudge, and measurable KPI recovery. The 865,917 lost visitors and ¥11.96B annual opportunity loss are not projections but empirically bounded estimates derived from AI-camera ground truth, Google intent signals, JMA weather observations, and 95,653 survey responses across three prefectures. The positive visitor--satisfaction correlation ($r_s=+0.161$, $p=0.001$) confirms that recovery efforts will simultaneously address vibrancy, not just volume. The framework is policy-ready for phased execution starting at existing monitored nodes, building toward Fukui's winter ranking recovery from 47th to approximately 35th nationally within a 3-year governance horizon.

**Reproducible code:** github.com/amilkh/hokuriku-tourism-ai-governance
