def plubina(k1, k2, k3):
    return k1 + k2 + k3

def try_to(st, tt):
    # 각 부분의 비교 결과를 리스트로 저장
    segments_correct = [st[i:i+2] == tt[i:i+2] for i in range(0, 6, 2)]
    # 각 부분의 오류 여부를 저장
    errors = [not correct for correct in segments_correct]

    # 각 부분에 대한 피드백
    if not segments_correct[0]:
        print("첫번째 시도는 잘못됐습니다.")
    if not segments_correct[1]:
        print("두번째 시도는 잘못됐습니다.")
    if not segments_correct[2]:
        print("세번째 시도는 잘못됐습니다.")
    
    if all(segments_correct):
        print("연결이 올바릅니다.")

    return all(segments_correct), errors

# 초기화
tt = '001000'
x1, x2, x3 = '', '', ''

# 메인 루프
while True:
    if not x1:  # 잘못 입력된 경우에만 다시 묻기
        x1 = input("첫번째 수를 입력하시오: ")
    if not x2:
        x2 = input("두번째 수를 입력하시오: ")
    if not x3:
        x3 = input("세번째 수를 입력하시오: ")

    xt = plubina(x1, x2, x3)
    is_correct, errors = try_to(xt, tt)

    if is_correct:
        break

    # 잘못된 입력을 초기화
    x1, x2, x3 = [x if not error else '' for x, error in zip([x1, x2, x3], errors)]