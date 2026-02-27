---
geometry: "a4paper, margin=1.2cm, top=1.0cm, bottom=1.0cm"
mainfont: "Noto Sans CJK JP"
CJKmainfont: "Noto Sans CJK JP"
fontsize: 9pt
linestretch: 1.05
pagestyle: plain
header-includes: |
  \usepackage{booktabs}
  \usepackage{graphicx}
  \usepackage{caption}
  \usepackage{array}
  \captionsetup{font=scriptsize, skip=3pt, labelfont=bf}
  \setlength{\parskip}{3pt}
  \setlength{\parindent}{0pt}
  \setlength{\abovecaptionskip}{2pt}
  \setlength{\belowcaptionskip}{2pt}
  \renewcommand{\arraystretch}{1.0}
---

# 科学的エグゼクティブレポート

\noindent\small\textbf{プロジェクト:} 福井観光の需要予測と空間最適化を目的としたAI主導の分析\quad\textbf{著者:} 福井大学 特命助教 Amil Khanzada\quad\textbf{日付:} 2026年2月22日\normalsize

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 1. 課題 / 2. データアーキテクチャ（DHDE）

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{1. 課題：「47位」と経済的損失}

\smallskip
福井県は冬季の観光客数ランキングで構造的に弱い（\textbf{47位/47}）状態が続いています。根本原因を需要不足ではなく「\textbf{計画の摩擦（Planning Friction）}」と定義。デジタル上の訪問意図は高い一方、天候不確実性と現地の賑わい不足が実訪問を阻み、機会損失（Opportunity Gap）を生んでいます。
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{2. 分散型ヒューマンデータエンジン（DHDE）}

\smallskip
4データストリームを統合：\textbf{デジタルインテント}（Google検索・ルート）、\textbf{環境フィルター}（JMA気象：気温・降水・積雪・風）、\textbf{実測データ}（AIカメラ来訪者カウント）、\textbf{行動センサー}（北陸観光アンケート95,653件＋消費データ89,414件）。
\end{minipage}

\vfill

## 3. 主要結果（予測精度・感性閾値）

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{4.1 予測性能と気象シールド効果}

\smallskip
精度: $R^2=0.810$（調整済み 0.802）。日次来訪変動の81\%を説明。最大予測因子: Google「Directions」意図（$r=0.781$）。JMA気象データ追加で精度+5.6\%向上。天候は経済のゲートキーパー。
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\textbf{4.2 過少な賑わいパラドックスと聖地閾値}

\smallskip
70,668件のテキスト分析から、福井の本質は「過少な賑わい」と判明。低満足（1-2★）は「寂しい」不満が11.4倍多い。東尋坊は混雑で満足が上昇、永平寺は静寂閾値（相対密度$\approx47\%$）超過で満足が低下。
\end{minipage}

\vspace{4pt}

\noindent\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/output/deep_analysis_fig5_rf_prediction_ja.png}
\captionof{figure}{\scriptsize 需要予測（赤）とAIカメラ実測（青）の高い一致。$R^2=0.810$。}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/output/ultimate_fig2_vibrancy_threshold_ja.png}
\captionof{figure}{\scriptsize 東尋坊（自然拠点）vs 永平寺（聖地）の賑わい閾値。}
\end{minipage}

\vfill

## 4. 経済インパクトと広域連携

\noindent\begin{minipage}[t]{0.48\textwidth}
\textbf{4.3 機会損失：約119.6億円（4ノード）}

\smallskip
4ノード（東尋坊/北・福井駅/中央・勝山/南・レインボーライン/東）で地理的飽和を達成。失われた来訪者 \textbf{865,917人/年}、推定損失額 \textbf{約119.6億円}、冬季感度は夏季の \textbf{6.29倍}。

\vspace{5pt}
\textbf{4.4 石川パイプライン（広域連携の根拠）}

\smallskip
石川の観光活動が福井への来訪を先導する強い先行相関（$r=0.537$）を確認。北陸広域ガバナンスが必須であり、共同助成金の根拠となる。
\end{minipage}\hfill
\begin{minipage}[t]{0.48\textwidth}
\centering
\includegraphics[width=0.96\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/output/rank_resurrection_projection_ja.png}
\captionof{figure}{\scriptsize AIガバナンスで865,917人を回復すれば、47位から約35位へ順位改善。}
\end{minipage}

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 5. 提案施策 / 6. 結論

\textbf{施策（約119.6億円の漏出回収）:}　①\textbf{供給側ナッジ}（店舗活性アラート）: 72時間前の需要予測で営業時間・人員配置を最適化。　②\textbf{需要側ナッジ}（耐候ルーティング）: 悪天候時に東尋坊から屋内拠点（勝山・永平寺）へ誘導。

\begin{center}
\includegraphics[width=0.84\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/output/weather_shield_network_ja.png}
\captionof{figure}{\scriptsize 4ノード気象シールドネットワーク。各ノードの天候感度係数。レインボーラインは最強の季節性（1.85倍）と積雪影響（$\beta=-0.0916$）を示す。}
\end{center}

\textbf{結論:} DHDEは4つの地理ノードで完全飽和（北・中央・南・東）を達成。予測をAIナッジに接続することで、約119.6億円の需要を回復し、福井の観光経済を\textbf{47位から約35位}へ押し上げることが可能。

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

\scriptsize\noindent
\textbf{検証ステータス:} 主要観光回廊をカバーする4カメラノードで地理的飽和を達成。約119.6億円の「佐竹ナンバー」は政策介入への準備が整った年間機会損失。\quad\textbf{再現コード:} github.com/amilkh/hokuriku-tourism-ai-governance
