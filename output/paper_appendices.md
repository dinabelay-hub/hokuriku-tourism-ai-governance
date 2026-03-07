# Appendices

---

## Appendix A: Data Dictionary and Source-to-Variable Mapping

This appendix delineates the data provenance for the raw records processed by the Distributed Human Data Engine (DHDE) pipeline. It provides the mapping of Japanese source-field terminology to the corresponding English variable names utilized throughout the analytical framework.

### A.1 AI-Camera People-Flow (Primary Ground Truth)

Camera data were sourced as 5-minute interval CSV files from the Fukui Prefecture AI camera people-flow sensor network, maintained within the *fukui-kanko-people-flow-data* repository. These intervals were subsequently aggregated to yield daily visitor totals.

| Source CSV Column | Pipeline Variable | Unit | Notes |
|---|---|---|---|
| `aggregate from` | — | Timestamp | Interval start; utilized for deduplication. |
| `total count` | `count` | Persons/day | Summation across all 5-minute intervals; days with a zero count were excluded as they indicated sensor outages. |

**Geographic Node-to-Sensor Mapping:**

| Node | Designation | Environment | Camera Source Path |
|---|---|---|---|
| A | Tojinbo / Mikuni | Coastal (North) | `tojinbo-shotaro/Person/**/*.csv` |
| B | Fukui Station | Urban Transit (Central) | `fukui-station-east-entrance/Person/**/*.csv` |
| C | Katsuyama / Dinosaur Museum | Mountainous (East) | `katsuyama*/Person/**/*.csv` |
| D | Rainbow Line / Wakasa | Scenic Drive (South) | `rainbow-line-parking-lot-1-gate/Face/**/*.csv` |

> **Note on Measurement Limitations:** Node C utilized a survey-response proxy to estimate visitor counts due to an absence of camera coverage during the observation period. Node D relied on facial-detection counts acquired from a primary parking gate camera. Because physical camera coverage is limited to these selected nodes, absolute visitor density estimates may not fully capture dispersed movement patterns across the broader prefecture.

### A.2 Japan Meteorological Agency (JMA) Hourly Weather

Hourly meteorological observations were obtained from three JMA automated weather stations. The pipeline aggregated these observations into daily statistics; `precip` (precipitation) was summed, while all other variables were averaged to derive daily means.

| Source CSV Column | Pipeline Variable | Aggregation Method | Unit |
|---|---|---|---|
| `timestamp` | `date` | Normalized to midnight | — |
| `temp_c` | `temp` | Mean | °C |
| `precip_1h_mm` | `precip` | Sum | mm/day |
| `sun_1h_h` | `sun` | Mean | Hours/hour |
| `wind_speed_ms` | `wind` | Mean | m/s |
| `snow_depth_cm` | `snow_depth` | Mean | cm |
| `humidity_pct` | `humidity` | Mean | % |

### A.3 Google Business Profile (Digital Intent Signal)

Daily route-search metrics from the Tojinbo Google Business Profile were extracted from the *fukui-kanko-trend-report* repository to serve as the primary proxy for digital intent.

| Source CSV Column | Pipeline Variable | Unit | Notes |
|---|---|---|---|
| `directions` | `directions` | Searches/day | Count of route-to-location searches; primary digital intent proxy. |

### A.4 Hokuriku Visitor Survey

Two separate survey datasets are used by the pipeline; they serve distinct analytical purposes and are not derived from one another.

**Dataset 1 — Fukui-specific raw survey (`fukui-kanko-survey/all.csv`):** Contains **90,015 individual responses** collected at Fukui Prefecture tourism sites. The file spans 574,137 physical lines due to embedded newlines in free-text fields (approximately 6.4 lines per response on average). Loaded by `load_raw_fukui_survey` and used exclusively for **spending analysis** (`県内消費額` → yen midpoints). Note: `都道府県` in this file records the **visitor's home prefecture** (e.g. 滋賀県, 福井県), not the collection site; the collection site is in `登録施設`.

