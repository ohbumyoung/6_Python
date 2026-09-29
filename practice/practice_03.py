# =============================================================================
# [0] 환경 설정 - 한글 폰트 깨짐 방지
# =============================================================================
import platform
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

if platform.system() == 'Windows':
    mpl.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # Mac
    mpl.rc('font', family='AppleGothic')
else:  # Linux (예: Colab)
    mpl.rc('font', family='NanumGothic')

mpl.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# =============================================================================
# [1] 가상 데이터셋 생성: 축구 선수 및 경기 데이터
# =============================================================================
import numpy as np
import pandas as pd

np.random.seed(42)

N = 260  # 총 행 수

teams = ['첼시FC', '맨체스터 시티', '멘체스터 유나이티드', '아스날FC',
         '뉴캐슬FC', '리버풀FC', '토트넘 홋스퍼FC', '에버턴FC']
positions = ['GK', 'DF', 'MF', 'FW']
position_probs = [0.10, 0.35, 0.35, 0.20]  # 포지션별 인원 비중(골키퍼 적음)

# 날짜: 2026-08-21 ~ 2027-05-30 사이 랜덤 경기일
date_range = pd.date_range('2026-08-21', '2027-05-30', freq='D')
match_date = np.random.choice(date_range, size=N)

team = np.random.choice(teams, size=N)
position = np.random.choice(positions, size=N, p=position_probs)

player_age = np.random.randint(18, 38, size=N)

# 출전 시간: 평소 0~90분, 이상치(데이터 오기입) 2건 포함
minutes_played = np.random.randint(0, 91, size=N).astype(float)

# 득점: 포지션에 따라 분포 다르게(대략적 근사)
goals = np.random.poisson(lam=0.15, size=N)
goals = np.where(position == 'FW', goals + np.random.poisson(0.3, N), goals)
goals = np.where(position == 'GK', 0, goals)

# 패스 성공률(%): 정규분포 근사, 70~95% 대
pass_success_rate = np.clip(np.random.normal(83, 6, size=N), 40, 99).round(1)

# 시장 가치(백만 유로): 로그정규분포로 현실적인 우측 꼬리 생성
market_value_million_eur = np.round(np.random.lognormal(mean=1.2, sigma=0.9, size=N), 2)

df = pd.DataFrame({
    'match_date': match_date,
    'team': team,
    'position': position,
    'player_age': player_age,
    'minutes_played': minutes_played,
    'goals': goals,
    'pass_success_rate': pass_success_rate,
    'market_value_million_eur': market_value_million_eur,
})

# -----------------------------------------------------------------------
# [1-1] 결측치 주입 (컬럼별 3~7% 수준)
# -----------------------------------------------------------------------
for col, ratio in [('position', 0.04), ('pass_success_rate', 0.06)]:
    missing_idx = df.sample(frac=ratio, random_state=1).index
    df.loc[missing_idx, col] = np.nan

# -----------------------------------------------------------------------
# [1-2] 이상치 주입 (비즈니스 관점에서 의심해볼 값)
# -----------------------------------------------------------------------
# (a) 출전 시간 오기입: 90분을 초과하는 비정상 값
outlier_idx_1 = df.sample(n=2, random_state=2).index
df.loc[outlier_idx_1, 'minutes_played'] = [180.0, 210.0]

# (b) 시장 가치 극단치: 슈퍼스타급 이적료(비정상적으로 튀는 값)
outlier_idx_2 = df.sample(n=2, random_state=3).index
df.loc[outlier_idx_2, 'market_value_million_eur'] = [180.5, 250.0]

df.to_csv('business_data.csv', index=False, encoding='utf-8-sig')
print(df.shape)
df.head()


# =============================================================================
# [과제 1] 결측치/이상치 점검 + 포지션별 핵심 지표 Bar Chart
# =============================================================================
# [비즈니스 문제 의도]
#   "우리 데이터는 신뢰할 수 있는가? 그리고 포지션별로 시장 가치에
#    유의미한 차이가 있는가?"
#   구단 프런트가 영입 전략을 세우기 전, 데이터 품질부터 점검하고
#   포지션별 평균 시장 가치를 파악하려 합니다.
#
# [분석 포인트 힌트]
#   - df.isnull().sum() / df.isnull().mean() 로 컬럼별 결측 비율 확인
#   - describe()로 minutes_played, market_value_million_eur의 min/max를 보고
#     "90분 초과", "비정상적으로 큰 값"이 있는지 의심해볼 것
#   - groupby('position')['market_value_million_eur'].mean() 후 bar chart

# ----------------------- TODO: 여기부터 작성 -----------------------
# 1) 결측치 비율 확인
# TODO: 컬럼별 결측 비율을 계산하세요
missing_ratio = df.isnull().sum() / len(df) * 100 
print(missing_ratio)

print('-'*60)

# 2) 이상치 의심 구간 확인 (예: minutes_played가 90 초과인 행)
 # TODO: 90분을 초과하는 행만 필터링하세요
suspect_minutes = df[df['minutes_played'] > 90]
print(suspect_minutes)

print('-'*60)

# 2-B) 이상치 의심 구간 확인 (2) - market_value_million_eur가 비정상적으로 큰 행
# 힌트: df['market_value_million_eur'].describe() 로 분포를 먼저 확인하고, 평균/75%값 대비 훨씬 큰 값을 기준으로 필터링해보세요.
# TODO: market_value_million_eur가 기준치를 초과하는 행만 필터링하세요
suspect_market_value = df[df['market_value_million_eur']>30]
print(suspect_market_value)

