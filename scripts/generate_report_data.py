"""
generate_report_data.py
------------------------
Builds public/data/dashboard_data.json for the FTAS Executive Dashboard.
- Ingests monthly camera chunks (monthly/tojinbo-shotaro/Person/**/*.csv).
- Integrates Fukui Station hotel reservation telemetry (latest_rsv_sum.csv).
- Robust weather column mapper and safe imputation (prevents 0-row dropna drops).
- Fast time-series data loader bypassing heavy survey NLP text scrubbing.
- Full live JMA Bosai API fallback when local weather data is stale.
"""

from __future__ import annotations

import io
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.config import load_config, resolve_repo_path
from src.report import Reporter

JMA_AREA_CODE = "180000"
JMA_ENDPOINT = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{JMA_AREA_CODE}.json"
HOTEL_RESERVATION_URL = "https://code4fukui.github.io/fukui-station-kanko-reservation/latest_rsv_sum.csv"

WEATHER_FRESHNESS_THRESHOLD_DAYS = 3

RF_PARAMS = dict(
    n_estimators=300, max_depth=10, min_samples_leaf=5,
    random_state=42, n_jobs=-1,
)


def fetch_weather_forecast() -> list[dict]:
    """Fetch the 14-day weather forecast from the JMA Bosai API for Fukui."""
    req = urllib.request.Request(JMA_ENDPOINT, headers={"User-Agent": "FTAS-Dashboard/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[WARN] JMA fetch failed: {e}")
        return []

    forecast_days = []
    try:
        short_term = data[0]["timeSeries"][0]
        time_defines = short_term["timeDefines"]
        weather_area = short_term["areas"][0]
        weathers = weather_area.get("weathers", [])
        winds = weather_area.get("winds", [])
        pops_series = data[0]["timeSeries"][1] if len(data[0]["timeSeries"]) > 1 else None
        pops_defines = pops_series["timeDefines"] if pops_series else []
        pops_area = pops_series["areas"][0] if pops_series else {}
        pops = pops_area.get("pops", [])

        for i, date_str in enumerate(time_defines):
            date = date_str[:10]
            pop_value = None
            for j, pdate in enumerate(pops_defines):
                if pdate[:10] == date and j < len(pops) and pops[j]:
                    pop_value = int(pops[j])
                    break
            forecast_days.append({
                "date": date,
                "weather": weathers[i] if i < len(weathers) else None,
                "wind": winds[i] if i < len(winds) else None,
                "precipitation_pct": pop_value,
                "rain_risk": bool(pop_value is not None and pop_value >= 40),
            })
    except Exception as e:
        print(f"[WARN] Unexpected JMA response format: {e}")

    return forecast_days


def fetch_hotel_reservations() -> pd.DataFrame:
    """Fetch Fukui Station hotel reservation telemetry."""
    req = urllib.request.Request(HOTEL_RESERVATION_URL, headers={"User-Agent": "FTAS-Dashboard/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            csv_text = resp.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_text))
        date_col = next((c for c in df.columns if any(t in str(c).lower() for t in ["date", "visit", "日付", "年月"])), df.columns[0])
        df["date"] = pd.to_datetime(df[date_col]).dt.normalize()
        return df.sort_values("date").reset_index(drop=True)
    except Exception as e:
        print(f"[WARN] Failed to fetch hotel booking data: {e}")
        return pd.DataFrame()


def find_date_column(df: pd.DataFrame) -> str:
    """Detects the datetime column safely across varying datasets."""
    for c in df.columns:
        c_low = str(c).lower()
        if any(t in c_low for t in ["date", "日付", "年月", "time", "day", "jst", "datetime"]):
            if not any(neg in c_low for neg in ["name", "id", "node", "place", "location"]):
                return c
    return df.columns[0]


def standardize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Maps varied weather column names to standard keys and guarantees defaults."""
    df_clean = pd.DataFrame(index=df.index)
    
    col_mapping = {
        "precip": ["precip", "precipitation", "rain", "降水", "雨量"],
        "temp": ["temp", "temperature", "気温"],
        "sun": ["sun", "sunshine", "日照"],
        "wind": ["wind", "wind_speed", "風速"],
        "humidity": ["humidity", "humid", "湿度"],
    }
    
    defaults = {
        "precip": 0.0,
        "temp": 18.0,
        "sun": 5.0,
        "wind": 3.0,
        "humidity": 65.0,
    }

    for standard_name, aliases in col_mapping.items():
        found = False
        for c in df.columns:
            if any(alias in str(c).lower() for alias in aliases):
                df_clean[standard_name] = pd.to_numeric(df[c], errors="coerce")
                found = True
                break
        if not found:
            df_clean[standard_name] = defaults[standard_name]

    return df_clean


def load_core_time_series(cfg: dict) -> tuple[pd.DataFrame, str]:
    """Loads camera telemetry, JMA weather, and RSI signals from monthly chunks."""
    search_roots = [
        Path("."),
        Path(".."),
        Path("../.."),
        Path("C:/Users/Student"),
        Path("C:/Users/Student/hokuriku-tourism-ai-governance"),
    ]

    # 1. Load and aggregate all monthly camera CSVs for Tojinbo
    camera_files = []
    for root in search_roots:
        matches = list(root.glob("**/monthly/tojinbo-shotaro/Person/**/*.csv")) or \
                  list(root.glob("**/tojinbo-shotaro/Person/**/*.csv"))
        if matches:
            camera_files = matches
            break

    if not camera_files:
        raise FileNotFoundError("Cannot locate monthly/tojinbo-shotaro/Person CSV files.")

    dfs = []
    for f in camera_files:
        try:
            temp_df = pd.read_csv(f)
            dfs.append(temp_df)
        except Exception:
            continue

    if not dfs:
        raise ValueError("Could not read monthly camera CSV files.")

    cam_df = pd.concat(dfs, ignore_index=True)

    date_c = find_date_column(cam_df)
    count_candidates = [
        c for c in cam_df.columns
        if any(term in str(c).lower() for term in ["count", "人数", "total", "val", "value", "person", "num"])
        and c != date_c
    ]
    count_c = count_candidates[0] if count_candidates else [c for c in cam_df.columns if c != date_c][-1]

    # Parse and aggregate daily counts
    cam_df["date"] = pd.to_datetime(cam_df[date_c], errors="coerce").dt.normalize()
    cam_df["count"] = pd.to_numeric(cam_df[count_c], errors="coerce").fillna(0)
    cam_df = cam_df.dropna(subset=["date"])
    cam_df = cam_df[cam_df["count"] > 0].groupby("date", as_index=False)["count"].sum()
    cam_df = cam_df.sort_values("date").reset_index(drop=True)

    # 2. JMA Weather lookup
    jma_file = Path("jma/jma_mikuni_hourly_8.csv")
    if not jma_file.exists():
        jma_file = Path("../jma/jma_mikuni_hourly_8.csv")
    if not jma_file.exists():
        for root in search_roots:
            matches = list(root.glob("**/jma_mikuni_hourly_8.csv"))
            if matches:
                jma_file = matches[0]
                break

    jma_df = pd.read_csv(jma_file)
    jma_date_col = find_date_column(jma_df)
    jma_df["date"] = pd.to_datetime(jma_df[jma_date_col], errors="coerce").dt.normalize()
    jma_df = jma_df.dropna(subset=["date"])

    weather_standard = standardize_weather_columns(jma_df)
    weather_standard["date"] = jma_df["date"]
    jma_clean = weather_standard.groupby("date", as_index=False).mean()

    # 3. RSI Data lookup
    rsi_file = None
    for root in search_roots:
        matches = list(root.glob("**/fukui-kanko-trend-report/**/data/*.csv"))
        if matches:
            rsi_file = matches[0]
            break

    if not rsi_file or not rsi_file.exists():
        for root in search_roots:
            matches = list(root.glob("**/trend.csv"))
            if matches:
                rsi_file = matches[0]
                break

    if not rsi_file or not rsi_file.exists():
        raise FileNotFoundError("Cannot locate trend CSV in fukui-kanko-trend-report/public/data.")

    rsi_df = pd.read_csv(rsi_file)
    rsi_date_col = find_date_column(rsi_df)
    rsi_df["date"] = pd.to_datetime(rsi_df[rsi_date_col], errors="coerce").dt.normalize()
    rsi_df = rsi_df.dropna(subset=["date"])

    route_col = next((c for c in rsi_df.columns if "direction" in str(c).lower() or "route" in str(c).lower() or "東尋坊" in str(c)), None)
    if not route_col:
        route_col = [c for c in rsi_df.columns if c != "date" and c != rsi_date_col and pd.api.types.is_numeric_dtype(rsi_df[c])][0]

    rsi_clean = rsi_df[["date", route_col]].drop_duplicates("date")

    # Merge
    daily = pd.merge(cam_df[["date", "count"]], jma_clean, on="date", how="left")
    daily = pd.merge(daily, rsi_clean, on="date", how="left")
    daily[route_col] = daily[route_col].fillna(daily[route_col].median() if not daily[route_col].dropna().empty else 0.0)

    # Guarantee all standard weather columns are present and filled
    for col, default_val in [("precip", 0.0), ("temp", 18.0), ("sun", 5.0), ("wind", 3.0), ("humidity", 65.0)]:
        if col not in daily.columns:
            daily[col] = default_val
        else:
            daily[col] = daily[col].ffill().bfill().fillna(default_val)

    return daily.sort_values("date").reset_index(drop=True), route_col


def is_local_weather_stale(daily: pd.DataFrame, threshold_days: int = WEATHER_FRESHNESS_THRESHOLD_DAYS) -> bool:
    if daily.empty:
        return True
    weather_cols = [c for c in ("temp", "precip", "wind") if c in daily.columns]
    if not weather_cols:
        return True
    has_weather = daily.dropna(subset=weather_cols, how="any")
    if has_weather.empty:
        return True
    last_weather_date = has_weather["date"].max()
    age_days = (pd.Timestamp(datetime.utcnow().date()) - last_weather_date).days
    return age_days > threshold_days


def compute_pacing_status(current_bookings: float, model_forecast: float) -> dict:
    rate = 0.0 if model_forecast == 0 else current_bookings / model_forecast
    if rate >= 1.20:
        badge, label = "HOT", "Superb"
    elif rate >= 0.80:
        badge, label = "OK", "Strong"
    elif rate >= 0.60:
        badge, label = "WARN", "Warning"
    else:
        badge, label = "CRIT", "Critical"
    return {"rate": round(rate, 4), "badge": badge, "label": label}


def build_features(daily: pd.DataFrame, route_col: str):
    import jpholiday
    df = daily.sort_values("date").reset_index(drop=True).copy()
    df["dow"] = df["date"].dt.dayofweek
    df["is_weekend"] = df["dow"].isin([5, 6]).astype(int)
    df["is_holiday"] = df["date"].apply(lambda d: int(jpholiday.is_holiday(d.date())))
    df["is_weekend_or_holiday"] = ((df["is_weekend"] == 1) | (df["is_holiday"] == 1)).astype(int)
    df["month"] = df["date"].dt.month
    
    precip = df["precip"].fillna(0.0)
    wind = df["wind"].fillna(0.0)
    df["weather_severity"] = (
        (precip > 0).astype(int) + (precip > 10).astype(int) + (wind > 8).astype(int)
    ).clip(upper=3)

    for lag in range(1, 4):
        df[f"{route_col}_lag{lag}"] = df[route_col].shift(lag).bfill().fillna(0.0)
    df[f"{route_col}_roll7"] = df[route_col].rolling(7, min_periods=1).mean().bfill().fillna(0.0)
    df["precip_lag1"] = precip.shift(1).bfill().fillna(0.0)
    df["weekend_x_severity"] = df["is_weekend_or_holiday"] * df["weather_severity"]
    df["weekend_x_intent"] = df["is_weekend_or_holiday"] * df[route_col].fillna(0.0)

    # Hotel reservation signals
    hotel_df = fetch_hotel_reservations()
    hotel_feature_names = [
        "hotel_reserve_lag1",
        "hotel_reserve_lag2",
        "hotel_reserve_roll7",
        "hotel_rooms_lag1",
        "hotel_people_lag1",
    ]

    if not hotel_df.empty:
        hotel_df["hotel_reserve_lag1"] = hotel_df["n_reserve"].shift(1).bfill().fillna(0.0)
        hotel_df["hotel_reserve_lag2"] = hotel_df["n_reserve"].shift(2).bfill().fillna(0.0)
        hotel_df["hotel_reserve_roll7"] = hotel_df["n_reserve"].shift(1).rolling(7, min_periods=1).mean().bfill().fillna(0.0)
        hotel_df["hotel_rooms_lag1"] = hotel_df["n_room"].shift(1).bfill().fillna(0.0)
        hotel_df["hotel_people_lag1"] = hotel_df["n_people"].shift(1).bfill().fillna(0.0)

        cols_to_merge = ["date"] + hotel_feature_names
        df = pd.merge(df, hotel_df[cols_to_merge], on="date", how="left")
        df[hotel_feature_names] = df[hotel_feature_names].fillna(0.0)
    else:
        for c in hotel_feature_names:
            df[c] = 0.0

    for c in ["precip", "temp", "sun", "wind"]:
        if c not in df.columns:
            df[c] = 0.0
        else:
            df[c] = df[c].fillna(0.0)

    feature_cols = [
        route_col, f"{route_col}_lag1", f"{route_col}_lag2", f"{route_col}_lag3",
        f"{route_col}_roll7", "precip", "temp", "sun", "wind", "precip_lag1",
        "is_weekend_or_holiday", "weather_severity", "weekend_x_severity",
        "weekend_x_intent", "month",
    ] + hotel_feature_names

    # Fill any remaining NaNs
    df[feature_cols] = df[feature_cols].ffill().bfill().fillna(0.0)

    return df, feature_cols


def train_and_predict(daily: pd.DataFrame, route_col: str):
    df, feature_cols = build_features(daily, route_col)
    clean = df[["date", "count"] + feature_cols].dropna().reset_index(drop=True)
    split_idx = int(len(clean) * 0.80)
    train = clean.iloc[:split_idx]
    
    model = RandomForestRegressor(**RF_PARAMS)
    model.fit(train[feature_cols], train["count"])
    
    clean = clean.copy()
    clean["forecast"] = model.predict(clean[feature_cols])
    return clean[["date", "count", "forecast"]], model, feature_cols


def build_estimated_outlook(daily: pd.DataFrame, route_col: str, model, feature_cols: list[str]) -> list[dict]:
    live_forecast = fetch_weather_forecast()
    if not live_forecast or daily.empty:
        return []

    weather_cols = [c for c in ("temp", "precip", "wind") if c in daily.columns]
    with_weather = daily.dropna(subset=weather_cols, how="any") if weather_cols else daily
    recent = with_weather.sort_values("date").tail(7)
    if recent.empty:
        return []

    baseline_temp = recent["temp"].mean() if "temp" in recent else 20.0
    baseline_sun = recent["sun"].mean() if "sun" in recent else 5.0
    baseline_wind = recent["wind"].mean() if "wind" in recent else 3.0
    recent_route_values = daily.sort_values("date")[route_col].dropna().tail(7).tolist()

    hotel_df = fetch_hotel_reservations()
    if not hotel_df.empty:
        recent_hotel = hotel_df.tail(7)
        base_hotel_reserve = float(recent_hotel["n_reserve"].mean()) if "n_reserve" in recent_hotel else 0.0
        base_hotel_room = float(recent_hotel["n_room"].mean()) if "n_room" in recent_hotel else 0.0
        base_hotel_people = float(recent_hotel["n_people"].mean()) if "n_people" in recent_hotel else 0.0
    else:
        base_hotel_reserve = base_hotel_room = base_hotel_people = 0.0

    rows = []
    import jpholiday
    for day in live_forecast:
        date = pd.to_datetime(day["date"])
        precip_estimate = 8.0 if day.get("rain_risk") else 0.0
        is_weekend = int(date.dayofweek in (5, 6))
        is_holiday = int(jpholiday.is_holiday(date.date()))
        is_weekend_or_holiday = int(is_weekend or is_holiday)
        weather_severity = min(
            3,
            int(precip_estimate > 0) + int(precip_estimate > 10) + int((baseline_wind or 0) > 8),
        )
        route_roll7 = sum(recent_route_values) / len(recent_route_values) if recent_route_values else 0
        lag_values = (recent_route_values[-3:] if len(recent_route_values) >= 3
                      else recent_route_values + [route_roll7] * (3 - len(recent_route_values)))

        feature_row = {
            route_col: route_roll7,
            f"{route_col}_lag1": lag_values[-1],
            f"{route_col}_lag2": lag_values[-2],
            f"{route_col}_lag3": lag_values[-3],
            f"{route_col}_roll7": route_roll7,
            "precip": precip_estimate,
            "temp": baseline_temp,
            "sun": baseline_sun,
            "wind": baseline_wind,
            "precip_lag1": precip_estimate,
            "is_weekend_or_holiday": is_weekend_or_holiday,
            "weather_severity": weather_severity,
            "weekend_x_severity": is_weekend_or_holiday * weather_severity,
            "weekend_x_intent": is_weekend_or_holiday * route_roll7,
            "month": date.month,
            "hotel_reserve_lag1": base_hotel_reserve,
            "hotel_reserve_lag2": base_hotel_reserve,
            "hotel_reserve_roll7": base_hotel_reserve,
            "hotel_rooms_lag1": base_hotel_room,
            "hotel_people_lag1": base_hotel_people,
        }
        X = pd.DataFrame([feature_row])[feature_cols]
        if X.isnull().any(axis=None):
            continue
        predicted = float(model.predict(X)[0])

        rows.append({
            "date": day["date"],
            "estimated_demand": round(predicted, 1),
            "weather": day.get("weather"),
            "precipitation_pct": day.get("precipitation_pct"),
            "rain_risk": day.get("rain_risk"),
            "is_estimated": True,
        })
    return rows


def build_summary(pred: pd.DataFrame) -> dict:
    last_date = pred["date"].max()

    def window_total(end_date, days):
        start = end_date - timedelta(days=days - 1)
        mask = (pred["date"] >= start) & (pred["date"] <= end_date)
        return pred.loc[mask, "count"].sum()

    current_30 = window_total(last_date, 30)
    prev_year_end = last_date - timedelta(days=365)
    previous_30 = window_total(prev_year_end, 30)
    diff = current_30 - previous_30
    yoy_pct = round((diff / previous_30 * 100), 2) if previous_30 else None
    this_week = pred[pred["date"] > last_date - timedelta(days=7)]
    this_week_pacing = compute_pacing_status(this_week["count"].sum(), this_week["forecast"].sum())

    return {
        "past_30_day": {
            "current_total": int(current_30),
            "previous_year_total": int(previous_30),
            "diff": int(diff),
            "yoy_pct": yoy_pct,
        },
        "this_week_pacing": this_week_pacing,
    }


def build_weekly_pacing(pred: pd.DataFrame) -> list[dict]:
    recent = pred.sort_values("date").tail(14)
    rows = []
    for _, r in recent.iterrows():
        status = compute_pacing_status(r["count"], r["forecast"])
        rows.append({
            "date": r["date"].strftime("%Y-%m-%d"),
            "actual": round(float(r["count"]), 1),
            "forecast": round(float(r["forecast"]), 1),
            **status,
        })
    return rows


def build_nudges(weather: list[dict], weekly_pacing: list[dict]) -> list[dict]:
    nudges = []
    for day in weather:
        if day.get("rain_risk"):
            nudges.append({
                "type": "weather", "date": day["date"],
                "message": "High rain probability — activate the indoor-activity plan and notify guests in advance.",
            })
    if weekly_pacing:
        last = weekly_pacing[-1]
        if last["badge"] in ("CRIT", "WARN"):
            nudges.append({
                "type": "demand", "date": last["date"],
                "message": "Below-expected pacing — activate an urgent 5-10% OTA discount.",
            })
        elif last["badge"] == "HOT":
            nudges.append({
                "type": "demand", "date": last["date"],
                "message": "Very high demand — raise rates and enable on-site upsell offers.",
            })
    return nudges


def build_dashboard_payload(cfg: dict, reporter: Reporter) -> dict:
    print("[1/4] Loading direct time-series feeds (Camera, JMA, RSI) ...")
    daily, route_col = load_core_time_series(cfg)
    print(f"      -> {len(daily)} merged time-series rows")

    print("[2/4] Checking weather freshness...")
    weather_is_stale = is_local_weather_stale(daily)
    if weather_is_stale:
        print("      -> Local weather is STALE. Fallback to live JMA forecast activated.")
    else:
        print("      -> Local weather is fresh.")

    print("[3/4] Training Random Forest with Hotel Booking Signals...")
    pred, model, feature_cols = train_and_predict(daily, route_col)

    print("[4/4] Fetching live 14-day weather forecast...")
    weather = fetch_weather_forecast()

    summary = build_summary(pred)
    weekly_pacing = build_weekly_pacing(pred)
    nudges = build_nudges(weather, weekly_pacing)

    demand_forecast = [
        {
            "date": r["date"].strftime("%Y-%m-%d"),
            "actual": round(float(r["count"]), 1),
            "forecast": round(float(r["forecast"]), 1),
        }
        for _, r in pred.sort_values("date").tail(60).iterrows()
    ]

    estimated_outlook = []
    if weather_is_stale:
        estimated_outlook = build_estimated_outlook(daily, route_col, model, feature_cols)

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summary": summary,
        "weather_strip": weather,
        "demand_forecast": demand_forecast,
        "weekly_pacing": weekly_pacing,
        "nudges": nudges,
        "weather_data_is_stale": weather_is_stale,
        "estimated_outlook": estimated_outlook,
    }


def export_json(payload: dict, cfg: dict) -> None:
    output_path = resolve_repo_path(cfg, "public", "data", "dashboard_data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[OK] dashboard_data.json written to {output_path}")


def main():
    cfg = load_config()
    reporter = Reporter(cfg)
    payload = build_dashboard_payload(cfg, reporter)
    export_json(payload, cfg)


if __name__ == "__main__":
    main()