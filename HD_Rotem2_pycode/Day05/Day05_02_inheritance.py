class Character:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.myShape = "character"

    def  display(self):
        print(self.x, ",", end="")
        print(self.y, ",", end="")
        print(self.myShape)
    
    def moveLeft(self):
        self.x -= 2 # self.x = self.x -2
        self.display()

    def moveRight(self):
        self.x += 2
        self.display()

    
class Player(Character):
    def display(self):
        print("Player....display()....")

class Enemy(Character):
    def moveUp(self):
        self.y -= 2
        self.display()

    def moveDown(self):
        self.y += 2
        self.display()

'''
#version_1

pobj = Player()
pobj.display()
pobj.moveRight()

eobj = Enemy()
eobj.display()
eobj.moveUp()
'''

'''
#version_2

pobj = Player()
pobj.display() #super class 상속한 메소드가 호출
pobj.show() #sub class 에서 확장한 메소드가 호출 ==> display()와 show()는 거의같은 기능을 수행하지만 다르다.
print("-"*50)


eobj = Enemy()
eobj.display()
'''


#version_3
pobj = Player()
pobj.display() #over writting 된 것 ==> 상속에 덮어쓰기

print("-"*50)

eobj = Enemy()
eobj.display()
