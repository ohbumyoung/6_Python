"""
    조건문
"""
# 블록은 들여쓰기로 구분, 조건식 옆에는 클론(:) 지정
# else는 elif로 사용
print("=" * 60)
print("if /elif / else")
print("=" * 60)

# value = 3 -> 조건문 내부 2줄 실행되지 않음
value = 10

if value > 5:
    print("조건문 내부입니다.")
    print("조건문 내에서 실행하고자 한다면 들여쓰기 필수!!")

print("조건문 외부입니다.")

score = 90 # int(input("점수 입력 : "))

if score >= 90:
    grade = "A"
elif score >= 80: 
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F" 

print(f"{score}점 => {grade}")

print()

print("=" * 60)
print("삼항 연산")
print("=" * 60)

# 참일때 결과값 if 조건식 else 거짓일때 결과값
age = 29 # int(input("나이 입력: "))
"""
if 문 사용 할때
if age >= 20:
    result = "성인"
else:
    result = "미성년자"

print(f"{age}세 -> {result}")
"""

result = "성인" if age >= 20 else "미성년자"
print(f"{age}세 -> {result}")

print("=" * 60)
print("match-case (Jave의 Switch)")
print("=" * 60)

status = int(input("상태 코드 입력: "))
match status:
    case 200:
        result = "정상"
    case 404:
        result = "페이지를 찾을 수 없음"
    case 500:
        result = "서버 오류"
    case _:
        result = "알수 없음"

print(f"{status} -> {result}")

print("=" * 60)
print(" pass ")
print("=" * 60)

# 빈 블록을 작성하고 할 때 사용 (오류 방지)
score = 90

if score > 90:
    pass        # 미구현 부분을 임시로 처리
else:
    print("---- else 영역----")