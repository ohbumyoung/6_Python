import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Malgun Gothic"

# 1번 문제
df = pd.read_csv("train.csv")

# 2번 문제 
#.head()의 기본값은 5이기 때문에 숫자를 안썼습니다.
df.head()


# 3번 문제
df.info()
"""
1. 결측치가 존재하는 열과 결측 개수
=> Age(177), Cabin(687), Embarked(2))
2. dtype이 예상과 다르거나 주의가 필요한 열
=> Age(float64) : 나이는 소수점이 될 수 없기 때문
"""

# 4번 문제 (차례대로 최대값, 최소값, 평균값)
print(df[["Age", "Fare"]].max())
print(df[["Age", "Fare"]].min())
print(df[["Age", "Fare"]].mean())

# 5번 문제
print(df["Survived"].value_counts())

# 6번 문제
print(df["Pclass"].value_counts().sort_index())

# 7번 문제
age50 = df[df["Age"] >= 50]
print(age50.shape)

# 8번 문제
# 조건식 if-else을 사용하여 풀었습니다.
def age_group(age):
    if pd.isna(age):
        return "미확인"
    elif age < 10:
        return "아동"
    elif age < 20:
        return "10대"
    elif age < 30:
        return "20대"
    elif age < 40:
        return "30대"
    elif age < 50:
        return "40대"
    elif age < 60:
        return "50대"
    else:
        return "60대 이상"
df["AgeGroup"] = df["Age"].apply(age_group)

# 9번 문제
print(df.groupby(["Sex", "Pclass"])["Survived"].mean())

# 10번 문제
print(df.groupby("AgeGroup")["Survived"].mean().round(2))

# 11번 문제
# 맨 밑 부분은 따로 볼 수 있게 만들었습니다.
NaN = df.isnull().sum()
result = NaN / 891 * 100
NaN_df = pd.DataFrame({"결측수": NaN, "비율(%)": result})
print(NaN_df.sort_values("결측수", ascending=False)) 
#print(result.sort_values(ascending=False), NaN.sort_values(ascending=False))

# 12번 문제 
# .map함수를 사용하여 풀었습니다.
df["Gender_Encoded"] = df["Sex"].map({"male":0, "female":1}) 
print(df["Gender_Encoded"])

# 13번 문제
print(df.groupby(["Embarked"])["Fare"].mean())

# 14번 문제
pivot = df.pivot_table(index="Pclass", columns="Sex", values="Fare", aggfunc="mean")
print(pivot)

# 15번 문제 
# 가족수에 본인을 포함시켜 +1을 사용했습니다.
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
print(df["FamilySize"].describe())


# 16번 문제
df["Title"] = df["Name"].str.extract(r', ([A-Za-z]+)\.')
print(df["Title"].head())

# 17번 문제
title_mean = df.groupby("Title").agg(
    승객수=("PassengerId", "count"),   
    평균나이=("Age", "mean"),
    평균생존율=("Survived", "mean"),
)
print(title_mean)

# 18번 문제
# pyplot을 사용하여 풀었습니다.
survived_age = df[df["Survived"] == 1]["Age"].dropna()
died_age = df[df["Survived"] == 0]["Age"].dropna()
 
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(survived_age, bins=20, alpha=0.5, label="생존")
ax.hist(died_age, bins=20, alpha=0.5, label="사망")
ax.set_title("생존 여부별 나이 분포")
ax.set_xlabel("나이")
ax.set_ylabel("승객 수")
ax.legend()
fig.savefig("age_distribution.png", dpi=150)
plt.close(fig)

# 19번 문제
df["Age"] = df["Age"].fillna(df.groupby(["Title", "Pclass"])["Age"].transform("median"))
print(df["Age"].isnull().sum())

# 20번 문제
# seaborn을 사용하여 풀었습니다.
num_cols = ["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
corr = df[num_cols].corr()
print(corr.round(2))
 
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
ax.set_title("수치형 변수 상관관계 히트맵")
fig.savefig("corr_heatmap.png", dpi=150, bbox_inches="tight")
plt.close(fig)