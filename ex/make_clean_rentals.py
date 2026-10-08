# %% [markdown]
# # 전 실습: 정제 후 clean_rentals.csv 만들기 (STEP 1~6)
# 작업 폴더에 data/ 를 만들고 stations.csv, raw-bikes.csv, raw-rentals.csv 를 넣으세요.

# %% 읽기 (원본 그대로)
import unicodedata
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent

def read_raw(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)

stations = read_raw(BASE / "data" / "stations.csv")
bikes = read_raw(BASE / "data" / "raw-bikes.csv")
rentals = read_raw(BASE / "data" / "raw-rentals.csv")

# %% STEP 1. 진단
for name, d in [("stations", stations), ("bikes", bikes), ("rentals", rentals)]:
    print(name, d.shape)
print("bike_id 고유 수:", bikes["bike_id"].nunique(), "/ 중복 행:", bikes["bike_id"].duplicated().sum())
print("rental_id 중복:", rentals["rental_id"].duplicated().sum())
print(bikes["bike_type"].value_counts(dropna=False))
print(stations["district"].unique())
print(rentals["payment_method"].value_counts(dropna=False))

# %% 공통 함수
def norm(s):
    """NFKC로 전각->반각, 앞뒤 공백 제거 (NFKC 먼저)"""
    return unicodedata.normalize("NFKC", s).strip()

def to_num(series):
    """정규화 -> 콤마 제거 -> 숫자 변환 (실패는 NaN)"""
    s = series.map(norm).str.replace(",", "", regex=False)
    return pd.to_numeric(s, errors="coerce")

# %% STEP 2. 자전거 마스터 정제
b = bikes.copy()
for c in b.columns:
    b[c] = b[c].map(norm)

b["station_id"] = b["station_id"].str.upper().replace("", np.nan)

def unify_type(x):
    x = x.lower()
    if "전동" in x or x in ("e", "e-bike", "ebike", "electric", "electronic"):
        return "전동"
    return "일반"
# 주의: 위 매핑은 추정입니다. STEP 1에서 찍은 고유값을 보고 꼭 맞춰보세요.
b["bike_type"] = b["bike_type"].map(unify_type)

b["gear_count"] = b["gear_count"].str.extract(r"(\d+)")[0].astype(float).astype("Int64")
b["daily_fee"] = to_num(b["daily_fee"]).astype("Int64")
b["manufacture_year"] = to_num(b["manufacture_year"]).astype("Int64")

b = b.drop_duplicates(subset="bike_id", keep="first").reset_index(drop=True)
print("[STEP2] 행 수:", len(b), "(기대 50)")
print(b["bike_type"].unique(), b["station_id"].nunique(), b["station_id"].isna().sum())

# %% STEP 3. 대여 기록 정제
r = rentals.copy()
for c in ["rental_id", "bike_id", "user_id", "rent_time", "return_time", "payment_method"]:
    r[c] = r[c].map(norm)

r["distance_km"] = to_num(r["distance_km"])
r["fee"] = to_num(r["fee"])
r["rent_time"] = pd.to_datetime(r["rent_time"], format="mixed", errors="coerce")
r["return_time"] = pd.to_datetime(r["return_time"], format="mixed", errors="coerce")
r["payment_method"] = r["payment_method"].str.upper()

print("시각 변환 실패:", r["rent_time"].isna().sum(), r["return_time"].isna().sum())
r = r.drop_duplicates(subset="rental_id", keep="first").reset_index(drop=True)
print("[STEP3] 행 수:", len(r), "(기대 14,500) | distance 결측:", r["distance_km"].isna().sum(),
      "(기대 200) | fee 결측:", r["fee"].isna().sum(), "(기대 0)")
print(r["payment_method"].unique())

# %% STEP 4. 결합
n0 = len(r)
m = r.merge(b, on="bike_id", how="left", validate="many_to_one", indicator=True)
print("[STEP4] 결합 전/후:", n0, len(m))
print("매칭 실패:", (m["_merge"] == "left_only").sum(), "(기대 80)")
print(m.loc[m["_merge"] == "left_only", "bike_id"].value_counts().head())
m = m[m["_merge"] == "both"].drop(columns="_merge")

m = m.merge(stations, on="station_id", how="left", validate="many_to_one")
print("자치구 결측:", m["district"].isna().sum(), "(기대 304) | 행 수:", len(m), "(기대 14,500)")

# %% STEP 5. 이상치/논리 검사 (도메인 규칙)
m["duration_min"] = (m["return_time"] - m["rent_time"]).dt.total_seconds() / 60
speed = m["distance_km"] / (m["duration_min"] / 60)

rule1 = m["return_time"] <= m["rent_time"]
rule2 = m["fee"] < 0
rule3 = speed > 50
print("[STEP5] ①", rule1.sum(), "(50) ②", rule2.sum(), "(20) ③", rule3.sum(), "(650)")
bad = rule1 | rule2 | rule3
print("합계:", bad.sum(), "(719)")
m = m[~bad].copy()
print("제거 후 행 수:", len(m), "(13,701)")

# %% STEP 6. 결측 처리
# fee 복원: 분당요금 = daily_fee / 1440 (하루 1440분 기준)
m["fee"] = m["fee"].astype(float)
fee_na = m["fee"].isna()
if fee_na.any():
    m.loc[fee_na, "fee"] = (m.loc[fee_na, "duration_min"]
                            * m.loc[fee_na, "daily_fee"].astype(float) / 1440).round()
print("[STEP6] 요금 복원:", fee_na.sum(), "건 (기대 0)")

dist_na = m["distance_km"].isna().sum()
m = m.dropna(subset=["distance_km"]).reset_index(drop=True)
print("거리 결측 제거:", dist_na, "(200) | 최종 행 수:", len(m), "(13,501)")

# %% 저장
m.to_csv("clean_rentals.csv", index=False, encoding="utf-8-sig")
print(m.columns.tolist())
print("clean_rentals.csv 저장 완료")
