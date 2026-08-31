"""
evaluate_hotel_impact.py
-------------------------
Fair out-of-sample chronological evaluation (80% train / 20% test)
comparing baseline model accuracy vs. hotel-augmented model accuracy
using local camera data and public/data/latest_rsv_sum.csv.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

RF_PARAMS = dict(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
)


def extract_date_and_count_columns(df: pd.DataFrame) -> tuple[str, str]:
    """Dynamically finds the date column and the count column from any DataFrame structure."""
    date_col = None
    count_col = None

    # 1. Search by common keywords
    for col in df.columns:
        col_str = str(col).lower()
        if any(k in col_str for k in ["date", "日時", "日付", "年月", "time", "day", "jst", "測定"]):
            if not any(neg in col_str for neg in ["name", "id", "node", "place"]):
                date_col = col
                break

    # 2. Fallback: inspect actual column values to find the datetime column
    if not date_col:
        for col in df.columns:
            sample = df[col].dropna().astype(str).head(10)
            if sample.empty:
                continue
            parsed = pd.to_datetime(sample, errors="coerce")
            if parsed.notnull().sum() >= len(sample) * 0.7:
                date_col = col
                break

    if not date_col:
        date_col = df.columns[0]

    # 3. Find count column
    for col in df.columns:
        if col == date_col:
            continue
        col_str = str(col).lower()
        if any(k in col_str for k in ["count", "人数", "total", "val", "value", "person", "num", "in", "合計"]):
            count_col = col
            break

    if not count_col:
        numeric_cols = [c for c in df.columns if c != date_col and pd.api.types.is_numeric_dtype(df[c])]
        count_col = numeric_cols[0] if numeric_cols else [c for c in df.columns if c != date_col][-1]

    return date_col, count_col


def load_local_data() -> pd.DataFrame:
    search_roots = [
        Path("."),
        Path(".."),
        Path("../.."),
        Path("C:/Users/Student"),
        Path("C:/Users/Student/hokuriku-tourism-ai-governance"),
    ]
    camera_files = []
    for root in search_roots:
        matches = list(root.glob("**/monthly/tojinbo-shotaro/Person/**/*.csv")) or \
                  list(root.glob("**/tojinbo-shotaro/Person/**/*.csv"))
        if matches:
            camera_files = matches
            break

    if not camera_files:
        raise FileNotFoundError("Could not find monthly Tojinbo camera CSV files.")

    dfs = []
    for f in camera_files:
        try:
            temp = pd.read_csv(f)
            dfs.append(temp)
        except Exception:
            continue

    cam_df = pd.concat(dfs, ignore_index=True)
    date_c, count_c = extract_date_and_count_columns(cam_df)

    cam_df["date"] = pd.to_datetime(cam_df[date_c], errors="coerce").dt.normalize()
    cam_df["count"] = pd.to_numeric(cam_df[count_c], errors="coerce").fillna(0)
    cam_df = cam_df.dropna(subset=["date"])
    cam_df = cam_df[cam_df["count"] > 0]
    daily = cam_df.groupby("date", as_index=False)["count"].sum().sort_values("date").reset_index(drop=True)

    # Calendar and baseline features
    daily["dow"] = daily["date"].dt.dayofweek
    daily["is_weekend"] = daily["dow"].isin([5, 6]).astype(int)
    daily["month"] = daily["date"].dt.month
    daily["count_lag1"] = daily["count"].shift(1).bfill().fillna(0)
    daily["count_lag7"] = daily["count"].shift(7).bfill().fillna(0)
    daily["count_roll7"] = daily["count"].rolling(7, min_periods=1).mean().shift(1).bfill().fillna(0)

    # Hotel reservation signals
    hotel_paths = [
        Path("public/data/latest_rsv_sum.csv"),
        Path("latest_rsv_sum.csv"),
        Path("public/data/latest_rsv_sum (5).csv"),
    ]
    hotel_file = next((p for p in hotel_paths if p.exists()), None)
    if not hotel_file:
        for root in search_roots:
            matches = list(root.glob("**/latest_rsv_sum*.csv"))
            if matches:
                hotel_file = matches[0]
                break

    if not hotel_file or not hotel_file.exists():
        raise FileNotFoundError("Cannot locate latest_rsv_sum.csv in public/data/ or root directory.")

    hotel_df = pd.read_csv(hotel_file)
    h_date_c = [c for c in hotel_df.columns if any(k in str(c).lower() for k in ["date", "visit", "日付", "年月"])][0]
    hotel_df["date"] = pd.to_datetime(hotel_df[h_date_c], errors="coerce").dt.normalize()
    hotel_df = hotel_df.sort_values("date").reset_index(drop=True)

    hotel_df["hotel_reserve_lag1"] = hotel_df["n_reserve"].shift(1).bfill().fillna(0)
    hotel_df["hotel_reserve_lag2"] = hotel_df["n_reserve"].shift(2).bfill().fillna(0)
    hotel_df["hotel_reserve_roll7"] = hotel_df["n_reserve"].shift(1).rolling(7, min_periods=1).mean().bfill().fillna(0)
    hotel_df["hotel_rooms_lag1"] = hotel_df["n_room"].shift(1).bfill().fillna(0)
    hotel_df["hotel_people_lag1"] = hotel_df["n_people"].shift(1).bfill().fillna(0)

    hotel_cols = ["date", "hotel_reserve_lag1", "hotel_reserve_lag2", "hotel_reserve_roll7", "hotel_rooms_lag1", "hotel_people_lag1"]
    merged = pd.merge(daily, hotel_df[hotel_cols], on="date", how="left")
    
    feature_cols_hotel = [c for c in hotel_cols if c != "date"]
    merged[feature_cols_hotel] = merged[feature_cols_hotel].ffill().bfill().fillna(0)

    return merged


def run_benchmark():
    df = load_local_data()

    baseline_features = [
        "dow",
        "is_weekend",
        "month",
        "count_lag1",
        "count_lag7",
        "count_roll7",
    ]

    hotel_features = [
        "hotel_reserve_lag1",
        "hotel_reserve_lag2",
        "hotel_reserve_roll7",
        "hotel_rooms_lag1",
        "hotel_people_lag1",
    ]

    augmented_features = baseline_features + hotel_features

    split_idx = int(len(df) * 0.80)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    y_train = train_df["count"]
    y_test = test_df["count"]

    # Model 1: Baseline
    rf_base = RandomForestRegressor(**RF_PARAMS)
    rf_base.fit(train_df[baseline_features], y_train)
    y_pred_base = rf_base.predict(test_df[baseline_features])

    r2_base = r2_score(y_test, y_pred_base)
    mae_base = mean_absolute_error(y_test, y_pred_base)
    rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))

    # Model 2: Augmented (with Hotel Features)
    rf_aug = RandomForestRegressor(**RF_PARAMS)
    rf_aug.fit(train_df[augmented_features], y_train)
    y_pred_aug = rf_aug.predict(test_df[augmented_features])

    r2_aug = r2_score(y_test, y_pred_aug)
    mae_aug = mean_absolute_error(y_test, y_pred_aug)
    rmse_aug = np.sqrt(mean_squared_error(y_test, y_pred_aug))

    print("\n" + "=" * 60)
    print("📊 HOTEL DATA IMPACT BENCHMARK (Out-of-Sample Test Set)")
    print("=" * 60)
    print(f"Test Set Size: {len(test_df)} days ({test_df['date'].min().strftime('%Y-%m-%d')} to {test_df['date'].max().strftime('%Y-%m-%d')})")
    print("-" * 60)
    print(f"{'Metric':<18} | {'Baseline (No Hotel)':<20} | {'With Hotel Data':<20} | {'Change':<10}")
    print("-" * 60)
    print(f"{'R² Score (↑)':<18} | {r2_base:<20.4f} | {r2_aug:<20.4f} | {r2_aug - r2_base:+.4f}")
    print(f"{'MAE (↓)':<18} | {mae_base:<20.1f} | {mae_aug:<20.1f} | {mae_aug - mae_base:+.1f}")
    print(f"{'RMSE (↓)':<18} | {rmse_base:<20.1f} | {rmse_aug:<20.1f} | {rmse_aug - rmse_base:+.1f}")
    print("-" * 60)

    importances = pd.Series(rf_aug.feature_importances_, index=augmented_features).sort_values(ascending=False)
    print("\n🔍 Feature Importances in Augmented Model:")
    for rank, (feat, val) in enumerate(importances.items(), 1):
        print(f"  {rank}. {feat:<24}: {val * 100:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()