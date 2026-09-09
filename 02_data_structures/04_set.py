"""
    집합 set
"""

# 중복 불가, 순서X , 수정 O

nums = {1, 2, 3, 3, 3, 4, 2 }
print(f"nums : {nums}")

# 비어 있는 상태 표현 -> set()
empty1 = {}     # type이 딕셔너리
empty2 = set()

print(f"empty1 : {type(empty1)}")
print(f"empty2 : {type(empty2)}")

nums = [1, 2, 3, 3, 3, 4, 2]
print(f"원본 데이터 : {nums}")
print(f"중복 제거 : {set(nums)}")
print(f"중복 제거 : {list(set(nums))}")
print()

# 집합 연산
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"합집합 | : {a | b}")    #합집합
print(f"교집합 & : {a & b}")    #교집합
print(f"차집합 - : {a - b}")

data = {1, 2}
print(f"data : {data}")

data.add(3)
print(f"data : {data}")

data.update([4,5])
print(f"data : {data}")

data.update([4,5,6,7])
print(f"data : {data}")

#삭제 discard
data.discard(1)
print(f"data : {data}")

#없는 숫자 적으면
data.discard(1)
print(f"data : {data}")
#오류도 없고 변화도 없음