"""
    reshape(shape) : 배열을 재구성

    * 배열 요소의 총 개수는 유지되어야 함
    (12,) --> (1, 12) / (12, 1) / (3, 4) / ...
    * 한 축을 자동으로 계산하고자 할 경우 -1 지정
    (단, 한번만 사용 가능)
"""
import numpy as np
# TODO: 0~11 까지 데이터를 포함하는 1차원 배열 생성

arr = np.arange(12)
print(np.arange(12))

# 1차원 배열(12, )을 2차원 배열로 재구성
arr_2d = arr.reshape(3, 4)
print(arr.reshape(3, 4))

arr_2d = arr.reshape(2, 6)
print(arr.reshape(2, 6))

# -1 지정: 자동계산
arr_2d_3 = arr.reshape(4, -1)
print(arr.reshape(4, -1))

arr_2d_4 = arr.reshape(-1, 6)
print(arr.reshape(-1, 6))

print('-'*60)

# 1차원 배열 -> 3차원 배열
#(12, ) -> (2,2,3)
arr_3d = arr.reshape(2,2,3)
print(arr.reshape(2,2,3))
print(arr_3d.shape)

# (12, ) -> (3,2,-1)
arr_3d_1 = arr.reshape(3,2,-1)
print(arr.reshape(3,2,-1))

print('-'*60)

#다차원 -> 1차원
arr_1d = arr_3d.flatten()
print(f"flatten : {arr_1d}")

arr_1d_2 = arr_3d.ravel()
print(f"ravel : {arr_1d_2}")
# ravel 이 복사본을 반환하는 경우
# 메모리가 연속적으로 배치된 경우에만 뷰를 반환
# 메모리가 불연속적인 경우 (ex. 전치행렬, .T 등) 복사본을 반환
# .base 속성으로 뷰인지 복사본인지 확인 가능
# ex) arr_1d_2.base is arr_3d => 결과가 True = 뷰 / False = 복사본

arr_1d_3 = arr_3d.reshape(-1)
print(f"reshape(-1) : {arr_1d_3}")  # 뷰

arr_1d_4 = arr_2d.reshape(-1)
print(f"reshape(-1) : {arr_1d_4}")
