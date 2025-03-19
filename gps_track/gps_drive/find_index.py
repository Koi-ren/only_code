import numpy as np

# 2D 배열 생성 (예시 데이터)
array = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# 찾고자 하는 값
target_value = 5

# 배열에서 값을 찾아서 그 값의 열을 반환하는 함수
def find_column(array, target_value):
    # 배열에서 target_value의 위치를 찾음
    result = np.where(array == target_value)
    
    # result는 (row_indices, col_indices) 형태로 반환됨
    if result[0].size > 0:  # 값이 존재하는 경우
        col_index = result[1][0]  # 열 인덱스 가져오기
        return col_index
    else:
        return None  # 값이 없을 경우 None 반환

# 값이 있는 열 찾기
column_index = find_column(array, target_value)

if column_index is not None:
    print(f"Value {target_value} is in column {column_index}")
else:
    print(f"Value {target_value} not found in the array")
