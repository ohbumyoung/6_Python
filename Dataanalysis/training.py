# =====================================================
# 타이타닉 pandas 과제 - 빈칸 채우기 뼈대 (1~20번)
# -----------------------------------------------------
# 사용법
#   1) ___ 로 된 빈칸을 직접 채운다 (힌트는 주석 참고)
#   2) 실행 전에 "결과가 어떻게 나올지" 먼저 예측해 본다
#   3) 실행 후 예측과 비교하고, 각 문제 아래에 '# 내 설명:' 으로 한 줄 적는다
#   * 빈칸이 남아 있으면 NameError가 나므로, 문제 하나씩 채우며 실행할 것
# =====================================================
import pandas as pd

# ---------- A. 불러오기 · 탐색 ----------

# 1번: CSV 파일을 읽어 DataFrame으로 저장
#      (train.csv가 이 파일과 같은 폴더에 있어야 함)
df = pd.read_csv("train.csv")

# 2번: 상위 5개 행 출력
print(df.head())

# 3번: 열 이름 / 결측치 / dtype을 한 번에 확인
df.___()
# 내 관찰 1) 결측치가 있는 열과 개수:
# 내 관찰 2) dtype이 예상과 다르거나 주의할 열:


# ---------- B. 기초 통계 · 필터링 ----------

# 4번: Age, Fare의 평균 / 최솟값 / 최댓값
#      (힌트: 여러 통계를 한 번에 계산해 주는 메서드에 리스트를 넘긴다)
print(df[["Age", "Fare"]].___(["mean", "min", "max"]))

# 5번: 생존자(1) / 사망자(0) 수
#      (힌트: 값별 개수 세기)
print(df["Survived"].___())

# 6번: 객실 등급별 탑승객 수
print(df["Pclass"].___())

# 7번: 나이 50세 이상 탑승객만 추출 (새 DataFrame)
#      (힌트: 불리언 인덱싱, "이상"을 나타내는 비교 연산자)
over50 = df[df["Age"] ___ 50]
print(over50.shape)


# ---------- C. 파생 열 만들기 ----------

# 8번: 나이대 열 AgeGroup 추가
bins = [0, 10, 20, 30, 40, 50, 60, ___]        # 힌트: 맨 끝은 "무한대"
labels = ["아동", "10대", "20대", "30대", "40대", "50대", "60대 이상"]
# right=False 이면 구간이 [0, 10) 처럼 "이상~미만"이 된다
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=___)
# 주의: cut 결과는 '카테고리형'이라 새 값("미확인")을 바로 못 넣는다
#       힌트: 먼저 일반 문자열/객체형(object)으로 바꾼 뒤 결측을 채운다
df["AgeGroup"] = df["AgeGroup"].astype(___).fillna("미확인")
print(df[["Age", "AgeGroup"]].head())

# 12번: Sex의 male -> 0, female -> 1 로 Gender_Encoded 열 추가
#       (힌트: 딕셔너리를 받아 값을 바꿔주는 Series 메서드)
df["Gender_Encoded"] = df["Sex"].___({"male": 0, "female": 1})

# 15번: SibSp + Parch 로 FamilySize 열 추가 후 요약 통계 확인
df["FamilySize"] = df["SibSp"] ___ df["Parch"]
print(df["FamilySize"].___())                  # 힌트: count/mean/std/min/... 한 번에

# 16번: Name에서 호칭 추출 -> Title 열, 가장 흔한 5개 출력
#       (힌트: .str 접근자 + 정규식에서 괄호 그룹을 뽑아주는 메서드)
df["Title"] = df["Name"].str.___(r", ([A-Za-z]+)\.", expand=False)
print(df["Title"].value_counts().___(5))       # 힌트: 위에서 5개만


# ---------- D. 그룹화 · 집계 ----------

# 9번: 성별 x 객실 등급 기준 평균 생존율
print(df.groupby([___, "Pclass"])["Survived"].___())

# 10번: 나이대(AgeGroup)별 평균 생존율
print(df.groupby("AgeGroup")["Survived"].___())

# 13번: 탑승지(Embarked)별 평균 요금
print(df.groupby("___")["Fare"].mean())

# 14번: 피벗 테이블 (인덱스: Pclass, 컬럼: Sex, 값: Fare 평균)
pivot = pd.pivot_table(df, index="Pclass", columns="___", values="Fare", aggfunc="___")
print(pivot)

# 17번: Title별 승객 수 / 평균 나이 / 평균 생존율 (Named Aggregation)
#       형식:  새열이름=("대상열", "집계함수")
title_summary = df.groupby("Title").agg(
    승객수=("PassengerId", "___"),     # 힌트: 개수 세기
    평균나이=("Age", "___"),
    평균생존율=("Survived", "___"),
)
print(title_summary)


# ---------- E. 결측치 ----------

# 11번: 열별 결측치 개수와 비율(%)을 내림차순 출력
missing = df.isnull().___()                    # 힌트: True를 더하면 개수
ratio = missing / ___(df) * 100                # 힌트: 전체 행 수
missing_df = pd.DataFrame({"결측수": missing, "비율(%)": ratio})
print(missing_df.sort_values("결측수", ascending=___))

# 19번: Title + Pclass 그룹의 나이 중앙값으로 Age 결측치 대치
#       (16번을 먼저 실행해서 Title 열이 있어야 함)
group_median = df.groupby(["Title", "___"])["Age"].transform("___")
df["Age"] = df["Age"].fillna(group_median)
print(df["Age"].isnull().sum())
# 내 생각: 0이 아니라면 왜 남았을까? (힌트: 그 그룹 전체가 결측이면?)


# ---------- F. 시각화 ----------

# 18번: 생존/사망자 나이 분포 히스토그램 -> 이미지 파일로 저장
#       (주의: 19번 전에 실행하면 Age에 NaN이 있으므로 dropna 필요)
survived_age = df[df["Survived"] == 1]["Age"].dropna()
died_age = df[df["Survived"] == 0]["Age"].dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(survived_age, bins=20, alpha=0.5, label="생존")
ax.hist(died_age, bins=20, alpha=___, label="사망")   # 힌트: 겹쳐 보이게 투명도
ax.set_title("___")
ax.set_xlabel("___")
ax.set_ylabel("___")
ax.___()                                        # 힌트: 범례 표시
fig.___("age_distribution.png", dpi=150)        # 힌트: 파일로 저장
plt.close(fig)                                  # 화면 출력 없이 닫기

# 20번: 수치형 변수 상관관계 행렬 + 히트맵 -> 이미지 파일로 저장
num_cols = ["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
corr = df[num_cols].___()                       # 힌트: 상관관계 행렬

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=___, cmap="coolwarm", center=___, ax=ax)
ax.set_title("___")
fig.savefig("corr_heatmap.png", dpi=150, bbox_inches="tight")
plt.close(fig)