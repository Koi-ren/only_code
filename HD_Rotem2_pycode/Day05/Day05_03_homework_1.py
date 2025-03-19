import random

class Duck:
    def __init__(self):
        self.x = random.randint(0,10)
        self.y = random.randint(0,10)
        self.work_count = 0
        self.bbik_count = 0

    def display(self, count): print(f"오리가 총 {count}마리 있습니다.", 
                                    f"오리들 평균 위치: ({self.x}, {self.y})")

    def work(self, count):
        self.work_count = count
        print(f"오리 {count}마리가 걸어갑니다.")

    def bbik_bbik(self, count):
        self.bbik_count = count
        print(f"오리가 {count}마리가 삑삑거립니다.")

    def move(self):
        dx = random.randint(1,10)
        dy = random.randint(1,10)
        right = self.x + dx
        left = self.y + dy
        print(f"오리들이 x축으로 {dx}만큼, y축으로 {dy}만큼 움직였습니다.", end =' ')
        print(f"현재 위치: ({right}, {left})")

    def bbik_bbik_stop(self): 
        print(f"시끄럽게 울던 오리 {self.bbik_count}마리가 삑삑거림을 멈춥니다.")

    def warning(self):
        print("오리의 마릿수가 잘못됐습니다.")

class Red(Duck):
    def color(self): print("빨간",end = "")

class Green(Duck):
    def color(self): print("초록",end = "")

red_warning = False
green_warning = False

red_duck_count = int(input("빨간오리의 수를 입력하세요: "))
working_red_duck_count = int(input("걸어다니는 빨간오리의 수를 입력하세요: "))
bbik_red_duck_count = int(input("삑삑거리는 빨간오리의 수를 입력하세요: "))
'''
if red_duck_count != working_red_duck_count + bbik_red_duck_count:
    red_warning = True
    print("빨간오리 숫자가 뭔가 잘못됐습니다.")
'''
    
green_duck_count = int(input("초록오리의 수를 입력하세요: "))
working_green_duck_count = int(input("걸어다니는 초록오리의 수를 입력하세요: "))
bbik_green_duck_count = int(input("삑삑거리는 초록오리의 수를 입력하세요: "))
'''
if green_duck_count != working_green_duck_count + bbik_green_duck_count:
    green_warning = True
    print("초록오리 숫자가 뭔가 잘못됐습니다.")
'''
    
red_duck = Red()
green_duck = Green()

print('='*10,"빨간오리",'='*10)
red_duck.color()
red_duck.display(red_duck_count)

red_duck.color()
red_duck.work(working_red_duck_count)

red_duck.color()
red_duck.bbik_bbik(bbik_red_duck_count)
'''
if red_warning: 
    red_duck.color()
    red_duck.warning()
'''
print('='*10,"초록오리",'='*10)
green_duck.color()
green_duck.display(green_duck_count)

green_duck.color()
green_duck.work(working_green_duck_count)

green_duck.color()
green_duck.bbik_bbik(bbik_green_duck_count)
'''
if green_warning: 
    green_duck.color()
    green_duck.warning()
'''
print('='*10,"빨간오리 행동",'='*10)
red_duck.color()
red_duck.move()

print('='*10,"초록오리 행동",'='*10)
green_duck.color()
green_duck.bbik_bbik_stop()