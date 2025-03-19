def main():
    print("1에서 100까지의 숫자를 입력하세요 (숫자는 역방향으로 입력할 수 없습니다):")
    numbers = []
    
    last_num = 0  # 이전 숫자를 저장할 변수
    
    while len(numbers) < 100:
        try:
            num = int(input(f"숫자 입력 ({len(numbers) + 1}/100): "))
            if num < 1 or num > 100:
                print("숫자는 1과 100 사이여야 합니다.")
            elif num in numbers:
                print("이미 입력된 숫자입니다.")
            elif num < last_num:  # 역방향으로 입력된 경우
                print("오류: 숫자가 역방향으로 입력되었습니다.")
            else:
                numbers.append(num)
                last_num = num  # 현재 숫자를 이전 숫자로 저장
        except ValueError:
            print("유효한 숫자를 입력하세요.")
    
    print("입력된 숫자는 올바르게 증가합니다.")
    
if __name__ == "__main__":
    main()
