#tt는 정답임으로 임의로 변경 가능
#각 시도 당 입력 숫자는 각각 00, 01, 10, 11로 제한함 -> 게임 적용시에는 이외의 값이 들어가지 않기 때문
#현재는 배터리와 연결되는 전선이 2개였기에 본 코드에서는 컴포넌트를 3개로 제한함.

tt = '000000'

z = False
y = []

def plubina(k1, k2, k3):
    xt = k1 + k2 + k3
    return xt

def try_to(st):
    global z, tt
    z1, z2, z3 = 0, 0, 0

    if st[0:2] != tt[0:2]:
        print("첫번째 시도는 잘못됐습니다")
        z1 += 1
        z = False
    if st[2:4] != tt[2:4]:
        print("두번째 시도는 잘못됐습니다")
        z2 += 1
        z = False

    if st[4:6] != tt[4:6]:
        print("세번째 시도는 잘못됐습니다")
        z3 += 1
        z = False

    if st == tt:
        print("연결이 올바릅니다.")
        z = True
    
    return z, z1, z2, z3

x1 = input("첫번째 수를 입력하시오: ")
x2 = input("두번쨰 수를 입력하시오: ")
x3 = input("세번째 수를 입력하시오: ")

xt = plubina(x1, x2, x3)
y = try_to(xt)

print(y[0], y[1], y[2], y[3])

while y[0] == False:
    if y[1] == 1:
        x1 = input("첫번째 수를 다시 입력하시오: ")
    if y[2] == 1:
        x2 = input("두번쨰 수를 다시 입력하시오: ")
    if y[3] == 1:
        x3 = input("세번째 수를 다시 입력하시오: ")
    xt = plubina(x1, x2, x3)
    y = try_to(xt)
    print(y[0], y[1], y[2], y[3])