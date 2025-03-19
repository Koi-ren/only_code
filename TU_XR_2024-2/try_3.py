#전선 번호 정답
#배터리 (+)극은 1, (-)극은 2
#브레이크 (+)극은 3, (-)극은 4, 신호선은 5

#규칙: 전선 번호 입력 시 두자리 이상 입력 금지 ex) 12, 20, 130, 안녕, 반가워

#위 같은 규칙이 있는 이유는 실제 게임에서는 버튼을 통해 신호가 가기에 정해진 값(1~5)이 입력되기에
#이에 따른 예외처리는 하지 않았기 때문

Battery_Ans = '11'
Break_Ans = '111'

z = False
x = False
Battery_reval = []
Break_reval = []

def Battery_Con(k1, k2):
    xt = k1 + k2
    return xt

def Break_Con(k1, k2, k3):
    xt = k1 + k2 + k3
    return xt

#배터리 결선 검사 함수
def Battery_test(st):
    global z, Battery_Ans
    z1, z2= 0, 0

    if st[0] != Battery_Ans[0]:
        print("배터리의 (+)극의 결선이 잘못됐습니다\n")
        #Battery_Ans[0] == 1
        if (st[0] == '2'):
            print('feedback_1\n')
        if (st[0] == '3'):
            print('feedback_2\n')
        if (st[0] == '4'):
            print('feedback_3\n')
        if (st[0] == '5'):
            print('feedback_4\n')
        z1 += 1
        z = False
    if st[1] != Battery_Ans[1]:
        print("배터리의 (-)극의 결선이 잘못됐습니다\n")
        #Battery_Ans[0] == 2
        if (st[1] == '0'):
            print('feedback_5\n')
        if (st[1] == '3'):
            print('feedback_6\n')
        if (st[1] == '4'):
            print('feedback_7\n')
        if (st[1] == '5'):
            print('feedback_8\n')
        z2 += 1
        z = False
    if st == Battery_Ans:
        print("배터리 결선 상태 양호합니다.\n")
        z = True
    
    return z, z1, z2

#브레이크 결선 검사 함수
def Break_test(st):
    global z, Break_Ans
    z1, z2, z3= 0, 0, 0

    if st[0] != Break_Ans[0]:
        print("브레이크의 (+)극의 결선이 잘못됐습니다\n")
        #Break_Ans[0] == 3
        if (st[0] == '0'):
            print('feedback_9\n')
        if (st[0] == '2'):
            print('feedback_10\n')
        if (st[0] == '4'):
            print('feedback_11\n')
        if (st[0] == '5'):
            print('feedback_12\n')
        z1 += 1
        z = False
    if st[1] != Break_Ans[1]:
        print("브레이크의 (-)극의 결선이 잘못됐습니다\n")
        #Break_Ans[0] == 4
        if (st[1] == '0'):
            print('feedback_13\n')
        if (st[1] == '2'):
            print('feedback_14\n')
        if (st[1] == '3'):
            print('feedback_15\n')
        if (st[1] == '5'):
            print('feedback_16\n')
        z2 += 1
        z = False
    if st[2] != Break_Ans[2]:
        print("브레이크 신호선의 결선이 잘못됐습니다\n")
        #Break_Ans[0] == 5
        if (st[2] == '0'):
            print('feedback_17\n')
        if (st[2] == '2'):
            print('feedback_18\n')
        if (st[2] == '3'):
            print('feedback_19\n')
        if (st[2] == '4'):
            print('feedback_20\n')        
        z3 += 1
        z = False
    if st == Break_Ans:
        print("브레이크 결선 상태 양호합니다.\n")
        z = True
    
    return z, z1, z2, z3

#배터리 연결부
print("\n배터리에 전선 연결을 시도합니다")
print("전선의 번호는 각각 1~5까지 존재합니다. 중복은 피해주세요\n")
Battery_1 = input("배터리의 (+)극에 연결할 전선의 번호를 입력하세요: ")
Battery_2 = input("배터리의 (-)극에 연결할 전선의 번호를 입력하세요: ")

#배터리 (+)극 연결 신호 처리
if (Battery_1 == '1'):
    Battery_1_1 = '1'
else:
    Battery_1_1 = Battery_1

#배터리 (-)극 연결 신호 처리
if (Battery_2 == '2'):
    Battery_2_1 = '1'
#입력 값에서 1을 0으로 치환 -> 예외처리
elif (Battery_2 == '1'):
    Battery_2_1 = '0'
else:
    Battery_2_1 = Battery_2
print('\n')

#브레이크 연결부
print("브레이크에 전선 연결을 시도합니다\n")
Break_1 = input("브레이크의 (+)극에 연결할 전선의 번호를 입력하세요: ")
Break_2 = input("브레이크의 (-)극에 연결할 전선의 번호를 입력하세요: ")
Break_3 = input("브레이크의 신호선에 연결할 전선의 번호를 입력하세요: ")

#브레이크 (+)극 연결 신호 처리
if (Break_1 == '3'):
    Break_1_1 = '1'
