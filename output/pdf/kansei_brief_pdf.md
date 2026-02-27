---
geometry: "a4paper, margin=1.3cm, top=1.2cm, bottom=1.2cm"
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
  \captionsetup{font=small, skip=3pt, labelfont=bf}
  \setlength{\parskip}{2pt}
  \setlength{\parindent}{0pt}
  \setlength{\abovecaptionskip}{2pt}
  \setlength{\belowcaptionskip}{2pt}
  \renewcommand{\arraystretch}{1.0}
---

# 【研究速報】分散型ヒューマンデータエンジンによる地域感性（Kansei）の定量化と人流最適化

\noindent\small\textbf{著者:} 福井大学 特命助教 Amil Khanzada\quad\textbf{想定読者:} 感性工学専門（井上先生）\quad\textbf{作成日:} 2026-02-26\normalsize

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

\textbf{目的:} 本研究は、\textbf{Soft Computing（Random Forest）} を中核に、天候・移動意図・現地体験の相互作用から、地域感性（Kansei）を定量化することを目的としています。物理環境（気温・湿度・風・降雪）が、来訪意思（Google Directions）と現地印象（満足度・感性テキスト）を介して、人流・経済損失にどのように連鎖するかを説明可能な形で統合しました。モデル精度は Tojinbo 主モデルで \textbf{$R^2=0.810$}。

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 1. 感性指標：過少な賑わい（Under-vibrancy）

テキスト感性分析により、低評価群（1-2★）において「寂しさ／閑散さ」関連表現が、高評価群（4-5★）の \textbf{11.4倍} 出現する構造を確認。形態素解析器 Janome を使用し、品詞（形容詞）ベースで語形正規化した頻度比較を実施。

\begin{center}
\includegraphics[width=0.60\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/kansei/fig_kansei_keywords_ja.png}
\captionof{figure}{\small 1★（Lonely）と5★（Vibrant）における過少な賑わい関連語の比較（1,000レビュー当たり出現率）。}
\end{center}

\vfill

## 2. 聖地における静寂の閾値（Eiheiji Case Study）

永平寺を対象に、相対密度（0〜100%）と満足度の関係を2次回帰で推定。推定ピーク密度 $x^*=47.2\%$（頂点満足度 $\hat{y}=4.26$）は、聖地体験保全のための\textbf{ファジィルール}として解釈可能。「高密度化そのもの」ではなく「静寂が維持される密度帯」を管理目標とする政策設計が妥当。

\begin{center}
\includegraphics[width=0.60\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/kansei/fig_eiheiji_threshold_ja.png}
\captionof{figure}{\small 永平寺における相対密度と満足度の2次回帰（ピーク: 47.2\%）。}
\end{center}

\vfill

## 3. 不快指数（DI）と計画摩擦 / 4. 石川・福井パイプライン：Hokuriku Impression Space

\textbf{DI分析:} JMA時系列を統合し、不快指数・体感温度・満足度の関係を検証。DIは「現地満足」よりも\textbf{来訪前の計画段階における摩擦（Planning Friction）}を先導する指標として機能する。

\textbf{広域連携:} 県境を跨ぐ時系列相関では、石川側シグナル→福井流入において $r\approx0.537$ を確認。北陸を一体の感性空間（\textbf{Hokuriku Impression Space}）として扱うべきことを示唆。感性誘導（期待形成）と移動誘導（行動実装）を同時最適化する必要がある。

\begin{center}
\includegraphics[width=0.70\textwidth]{/home/amil/active/hokuriku-tourism-ai-governance/kansei/fig_di_heatmap_ja.png}
\captionof{figure}{\small 4ノードにおける DI / 体感温度 / 満足度の相関ヒートマップ。}
\end{center}

\vfill

\vspace{3pt}\noindent\rule{\linewidth}{0.3pt}\vspace{3pt}

## 係数テーブル

\noindent\begin{minipage}[t]{0.57\textwidth}
\textbf{Table A. 4ノード OLS係数（Google意図 + 気象）}

\vspace{4pt}
\small
\begin{tabular}{lrrrr}
\toprule
変数 & Node A & Node B & Node C & Node D \\
\midrule
const       & 1382.3 & 4449.3 & nan & 11.7  \\
directions  & 1.478  & 0.853  & nan & 0.020 \\
temp        & 32.7   & -4.6   & nan & -2.0  \\
precip      & -71.7  & -1.5   & nan & -2.2  \\
wind        & -99.4  & -64.4  & nan & 2.1   \\
snow        & 0.0    & -25.1  & nan & -1.6  \\
\bottomrule
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[t]{0.38\textwidth}
\textbf{Table B. 永平寺静寂閾値（2次回帰）}

\vspace{4pt}
\small
\begin{tabular}{lr}
\toprule
係数 & 値 \\
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

\textbf{結語:} 本研究は、地域観光を「来訪者数の最大化問題」ではなく、\textbf{感性品質の最適制御問題}として再定義するものです。永平寺の静寂閾値は文化的価値保全とデータ駆動型政策の接点を与える定量指標であり、感性情報科学の社会実装に有効です。