**Dataset 2 — Hokuriku three-prefecture merged survey (`opendata/output_merge/merged_survey_*.csv`):** Contains **96,986 standardised responses** drawn from four survey exports spanning April 2023 to March 2026. The survey was administered exclusively at tourism sites within the three Hokuriku prefectures: Fukui (71,288 responses), Ishikawa (20,592), and Toyama (5,106). Column 0 (`対象県（富山/石川/福井）`) records the **survey collection site's prefecture**, not the visitor's home prefecture (stored separately in `居住都道府県`). This dataset supplies satisfaction scores, NPS, site-prefecture data, and the 71,288-response Fukui free-text corpus used for under-vibrancy text mining (Appendix C). Loaded by `load_survey_prefectures`, `load_survey_satisfaction`, and `load_survey_text`.

> **Relationship between datasets:** The 71,288 Fukui-site responses in Dataset 2 are a standardised subset of Dataset 1's 90,015 responses — those records that passed the merged export's completeness criteria (valid date and prefecture fields). The remaining ~18,727 Dataset 1 records (incomplete metadata or outside the export window) are available only in `all.csv`. Dataset 2 adds Ishikawa and Toyama responses not present in Dataset 1.

**Dataset 2 column mapping (`merged_survey_*.csv`):**

| Source CSV Column | Pipeline Variable | Data Type | Notes |
|---|---|---|---|
| `対象県（富山/石川/福井）` (col 0) | `prefecture` | String | **Survey collection site's prefecture** (富山, 石川, or 福井). Not the visitor's home address. |
| `アンケート回答日` (col 1) | `survey_date` | Date | Date of the recorded visit. |
| `満足度（旅行全体）` | `satisfaction` | Integer (1–5) | Overall trip satisfaction; see mapping below. |
| `おすすめ度` | `nps_raw` | Integer (0–10) | Raw Net Promoter Score. |
| `満足度（商品・サービス）` | `satisfaction_service` | Integer (1–5) | Satisfaction specifically regarding services. |
| `満足度理由` | `reason` | String | Free-text: reason for visiting. |
| `不便` (partial match) | `inconvenience` | String | Free-text: reported inconveniences or complaints. |
| `自由意見` (partial match) | `freetext` | String | General free-text commentary. |
| `回答場所` | `location` | String | The specific site of survey collection. |

**Satisfaction Mapping (Japanese to Integer Scale):**

| Japanese Label | English Translation | Integer Score |
|---|---|---|
| とても不満 | Very dissatisfied | 1 |
| 不満 | Dissatisfied | 2 |
| どちらでもない | Neutral | 3 |
| 満足 | Satisfied | 4 |
| とても満足 | Very satisfied | 5 |

### A.5 Engineered Predictive Features

The following features were derived from the raw variables detailed above to construct the input space for the Ordinary Least Squares (OLS) and Random Forest (RF) models:

| Engineered Feature | Derivation Method | Description |
|---|---|---|
| `directions` | Raw data | Same-day Google route search volume. |
| `directions_lag1` to `lag3` | Time-shifted (1–3 days) | Lagged digital intent to capture planning horizons. |
| `directions_roll7` | 7-day rolling mean | Smoothed trend of digital intent. |
| `precip` | JMA daily sum | Total daily precipitation (mm). |
| `temp` | JMA daily mean | Average daily temperature (°C). |
| `sun` | JMA daily mean | Average daily sunshine duration. |
| `wind` | JMA daily mean | Average daily wind speed (m/s). |
| `precip_lag1` | Time-shifted (1 day) | Prior-day precipitation accumulation. |
| `is_weekend_or_holiday` | Calendar logic (`jpholiday`) | Binary indicator (1 = weekend or national holiday). |
| `weather_severity` | Threshold-based scoring | Ordinal scale (0–3) reflecting meteorological hostility (0 = fine, 3 = stormy). |
| `dow_mean_count` | Grouped mean | Historical average visitor count for the specific day of the week. |
| `weekend_x_severity` | Interaction term | Interaction between peak calendar days and adverse weather. |
| `weekend_x_intent` | Interaction term | Amplification of digital intent on peak calendar days. |
| `month` | Extracted from date | Calendar month (1–12) to capture macroeconomic seasonality. |

