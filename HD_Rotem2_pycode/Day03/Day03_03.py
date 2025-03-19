class FourCal:
    def __init__(self):
        self.result = 3
    def add(self,num):
        self.result += num
        return self.result
    def sub(self, num):
        self.result -= num
        return self.result
    
a = FourCal()

k = a.add(3)
print(k)