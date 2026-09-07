"""
    변수와 자료형
"""

# 동적 타입 => 타입 선언 생략
name = "오범영"
age = 20
height = 183.2
is_tired = False  #True
temp = None

print(name, age, height, is_tired, temp)

print("=" * 60)
print("기본 자료형 5가지")
print("=" * 60)

# 변수에 저장된 데이터 타입 확인 => type(변수)
print(f"{name} : {type(name)}")
print(f"{age} : {type(age)}")
print(f"{height} : {type(height)}")
print(f"{is_tired} : {type(is_tired)}")
print(f"{temp} : {type(temp)}")

print("=" * 60)

# 이전에 저장한 타입과 이후에 저장한 타입이 달라도 저장 가능
# --> 홀란을 방지하기 위해 하나의 변수에는 하나의 타입만 사용(권장)
value = 27
print(f"{value} : {type(value)}")
value = "스물일곱"
print(f"{value} : {type(value)}")

print("=" * 60)

# 다중 할당
x, y, z = 10, 20, 30
print(f"x, y, z -> {x}, {y}, {z}")

a = b = c = 0
print(f"a = b = c -> {a}, {b}, {c}")

# 값 교환
x, y = y, x
print(f"x, y -> {x}, {y}")

# 타입 힌트
# : 강제없이 없으며, 에러도 발생되지 않는다.
menu: str = "보섭살"
print(f"menu : {menu} ({type(menu)})")

price: int = "39000원"
print(f"price : {price} ({type(price)})")

print("=" * 60)

# 상수 -> 대문자로 변수를 작성하는 것을 약속관례
# 자바와 같이 .final 키워드는 없다.

# 최대 인원: 60 이라는 값을 저장

MAX_PERSON = 60
print(f"최대인원: {MAX_PERSON}")