print('-'*60)
# 3) 포지션별 평균 시장 가치 집계
# TODO: position별 market_value_million_eur 평균
position_avg_value = df.groupby('position')['market_value_million_eur'].mean() 
superstars_out = df[df['market_value_million_eur'] <= 30]
position_avg_superstars_out = superstars_out.groupby('position')['market_value_million_eur'].mean()

print(f"전체포함:\n{position_avg_value}")
print(f"슈퍼스타 제외:\n{position_avg_superstars_out}")

print('-'*60)


# 4) Bar Chart 그리기
# TODO: sns.barplot() 또는 position_avg_value.plot(kind='bar') 로 시각화
# TODO: 제목, x/y축 라벨 추가
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='position', y='market_value_million_eur')

plt.title('포지션별 시장가치(슈퍼스타 2명 포함)')
plt.xlabel('포지션')
plt.ylabel('시장가치(백만유로)')

plt.savefig('과제1_포지션별_시장가치.png', dpi=150, bbox_inches='tight')
plt.close()
# --------------------------------------------------------------------


# =============================================================================
# [과제 2] 두 연속형 지표 간 상관관계 및 이상치 식별 Scatter Plot
# =============================================================================
# [비즈니스 문제 의도]
#   "출전 시간이 늘어날수록 시장 가치도 함께 오르는가?
#    아니면 이 상관관계를 깨는 이례적인 케이스(저출전-고가치 등)가 있는가?"
#
# [분석 포인트 힌트]
#   - x축: minutes_played, y축: market_value_million_eur
#   - hue='position' 으로 포지션별 패턴 구분
#   - 앞서 [과제 1]에서 발견한 이상치 행이 산점도 어디에 찍히는지 확인
#   - sns.scatterplot(data=..., x=..., y=..., hue=...)

# ----------------------- TODO: 여기부터 작성 -----------------------
plt.figure(figsize=(8, 6))
# TODO: seaborn scatterplot 작성 (hue='position')
# TODO: 이상치로 의심되는 점에 주석(annotate) 달아보기 (선택)
sns.scatterplot(data=df, x='minutes_played', y='market_value_million_eur', hue='position')

plt.title('출전시간 vs 시장가치(슈퍼스타 2명 포함)')
plt.xlabel('출전시간(분)')
plt.ylabel('시장가치(백만 유로)')

plt.savefig('과제2_산점도.png', dpi=150, bbox_inches='tight')
plt.close()
# --------------------------------------------------------------------


# =============================================================================
# [과제 3] 팀별 시장 가치 분포 비교 (Box Plot / Violin Plot)
# =============================================================================
# [비즈니스 문제 의도]
#   "어느 팀이 특별히 고가치 선수단을 보유하고 있고,
#    어느 팀이 선수단 가치 편차(분산)가 큰가?"
#   단순 평균만으로는 팀 내 선수단 구성의 불균형을 볼 수 없습니다.
#
# [분석 포인트 힌트]
#   - x='team', y='market_value_million_eur'
#   - Box Plot은 중앙값/사분위/이상치를, Violin Plot은 분포 형태(밀도)를 보여줌
#   - 팀 이름이 길면 plt.xticks(rotation=...) 필요

# ----------------------- TODO: 여기부터 작성 -----------------------
plt.figure(figsize=(10, 6))
# TODO: sns.boxplot() 또는 sns.violinplot() 으로 team별 분포 비교
# TODO: x축 라벨 회전 처리
sns.boxplot(data=df, x='team', y='market_value_million_eur')
plt.xticks(rotation=45)
plt.title('구단별 시장가치(슈퍼스타 2명 포함)')
plt.xlabel('구단')
plt.ylabel('시장가치(백만유로)')

plt.savefig('과제3_박스플롯.png', dpi=150, bbox_inches='tight')
plt.close()
# --------------------------------------------------------------------


# =============================================================================
# [과제 4] 팀 x 포지션 피벗 히트맵 또는 월별 추세선
# =============================================================================
# [비즈니스 문제 의도]
#   "팀-포지션 조합별로 평균 패스 성공률에 어떤 패턴이 있는가?"
#   또는
#   "시즌 진행에 따라(월별) 리그 전체 평균 득점 추세는 어떻게 변화하는가?"
#   둘 중 하나를 선택해 다차원/시계열 관점의 인사이트를 도출해보세요.
#
# [분석 포인트 힌트]
#   (A) 히트맵: pd.pivot_table(df, index='team', columns='position',
#                              values='pass_success_rate', aggfunc='mean')
#       -> sns.heatmap(pivot, annot=True, cmap='YlGnBu')
# ----------------------- TODO: 여기부터 작성 -----------------------
# (A) 히트맵 버전
#TODO: pivot_table 작성
pivot_table = pd.pivot_table(df, index='team', columns='position', values='pass_success_rate', aggfunc='mean')
plt.figure(figsize=(9, 6))
# TODO: sns.heatmap()
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu')
plt.title('팀-포지션 조합별 평균 패스')

plt.savefig('과제4_히트맵.png', dpi=150, bbox_inches='tight')
plt.close()
# --------------------------------------------------------------------