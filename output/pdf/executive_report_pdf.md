---
geometry: "a4paper, margin=0.7cm, top=0.65cm, bottom=0.65cm"
mainfont: "Noto Sans CJK JP"
CJKmainfont: "Noto Sans CJK JP"
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

# 科学的エグゼクティブレポート

\noindent\small\textbf{プロジェクト:} DHDEによる福井・北陸観光ガバナンス最適化\quad\textbf{日付:} 2026年3月1日\normalsize

\vspace{2pt}\noindent\rule{\linewidth}{0.3pt}\vspace{2pt}

## 1) 主要知見（1ページ要約）

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{構造課題}

\smallskip
福井は冬季観光で\textbf{47位}。問題は需要不足ではなく\textbf{計画摩擦}（高いデジタル意図が実来訪に転換しない構造）です。

\smallskip
\textbf{経済漏出（4ノード飽和）}

\smallskip
失われた来訪者は\textbf{865,917人/年}、機会損失は\textbf{約119.6億円/年}。冬季は夏季の\textbf{6.29倍}天候感度が高い。
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{予測妥当性}

\smallskip
東尋坊で来訪を\textbf{$R^2=0.810$}（調整済み0.802）で予測。最大説明変数はGoogle Directions意図（$r=0.781$）。JMA気象追加で\textbf{+5.6\%}精度向上。

\smallskip
\textbf{感性分析}

\smallskip
70,668件のテキストで、低満足層は「寂しい・閉まっている」語彙を\textbf{11.4倍}多用。福井の本質は過密ではなく\textbf{過少賑わい}。
\end{minipage}

\vspace{2pt}

## 2) 広域メカニズムと政策実装

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{広域連携の根拠}

\smallskip
石川の観光シグナルは福井来訪を先導（$r=0.537$）。単県最適化ではなく、\textbf{北陸広域ガバナンス}が必要。

\smallskip
\textbf{2つのAIナッジ}

\smallskip
(1) \textbf{供給側:} 72時間先の店舗活性アラート（営業時間・人員最適化）\\
(2) \textbf{需要側:} 悪天候時の耐候ルーティング（沿岸→屋内拠点）
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{到達目標}

\smallskip
定量漏出の回収により、観光順位は\textbf{47位→35位前後}への改善が現実的。

\smallskip
\textbf{結論}

\smallskip
DHDEは「損失定量→予測→施策」の実装ループを構築済み。政策導入に移行可能な状態にある。
\end{minipage}

\vspace{2pt}

\noindent\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../deep_analysis_fig5_rf_prediction_ja.png}
\captionof{figure}{\tiny 東尋坊における予測需要と実測来訪の高い一致（$R^2=0.810$）。}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{../rank_resurrection_projection_ja.png}
\captionof{figure}{\tiny 機会損失回収時の順位改善シナリオ（47位→約35位）。}
\end{minipage}

\vspace{2pt}\noindent\rule{\linewidth}{0.3pt}\vspace{2pt}

\scriptsize\noindent
\textbf{検証ステータス:} 4ノード（北/中央/南/東）で地理的飽和を達成し、政策実装フェーズへ移行可能。\quad\textbf{再現コード:} github.com/amilkh/hokuriku-tourism-ai-governance
