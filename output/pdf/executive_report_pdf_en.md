---
geometry: "a4paper, margin=0.7cm, top=0.65cm, bottom=0.65cm"
mainfont: "Latin Modern Roman"
fontsize: 7pt
linestretch: 0.92
pagestyle: plain
header-includes: |
  \usepackage{booktabs}
  \usepackage{graphicx}
  \usepackage{caption}
  \usepackage{array}
  \captionsetup{font=tiny, skip=1pt, labelfont=bf}
  \setlength{\parskip}{1.5pt}
  \setlength{\parindent}{0pt}
  \setlength{\abovecaptionskip}{0.5pt}
  \setlength{\belowcaptionskip}{0.5pt}
  \renewcommand{\arraystretch}{1.0}
---

# Scientific Executive Report

\noindent\small\textbf{Project:} DHDE-based tourism governance optimization for Fukui/Hokuriku\quad\textbf{Date:} March 1, 2026\normalsize

\vspace{2pt}\noindent\rule{\linewidth}{0.3pt}\vspace{2pt}

## 1) Core Findings (One-page Executive)

\noindent\begin{minipage}[t]{0.48\textwidth}
	extbf{Structural problem}

\smallskip
Fukui remains \textbf{47th} in winter tourism. The bottleneck is \textbf{Planning Friction}: high digital intent fails to convert into physical arrivals due to weather risk and low on-site vibrancy.

\smallskip
	extbf{Economic leakage (4-node saturation)}

\smallskip
Lost visitors: \textbf{865,917/year}. Estimated opportunity loss: \textbf{\textasciitilde\yen{}11.96B/year}. Winter demand is \textbf{6.29\texttimes} more weather-sensitive than summer.
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
	extbf{Model validity}

\smallskip
At Tojinbo, DHDE predicts daily arrivals at \textbf{$R^2=0.810$} (adj. 0.802). Top driver: Google Directions intent ($r=0.781$). Adding JMA weather improves accuracy by \textbf{+5.6\%}.

\smallskip
	extbf{Kansei evidence}

\smallskip
Across 70,668 texts, dissatisfied users mention ``lonely/closed'' signals \textbf{11.4\texttimes} more. Fukui's issue is under-vibrancy, not overtourism.
\end{minipage}

\vspace{2pt}

## 2) Regional Mechanism and Policy Response

\noindent\begin{minipage}[t]{0.48\textwidth}
	extbf{Regional linkage}

\smallskip
Ishikawa demand signals lead Fukui arrivals ($r=0.537$). This requires \textbf{Hokuriku-wide governance}, not single-prefecture optimization.

\smallskip
	extbf{Two AI nudges}

\smallskip
(1) \textbf{Supply-side:} 72h merchant activation alerts (hours/staffing).\\
(2) \textbf{Demand-side:} weather-resilient routing from exposed to sheltered nodes.
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
	extbf{Target outcome}

\smallskip
Recovering the quantified leakage supports a realistic ranking shift from \textbf{47th to around 35th}, with policy action linked directly to forecast signals.

\smallskip
	extbf{Conclusion}

\smallskip
DHDE is validation-ready for implementation: measurable loss, reproducible forecasts, and operational interventions are now integrated.
\end{minipage}

\vspace{2pt}

\noindent\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../deep_analysis_fig5_rf_prediction.png}
\captionof{figure}{\tiny Predicted vs actual daily arrivals at Tojinbo ($R^2=0.810$).}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../rank_resurrection_projection.png}
\captionof{figure}{\tiny Estimated rank recovery under opportunity-gap closure scenario.}
\end{minipage}

\vspace{2pt}\noindent\rule{\linewidth}{0.3pt}\vspace{2pt}

\scriptsize\noindent
	extbf{Validation status:} 4 nodes (north/central/south/east) are operationally saturated and policy-ready.\quad\textbf{Code:} github.com/amilkh/hokuriku-tourism-ai-governance
