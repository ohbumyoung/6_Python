"""
    연산자
"""

print("=" * 60)
print("산술 연산자")
print("=" * 60)

print(f"7 + 3 = {7 + 3}")
print(f"7 - 3 = {7 - 3}")
print(f"7 * 3 = {7 * 3}")
print(f"7 ** 3 = {7 ** 3}") # 거듭제곱 연산 = 7을 3번 곱함
print(f"7 / 3 = {7 / 3}")   # 실수 나눗셈
print(f"7 / 3 = {7 // 3}")  # 정수 나눗셈
print(f"7 % 3 = {7 % 3}")   # 나머지 연산

print(f"실수 나눗셈 타입(7 / 3) : {type(7 / 3)}")
# 타입은 항상 floot
print(f"실수 나눗셈 타입(6 / 3) : {6 / 3} {type(6 / 3)}")

print(f"-7 / 3 = {-7 / 3}")
# 자바에서는 버림처리, 파이썬에서는 내림처리
print(f"-7 // 3 = {-7 // 3}") 

print("=" * 60)
print("비교, 논리 연산자")
print("=" * 60)

a, b = 2, 5
print(f"a, b --> {a}, {b}")
print(f"a == b --> {a == b}")   # 같은지
print(f"a != b --> {a != b}")   # 다른지 
print(f"a < b --> {a < b}")  
print(f"a > b --> {a > b}")   
print()    

# 논리 연산자 : Java에서 &&, ||, ! 연산자가 아닌 피아썬에서는
#             and, or, not을 사용

print(f"and --> {True and True}")
print(f"or --> {True or Fales}")
print(f"not --> {not False}")

# a 값이 -5 ~ 5 사이의 값인가?
print(f"결과: {-5 <= a and a <= 5}")
print(f"{-5 <= a <= 5}")    #연쇄 비교 가능!