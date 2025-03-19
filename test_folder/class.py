class FourCal:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        
    def setdata(self, first, second):
        self.first = first
        self.second = second

    def add(self):
        result = self.first + self.second
        
        return result
    def sub(self):
        result = self.first - self.second
        return result
    def div(self):
        result = self.first / self.second
        return result
    def mul(self):
        result = self.first * self.second
        return result
    
class MoreFourCal(FourCal):
    def pow(self):
        result = self.first ** self.second
        return result
    
class SafeFourCal(FourCal):
    def div(self):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second
        
class Family:
    lastname = "김"

a = MoreFourCal(4,0)
b = SafeFourCal(4,0)
c = Family
#특정 클래스에 괄호()를 안붙히고 해당 객체 변수를 바꾸면 전체 클래스 변수가 변한다
#d = Family 
d = Family()
d.lastname = "최"

print(a.first, a.second)
print(f"a, add: {a.add()}")
print(f"a, mul: {a.mul()}")
print(f"a, pow: {a.pow()}")
print(f"b, div: {b.div()}")
print(Family.lastname)
print(c.lastname)
print(d.lastname)