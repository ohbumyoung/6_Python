import pandas as pd

# 1번 문제
df = pd.read_csv("train.csv")

# 2번 문제
df.head()

# 3번 문제
df.info()

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
