#미완

Battery_Ans = '12'
Break_Ans = '345'

def get_input(prompt, valid_choices):
    while True:
        value = input(prompt)
        if value in valid_choices:
            return value
        print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")

def Battery_Con(k1, k2):
    return k1 + k2

def Break_Con(k1, k2, k3):
    return k1 + k2 + k3

def Battery_test(st, Battery_Ans):
    feedbacks = {
        '1': ["", 'feedback_1', 'feedback_2', 'feedback_3', 'feedback_4'],
        '2': ['feedback_5', '', 'feedback_6', 'feedback_7', 'feedback_8']
    }

    errors = [i for i in range(2) if st[i] != Battery_Ans[i]]

    if errors:
        for i in errors:
            print(f"배터리의 {'(+)극' if i == 0 else '(-)극'}의 결선이 잘못됐습니다")
            print(feedbacks[Battery_Ans[i]][int(st[i])] + '\n')
        return False
    else:
        print("배터리 결선 상태 양호합니다.\n")
        return True

def Break_test(st, Break_Ans):
    feedbacks = {
        '3': ['feedback_9', '', 'feedback_10', '', 'feedback_11', 'feedback_12'],
        '4': ['feedback_13', '', 'feedback_14', 'feedback_15', '', 'feedback_16'],
        '5': ['feedback_17', '', 'feedback_18', 'feedback_19', 'feedback_20', '']
    }

    errors = [i for i in range(3) if st[i] != Break_Ans[i]]

    if errors:
        for i in errors:
            print(f"브레이크의 {['(+)극', '(-)극', '신호선'][i]}의 결선이 잘못됐습니다")
            print(feedbacks[Break_Ans[i]][int(st[i])] + '\n')
        return False
    else:
        print("브레이크 결선 상태 양호합니다.\n")
        return True

def main():
    valid_choices = ['1', '2', '3', '4', '5']

    print("\n전선의 번호는 각각 1~5까지 존재합니다. 중복은 피해주세요")
    print("\n배터리에 전선 연결을 시도합니다")
    Battery_1 = get_input("배터리의 (+)극에 연결할 전선의 번호를 입력하세요: ", valid_choices)
    Battery_2 = get_input("배터리의 (-)극에 연결할 전선의 번호를 입력하세요: ", valid_choices)
    
    Battery_t = Battery_Con(Battery_1, Battery_2)
    while not Battery_test(Battery_t, Battery_Ans):
        Battery_1 = get_input("배터리의 (+)극에 연결할 전선의 번호를 다시 입력하세요: ", valid_choices)
        Battery_2 = get_input("배터리의 (-)극에 연결할 전선의 번호를 다시 입력하세요: ", valid_choices)
        Battery_t = Battery_Con(Battery_1, Battery_2)

    print("브레이크에 전선 연결을 시도합니다")
    Break_1 = get_input("브레이크의 (+)극에 연결할 전선의 번호를 입력하세요: ", valid_choices)
    Break_2 = get_input("브레이크의 (-)극에 연결할 전선의 번호를 입력하세요: ", valid_choices)
    Break_3 = get_input("브레이크의 신호선에 연결할 전선의 번호를 입력하세요: ", valid_choices)
    
    Break_t = Break_Con(Break_1, Break_2, Break_3)
    while not Break_test(Break_t, Break_Ans):
        Break_1 = get_input("브레이크의 (+)극에 연결할 전선의 번호를 다시 입력하세요: ", valid_choices)
        Break_2 = get_input("브레이크의 (-)극에 연결할 전선의 번호를 다시 입력하세요: ", valid_choices)
        Break_3 = get_input("브레이크의 신호선에 연결할 전선의 번호를 다시 입력하세요: ", valid_choices)
        Break_t = Break_Con(Break_1, Break_2, Break_3)

    print("모든 결선 상태 양호")

if __name__ == "__main__":
    main()
