import csv

class score_management:
    def __init__(self, st_num, name, score):
        self.num = st_num
        self.name = name
        self.score = score
    
    def input_value_reading(self):
        st_num = self.num
        name = self.name
        kor, math, eng = int(self.score[0]), int(self.score[1]), int(self.score[2])
        sum = kor + eng + math

        save_to_csv(score_save_path, st_num, name, kor, eng, math, sum) 

score_save_path = "c:/ws/HD_Rotem2_pycode/score_management.csv"
prev_st_num, score = 0, []

print("각 학생의 학번, 이름, 국영수 성적을 입력하시오")
print("더 입력할 학생이 없을 시, 학번에 c를 입력하시오")

with open(score_save_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["학번", "이름", "한국어", "영어", "수학", "총점"])

def save_to_csv(file_path, student_number, name, Korean, English, Math, Sum):
    """학번, 이름, 성적, 총점을 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_number, name, Korean, English, Math, Sum])

while (True):
    st_num = input("학번: ")
    
    if st_num == "c": break

    name = input("이름: ") 
    kor = input("국어 성적: ")
    eng = input("영어 성적: ")
    math = input("수학 성적: ")

    score = [kor, eng, math]

    if prev_st_num is not st_num:
        prev_st_num = st_num

        student = score_management(st_num, name, score)
        student.input_value_reading()