#입력 값에서 1을 0으로 치환 -> 예외처리
elif (Break_1 == '1'):
    Break_1_1 = '0'
else:
    Break_1_1 = Break_1

#브레이크 (-)극 연결 신호 처리
if (Break_2 == '4'):
    Break_2_1 = '1'
elif (Break_2 == '1'):
    Break_2_1 = '0'
else:
    Break_2_1 = Break_2

#브레이크 신호선 연결 신호 처리    
if (Break_3 == '5'):
    Break_3_1 = '1'
#입력 값에서 1을 0으로 치환 -> 예외처리
elif (Break_3 == '1'):
    Break_3_1 = '0'
else:
    Break_3_1 = Break_3
print('\n')

print('배터리의 결선 상태부터 검사 후 브레이크 결선 상태를 검사하겠습니다.')

#----------------------------------------------------------------------------------------------------
#-------------------------------------배터리 결선 검사부-----------------------------------------------
#----------------------------------------------------------------------------------------------------

print('배터리 결선 상태 검사 실시')
#배터리 연결 신호 문자열을 합해 Battery_t에 저장
Battery_t = Battery_Con(Battery_1_1, Battery_2_1)
print(Battery_t)
#배터리 결선 상태 결과값 Battery_reval에 저장
Battery_reval = Battery_test(Battery_t)

#배터리 연결 전선 번호가 맞을 때까지 반복
while Battery_reval[0] == False:
    #배터리 (+)극 재연결 시도
    if Battery_reval[1] == 1:
        Battery_1 = input("배터리의 (+)극에 연결할 전선의 번호를 다시 입력하세요: ")
        
        #배터리 (+)극 연결 신호 처리
        if (Battery_1 == '1'):
            Battery_1_1 = '1'
        else:
            Battery_1_1 = Battery_1
    #배터리 (-)극 재연결 시도        
    if Battery_reval[2] == 1:
        Battery_2 = input("배터리의 (-)극에 연결할 전선의 번호를 다시 입력하세요: ")
        
        #배터리 (-)극 연결 신호 처리
        if (Battery_2 == '2'):
            Battery_2_1 = '1'
        #입력 값에서 1을 0으로 치환 -> 예외처리
        elif (Battery_2 == '1'):
            Battery_2_1 = '0'
        else:
            Battery_2_1 = Battery_2
    #배터리 연결 신호 문자열을 합해 Battery_t에 저장
    Battery_t = Battery_Con(Battery_1_1, Battery_2_1)
    #배터리 결선 상태 결과값 Battery_reval에 저장
    Battery_reval = Battery_test(Battery_t)

print('배터리 결선 상태 검사 종료')
#배터리 결선 검사부 종료

#----------------------------------------------------------------------------------------------------
#-------------------------------------브레이크 결선 검사부---------------------------------------------
#----------------------------------------------------------------------------------------------------

print('브레이크 결선 상태 검사 실시')
#브레이크 연결 신호 문자열을 합해 Break_t에 저장
Break_t = Break_Con(Break_1_1, Break_2_1, Break_3_1)
#브레이크 결선 상태 결과값 Break_reval에 저장
Break_reval = Break_test(Break_t)

#브레이크 연결 전선 번호가 맞을 때까지 반복
while Break_reval[0] == False:
    #브레이크 (+)극 재연결 시도
    if Break_reval[1] == 1:
        Break_1 = input("브레이크의 (+)극에 연결할 전선의 번호를 다시 입력하세요: ")
        #브레이크 (+)극 연결 신호 처리
        if (Break_1 == '3'):
            Break_1_1 = '1'
        #입력 값에서 1을 0으로 치환 -> 예외처리
        elif (Break_1 == '1'):
            Break_1_1 = '0'
        else:
            Break_1_1 = Break_1
    #브레이크 (-)극 재연결 시도
    if Break_reval[2] == 1:
        Break_2 = input("브레이크의 (-)극에 연결할 전선의 번호를 다시 입력하세요: ")
        #브레이크 (-)극 연결 신호 처리
        if (Break_2 == '4'):
            Break_2_1 = '1'
        #입력 값에서 1을 0으로 치환 -> 예외처리
        elif (Break_2 == '1'):
            Break_2_1 = '0'
        else:
            Break_2_1 = Break_2
    #브레이크 신호선 재연결 시도
    if Break_reval[3] == 1:
        Break_3 = input("브레이크의 신호선에 연결할 전선의 번호를 다시 입력하세요: ")
        #브레이크 신호선 연결 신호 처리
        if (Break_3 == '5'):
            Break_3_1 = '1'
        #입력 값에서 1을 0으로 치환 -> 예외처리
        elif (Break_3 == '1'):
            Break_3_1 = '0'
        else:
            Break_3_1 = Break_3
    #브레이크 연결 신호 문자열을 합해 Break_t에 저장
    Break_t = Break_Con(Break_1_1, Break_2_1, Break_3_1)
    #브레이크 결선 상태 결과값 Break_reval에 저장
    Break_reval = Break_test(Break_t)

print('브레이크 결선 상태 검사 종료')
print('모든 결선 상태 양호')
#브레이크 결선 검사부 종료