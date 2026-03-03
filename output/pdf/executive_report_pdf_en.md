---
geometry: "a4paper, margin=0.85cm, top=0.75cm, bottom=0.75cm"
mainfont: "Latin Modern Roman"
fontsize: 8pt
linestretch: 0.95
pagestyle: plain
header-includes: |
  \usepackage{booktabs}
  \usepackage{graphicx}
  \usepackage{caption}
  \usepackage{array}
  \captionsetup{font=scriptsize, skip=2pt, labelfont=bf}
  \setlength{\parskip}{2pt}
  \setlength{\parindent}{0pt}
  \setlength{\abovecaptionskip}{1pt}
  \setlength{\belowcaptionskip}{1pt}
  \renewcommand{\arraystretch}{1.0}
---

# Scientific Executive Report

\noindent\small\textbf{Project:} AI-driven demand forecasting and spatial optimization for Hokuriku tourism (Fukui Prefecture, Japan)\quad\textbf{Author:} Amil Khanzada, Associate Professor, University of Fukui\quad\textbf{Date:} February 27, 2026\normalsize

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 1. Problem / 2. Data Architecture (DHDE)

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{1. Problem: ``47th Place'' and Economic Loss}

\smallskip
Fukui Prefecture remains structurally weak in winter tourism (\textbf{47th/47}). Root cause is defined not as demand shortage but as ``\textbf{Planning Friction}''---a gap between high digital intent and low physical visits, driven by weather uncertainty and lack of vibrancy, creating an Opportunity Gap.
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{2. Distributed Human Data Engine (DHDE)}

\smallskip
Four data streams integrated: \textbf{Digital Intent} (Google search/route queries), \textbf{Environmental Filter} (JMA weather: temperature, precipitation, snow, wind), \textbf{Observed Data} (AI camera visitor counts), \textbf{Behavioral Sensor} (Hokuriku survey: 95,653 responses + 89,414 spending records).
\end{minipage}

\vfill

## 3. Key Results (Forecast Accuracy \& Kansei Threshold)

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{3.1 Forecast Performance \& Weather Shield Effect}

\smallskip
Accuracy: $R^2=0.810$ (adj.\ 0.802). 81\% of daily visitor variation explained. Top predictor: Google ``Directions'' intent ($r=0.781$). Adding JMA weather data boosts accuracy by +5.6\%, proving weather as an economic gatekeeper.
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{3.2 Under-vibrancy Paradox \& Sacred Site Threshold}

\smallskip
Text mining (70,668 reviews) reveals Fukui's essence is ``under-vibrancy.'' Low satisfaction (1--2$\star$) complaints about ``loneliness/closed shops'' are 11.4$\times$ more frequent. Tojinbo (nature) satisfaction rises with crowding; Eiheiji (sacred site) requires density management (threshold $\approx47\%$).
\end{minipage}

\vspace{4pt}

\noindent\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../deep_analysis_fig5_rf_prediction.png}
\captionof{figure}{\scriptsize Demand forecast (red) vs AI camera actual (blue). High agreement at $R^2=0.810$.}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../ultimate_fig2_vibrancy_threshold.png}
\captionof{figure}{\scriptsize Tojinbo (nature) vs Eiheiji (sacred site) vibrancy threshold.}
\end{minipage}

\vfill

## 4. Economic Impact \& Regional Linkage

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{4.1 Opportunity Loss: \textasciitilde\yen{}11.96B (4 Nodes)}

\smallskip
4 nodes (Tojinbo/North, Fukui Stn/Central, Katsuyama/South, Rainbow Line/East) achieved geographic saturation. Lost visitors: \textbf{865,917/year}. Estimated loss: \textbf{\textasciitilde\yen{}11.96B} (``Satake Number''). Winter sensitivity: \textbf{6.29$\times$} higher than summer.

\vspace{5pt}
\textbf{4.2 Ishikawa Pipeline (Regional Linkage Evidence)}

\smallskip
Ishikawa tourism activity strongly leads Fukui visits ($r=0.537$). Hokuriku functions as a single ecosystem---regional governance and joint grants are essential.
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../rank_resurrection_projection.png}
\captionof{figure}{\scriptsize AI governance recovers 865,917 lost visitors, improving rank from 47th to \textasciitilde{}35th.}
\end{minipage}

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 5. Policy Proposals / 6. Conclusion

\textbf{Policy (Recovering \textasciitilde\yen{}11.96B in lost demand):}\quad\textbf{(1) Supply-side Nudge} (Shop Activation Alert): Optimize opening hours/staffing 72 hours ahead based on demand forecast.\quad\textbf{(2) Demand-side Nudge} (Weather Routing): Guide visitors from Tojinbo to indoor sites (Katsuyama, Eiheiji) during bad weather.

\begin{center}
\includegraphics[width=0.84\textwidth]{../weather_shield_network.png}
\captionof{figure}{\scriptsize 4-node weather shield network. Each node's weather sensitivity coefficients. Rainbow Line shows strongest seasonality (1.85$\times$) and snow impact ($\beta=-0.0916$).}
\end{center}

\textbf{Conclusion:} DHDE achieves \textbf{full geographic saturation} (north, central, south, east). Connecting forecasts to AI nudges can recover \textasciitilde\yen{}11.96B in demand, raising Fukui's tourism economy from \textbf{47th to \textasciitilde{}35th place}.

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

\scriptsize\noindent
\textbf{Validation Status:} All four camera nodes cover main tourist corridors, achieving geographic saturation. The ``Satake Number'' (\textasciitilde\yen{}11.96B) is quantified and ready for policy intervention as annual opportunity loss.\quad\textbf{Reproducible Code:} github.com/amilkh/hokuriku-tourism-ai-governance