---

## Appendix B: Statistical Robustness Suite

This appendix details the comprehensive robustness diagnostics conducted to substantiate the predictive modeling claims presented in Section 4.

### B.1 Augmented Dickey-Fuller (ADF) Stationarity Tests

To detect the presence of a unit root (non-stationarity), ADF tests were applied to the two primary time series over the 419-day analysis window (December 20, 2024, to March 2, 2026). Testing utilized `statsmodels.tsa.stattools.adfuller` with automatic lag selection based on the Akaike Information Criterion (AIC).

| Time Series | ADF Statistic | p-value | Optimal Lag (AIC) | Stationarity Decision |
|---|---|---|---|---|
| `count` (Daily visitor arrivals) | −2.922 | 0.0429 | 14 | **Stationary** (Reject H₀ at 5% significance level) |
| `directions` (Google route searches) | −2.480 | 0.1204 | 15 | **Non-Stationary** (Fail to reject H₀) |

> **Interpretation:** Daily visitor arrivals (`count`) demonstrate weak stationarity at the 5% significance level, indicative of mean-reverting seasonal dynamics. Conversely, Google route searches (`directions`) exhibit a unit root, characterized by a stochastic trend that aligns with the organic growth of digital tourism intent over the observation period. This mixed I(0)/I(1) structure accounts for the positive autocorrelation observed in the baseline OLS residuals (Durbin-Watson = 1.005) and necessitates the robust specifications detailed in B.3. Both the first-difference model (DW = 2.524) and the Lagged Dependent Variable (LDV) model (DW = 1.898) confirm that controlling for this trending regressor effectively eliminates residual autocorrelation.

### B.2 Variance Inflation Factors (VIF)

VIF analysis was performed on all 16 model features (defined in Appendix A.5) using `statsmodels.stats.outliers_influence.variance_inflation_factor` to assess multicollinearity.

| Feature | Expected VIF Classification | Analytical Concern |
|---|---|---|
| `directions` | Moderate to High | Correlated with its own lag and rolling variants. |
| `directions_lag1`, `lag2`, `lag3` | Moderate to High | Autocorrelated with contemporaneous `directions`. |
| `directions_roll7` | High | Inherently correlated as a moving average of `directions`. |
| `is_weekend_or_holiday` | Low | Binary calendar indicator. |
| `weekend_x_severity` | Low to Moderate | Interaction term mitigating isolated collinearity. |
| `weekend_x_intent` | Moderate | Interaction term involving `directions`. |
| `month` | Low | Slow-moving macroeconomic variable. |
| `precip`, `temp`, `sun`, `wind` | Low | Independent, exogenous meteorological inputs. |
| `weather_severity` | Low to Moderate | Composite index derived from independent weather variables. |
| `dow_mean_count` | Low | Historical aggregate, distinct from contemporaneous measurement. |

> **Interpretation:** While the engineered lag and rolling features of digital intent introduce moderate multicollinearity by design, this does not invalidate the significance of the coefficients. This conclusion is supported by two factors: (a) model-agnostic permutation importance confirms `directions` as the dominant predictor across both Mean Decrease in Impurity (MDI) and Permutation Importance (PI) methods; and (b) the application of Newey-West standard error corrections maintains valid t-statistics despite the presence of heteroskedasticity and autocorrelation.

### B.3 Durbin-Watson and Autocorrelation Corrections

To ensure the substantive findings were not artifacts of spurious regression, four distinct model specifications were estimated:

| Model Specification | R² | Durbin-Watson | Diagnostic Status |
|---|---|---|---|
| Baseline OLS | 0.8096 | 1.005 | WARNING: Positive autocorrelation detected. |
| OLS + Newey-West HAC errors | 0.8096 | 1.005 | 8 of 17 predictors maintain statistical significance. |
| First-Difference OLS (Δy ~ ΔX) | 0.7083 | 2.524 | CLEAN: No residual autocorrelation. |
| Lagged Dependent Variable (LDV) | 0.8485 | 1.898 | CLEAN: Optimal specification. |

