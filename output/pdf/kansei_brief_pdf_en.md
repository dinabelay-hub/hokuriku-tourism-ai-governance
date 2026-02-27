---
geometry: "a4paper, margin=1.0cm, top=0.9cm, bottom=0.9cm"
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

# [Research Brief] Quantifying Regional Kansei and Optimizing People Flow with a Distributed Human Data Engine

\noindent\small\textbf{Author:} Amil Khanzada, Associate Professor, University of Fukui\quad\textbf{Target reader:} Kansei engineering specialist (Prof.\ Inoue)\quad\textbf{Date:} 2026-02-26\normalsize

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

\textbf{Objective:} This study uses \textbf{Soft Computing (Random Forest)} as the core and quantifies regional Kansei from the interaction of weather, travel intent, and on-site experience. Specifically, we model how: (1) physical environment (temperature, humidity, wind, snowfall), (2) visit intent (Google Directions) and local impression (satisfaction + Kansei text), propagate to people flow and economic loss. The main Tojinbo model achieved $R^2=0.810$, confirming that weather variables improve predictive performance.

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 1. Kansei Indicator: Under-vibrancy

Text-based Kansei analysis shows that expressions related to loneliness/emptiness are dominant in low-rated groups. In the integrated result, \textbf{the 1--2$\star$ group shows 11.4$\times$ higher under-vibrancy expression frequency} than the 4--5$\star$ group. Analysis used \textbf{Janome} morphological analysis with lemma-normalized adjective frequency comparison.

\begin{center}
\includegraphics[width=0.60\textwidth]{../kansei/fig_kansei_keywords_ja.png}
\captionof{figure}{\small Under-vibrancy keyword rates in 1$\star$ (Lonely) vs 5$\star$ (Vibrant), per 1,000 reviews.}
\end{center}

\vfill

## 2. Quietness Threshold at a Sacred Site (Eiheiji Case Study)

For Eiheiji, the relationship between relative density (0--100\%) and satisfaction was estimated using quadratic regression.

\begin{itemize}
  \setlength{\itemsep}{0pt}
  \item Model: $\hat{y}=ax^2+bx+c$
  \item Estimated coefficients: $a=1.857986\times10^{-5},\ b=-1.754081\times10^{-3},\ c=4.303838$
  \item Vertex (max satisfaction): $x^*=-\frac{b}{2a}=47.2\%$\quad Satisfaction at vertex: $\hat{y}(x^*)=4.26$
\end{itemize}

This is interpretable as a \textbf{fuzzy rule} for sacred-space experience management: policy should optimize for a density band that preserves quietness, rather than maximize volume alone.

\begin{center}
\includegraphics[width=0.60\textwidth]{../kansei/fig_eiheiji_threshold_ja.png}
\captionof{figure}{\small Quadratic fit of relative density vs satisfaction at Eiheiji (peak at 47.2\%).}
\end{center}

\vfill

## 3. Discomfort Index (DI) and Planning Friction / 4. Ishikawa--Fukui Pipeline: Hokuriku Impression Space

\textbf{DI Analysis:} After integrating JMA time series, we examined Discomfort Index, Wind Chill, and Satisfaction. A key finding is that DI works less as an on-site satisfaction driver and more as a \textbf{leading indicator of planning-stage friction}. Under poor weather, demand often drops first as visit cancellation before appearing as lower local ratings.

\textbf{Regional Linkage:} Cross-prefecture time-series coupling confirmed \textbf{Ishikawa-side signal $\rightarrow$ Fukui inflow} at $r\approx0.537$ (observed: 0.537). This supports treating Hokuriku as one integrated \textbf{Hokuriku Impression Space}. Policies should optimize inter-prefectural impression linkage---Kansei induction (expectation shaping) and mobility induction (behavior execution) should be jointly optimized.

\begin{center}
\includegraphics[width=0.70\textwidth]{../kansei/fig_di_heatmap_ja.png}
\captionof{figure}{\small Correlation heatmap among DI / Wind Chill / Satisfaction across four nodes.}
\end{center}

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## Coefficient Tables (Aligned with MANUSCRIPT\_METADATA)

\noindent\begin{minipage}[t]{0.57\textwidth}
\textbf{Table A. OLS Coefficients for 4 Nodes (Google Intent + Weather)}

\vspace{4pt}
\small
\begin{tabular}{lrrrr}
\toprule
Variable & Node A & Node B & Node C & Node D \\
\midrule
const       & 1382.3 & 4449.3 & nan & 11.7  \\
directions  & 1.478  & 0.853  & nan & 0.020 \\
temp        & 32.7   & $-$4.6   & nan & $-$2.0  \\
precip      & $-$71.7  & $-$1.5   & nan & $-$2.2  \\
wind        & $-$99.4  & $-$64.4  & nan & 2.1   \\
snow        & 0.0    & $-$25.1  & nan & $-$1.6  \\
\bottomrule
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[t]{0.38\textwidth}
\textbf{Table B. Eiheiji Quietness Threshold (Quadratic)}

\vspace{4pt}
\small
\begin{tabular}{lr}
\toprule
Coefficient & Value \\
\midrule
$a$               & $1.858\times10^{-5}$ \\
$b$               & $-1.754\times10^{-3}$ \\
$c$               & $4.3038$ \\
$x^*=-b/(2a)$     & $47.204$ \\
$\hat{y}(x^*)$    & $4.262$ \\
\bottomrule
\end{tabular}
\end{minipage}

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

\textbf{Conclusion (Research Implication):} This work reframes regional tourism from a ``visitor maximization problem'' to a \textbf{Kansei quality control problem}. The Eiheiji quietness threshold is a concrete quantitative bridge between cultural-value preservation and data-driven policy design, with strong potential for social implementation in Kansei informatics.
