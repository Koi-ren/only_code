#구정은 강사님이 짜보는 코드

class Score:
    #def __init__(self):
    #    pass
    #다른 객체 지향 방법론을 지닌 유학학
    def __init__(self, num, sname, kor, math, eng):
        self.hnum = num
        self.sname = sname
        self.kor = kor
        self.math = math
        self.eng = eng
        self.total = self.kor + self.math + self.eng

    ##--getter/setter
    def getHnum(self): return self.hnum
    
    def setHnum(self, hn):
        if hn > 0: self.hnum = hn
    
    def getSname(self): return self.sname
    
    def setKor(self, kor): 
        if 0 <= kor <= 100: self.kor = kor

    def display(self):
        print(self.hnum, ",", end='')
        print(self.sname, ",", end='')

        print("")

s1 = Score(1, "홍길동", 56, 78,39)
s2 = Score(2, "김길동", 56, 92,85)

s1.display()