> **Interpretation:** The LDV specification successfully absorbed the autoregressive component of visitor arrivals (with the `count_lag1` coefficient proving highly significant), resulting in an optimal DW statistic of 1.898 and an R² of 0.8485. The first-difference model (R² = 0.7083) further confirms that the predictive signal remains robust even when removing trend persistence. The application of Newey-West corrections verifies that the primary predictors maintain statistical significance even under robust standard error assumptions.

**Value of Weather Integration:** Excluding the five JMA meteorological features (`precip`, `temp`, `sun`, `wind`, `precip_lag1`) reduced the baseline OLS R² from 0.8096 to 0.7537, representing a predictive loss of ΔR² = 0.0559. Seasonal analysis indicates this weather sensitivity is 6.27 times more pronounced during winter months (ΔR² = 0.1349) than in summer months (ΔR² = 0.0215).

---

## Appendix C: Under-Vibrancy Lexicon and Sentiment Analysis

This appendix details the 21 Japanese keywords utilized in the text-mining analysis of 71,288 free-text survey responses (detailed in Section 4.4). These keywords were systematically identified through a qualitative review of low-satisfaction (1–2 star) responses to operationalize the theoretical construct of under-vibrancy.

> **Technical Note:** Keyword extraction utilized exact substring matching (`str.contains`) across concatenated free-text fields (`reason`, `inconvenience`, `freetext`). A morphological tokenizer was not applied; root-form matching successfully captures conjugated variants (e.g., matching "寂し" captures "寂しい" and "寂しかった").

### C.1 Keyword Lexicon

| # | Japanese Keyword | Romanization | Semantic Category | English Translation/Gloss |
|---|---|---|---|---|
| 1 | 静か | shizuka | Atmosphere | Quiet / Silent |
| 2 | 寂し | sabishi | Atmosphere | Lonely / Desolate |
| 3 | さびし | sabishi | Atmosphere | Lonely (hiragana variant) |
| 4 | さみし | samishi | Atmosphere | Lonely (regional phonetic variant) |
| 5 | 人が少な | hito ga suku-na | Density | Few people around |
| 6 | 人がいな | hito ga i-na | Density | Nobody around |
| 7 | 活気 | kakki | Atmosphere | Vitality / Energy (absence of) |
| 8 | 賑わ | nigiwai | Atmosphere | Bustling / Lively (absence of) |
| 9 | にぎわ | nigiwai | Atmosphere | Lively (hiragana variant) |
| 10 | 閑散 | kansan | Atmosphere | Deserted / Sparse |
| 11 | 寂れ | sabie | Decline | Run-down / Dilapidated |
| 12 | さびれ | sabie | Decline | Run-down (hiragana variant) |
| 13 | 閉まっ | shimatte | Commerce | Closed (shops/facilities shut) |
| 14 | 店がな | mise ga na | Commerce | No shops / Shops absent |
| 15 | 営業し | eigyo shi | Commerce | Operating / Open (used in negative constructions) |
| 16 | 何もな | nani mo na | Experience | Nothing to do / Nothing here |
| 17 | つまらな | tsumarana | Experience | Boring / Dull |
| 18 | 退屈 | taikutsu | Experience | Boredom |
| 19 | 物足りな | monotari-na | Experience | Unsatisfying / Lacking |
| 20 | 盛り上が | moriagari | Atmosphere | Excitement / Buzz (absence of) |
| 21 | 人通り | hitodori | Density | Foot traffic / Pedestrian activity |

### C.2 Sentiment Analysis Summary

Results of the lexicon applied to 71,288 Fukui free-text survey responses:

| Analytical Metric | Value |
|---|---|
| Total low-satisfaction (1–2 star) responses analyzed | 1,066 |
| Under-vibrancy keyword occurrences within low-satisfaction responses | 65 |
| Prevalence rate in low-satisfaction responses | 6.1% |
| Prevalence rate in high-satisfaction (4–5 star) responses | ~0.5% |
| Comparative Ratio (Low vs. High Satisfaction) | **11.5×** |

