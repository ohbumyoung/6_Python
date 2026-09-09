"""
    딕셔너리 (dict)
"""

# key-value 형태로 데이터를 관리

user = {
    "name" : "오범영",
    "age" : 29,
    "skills" : ["Java", "SQL", "Html / Css", "Js", "Python"] 
}

print(f"user : {user}")

# 딕셔너리 내의 데이터 접근 -> 키값 사용
print(f"이름 : {user['name']}")
print(f"스킬 : {user['skills']}")

# 직접 접근 시 존재하지 않는 키값은 오류 발생
print()
# get() 사용하여 접근
print(f"이름 : {user.get('name')}")
print(f"스킬 : {user.get('skills')}")

# 존재하지 않는 키값인 경우 None 반환
print(f"연락처 : {user.get('phone')}")
print(f"연락처 : {user.get('phone', '없음')}") # 기본값 지정 가능

# 변경 (추가 / 수정 / 삭제)
user['email'] = 'dhqjadud3@naver.com'
print(f"user - {user}")

user['age'] = 40    # 기존의 키값을 지정하면 변경
print(f"user - {user}")

del user['age']
print(f"user - {user}")

"""     # 오류 발생
del user['phone']
print(f"user - {user}")
"""
print()

# 탐색
for key in user:
    print(f"{key} / value:{user[key]}")

for k, v in user.items():
    print(f"key: {k} / value: {v}")
print()

print(f"키 목록: {list(user.keys())}")
print(f"밸류 목록 :{list(user.values())}")
print(f"items() : {list(user.items())}")