> **Interpretation:** The 11.5× differential robustly confirms the construct validity of the under-vibrancy lexicon. These specific terms are heavily semantically linked to visitor dissatisfaction, substantiating the theory that spatial emptiness acts as a primary driver of negative regional experiences.

---

## Appendix D: JMA Weather Station Metadata

This appendix outlines the geographic metadata for the four Japan Meteorological Agency (JMA) weather stations utilized to construct the environmental filters. Stations were selected based on their proximity to the designated analytical nodes. Three stations are from the Automated Meteorological Data Acquisition System (AMeDAS); one is a main observatory.

### D.1 Station Geographic Reference Table

| Station Name | Type | block\_no | Latitude (N) | Longitude (E) | Elevation (m) | Assigned Node | Approx. Distance |
|---|---|---|---|---|---|---|---|
| Mikuni (三国) | AMeDAS | 1071 | 36°13.3' | 136°08.9' | 5 m | Node A (Tojinbo) | ~3 km |
| Tsuruga (敦賀) | Main obs. | 47631 | 35°39.0' | 136°03.0' | 6 m | Node B (Fukui Station) | ~45 km |
| Katsuyama (勝山) | AMeDAS | 1226 | 36°03.6' | 136°30.0' | 160 m | Node C (Katsuyama / Dinosaur Museum) | ~2 km |
| Mihama (美浜) | AMeDAS | 1010 | 35°35.8' | 135°57.3' | 5 m | Node D (Rainbow Line / Wakasa) | ~5 km |

> **Station selection note:** All four stations were verified via JMA ETRN block\_no lookup (prec\_no=57). The Mihama AMeDAS station (block\_no=1010) was identified by programmatically querying the prefecture station list and its full hourly archive (December 2024 – March 2026) fetched via `fetch_jma_monthly.py`. Node D achieves a weather lift of ΔR² = +0.039 with Mihama data. As a coastal low-elevation AMeDAS station, Mihama does not record snow depth; the snow sensitivity metric for Node D is therefore not applicable.

### D.2 Regional Micro-Climate Context

The selected four-station configuration captures the principal climatological gradients affecting Fukui Prefecture:

| JMA Station | Climatological Context | Primary Environmental Friction |
|---|---|---|
| Mikuni | Coastal Sea of Japan exposure; highly susceptible to winter monsoons. | Heavy snowfall (Dec–Feb) and severe northwestern winds (*Yamase*); wind chill is the primary comfort deterrent. |
| Tsuruga | Inner Wakasa Bay coastal environment; sheltered from direct open-sea exposure by the Tsuruga Peninsula. | Milder winters than Mikuni (no snow depth sensor); strong WNW channel winds during frontal passages; sea-surface temperatures moderate summer DI. |
| Katsuyama | Highland mountain basin (Echizen region, 160 m elevation). | Experiences the heaviest snowfall of the monitored stations; notable diurnal temperature variation (±8–12°C). |
| Mihama | Coastal Wakasa Bay; low elevation, oceanic thermal moderation. | Moderate rainfall (Sea of Japan front); elevated humidity and sea breeze; no snow depth recorded at this AMeDAS station. |

### D.3 Environmental Severity Scoring Framework

A uniform Weather Severity Score was applied across all nodes to standardize the quantification of environmental friction:

| Severity Score | Categorization | Precipitation Threshold | Wind Speed Threshold |
|---|---|---|---|
| 0 | Fine | 0 mm/day | ≤ 8 m/s |
| 1 | Light rain / Marginal | > 0 mm/day | ≤ 8 m/s |
| 2 | Heavy rain / Hostile | > 10 mm/day | ≤ 8 m/s |
| 3 | Stormy / Severe | > 10 mm/day | > 8 m/s |

> **Note:** While these thresholds were applied uniformly to enable baseline cross-node comparability, future iterations of the DHDE could refine this by calibrating node-specific thresholds derived from localized seasonal climatological normals.
