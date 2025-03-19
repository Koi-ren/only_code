import random

class enemy:
    def __init__(self, enemy_name):
        self.x = random.randint(0,540)
        self.y = random.randint(0,480)
        self.name = enemy_name

    def display(self):
        print(self.x, ",",self.y,",","===>", self.name)

    def move_left(self):
        distance = 2
        self.x -= distance
        print(f"{self.name} move left!",end=' ')
        self.display()

    def move_right(self):
        distance = 2
        self.x += distance
        print(f"{self.name} move right!",end=' ')
        self.display()

    def move_up(self):
        distance = 2
        self.y -= distance
        print(f"{self.name} move up!", end=' ')
        self.display()

    def move_down(self):
        distance = 2
        self.y += distance
        print(f"{self.name} move down!", end=' ')
        self.display()

enemy1, enemy2 = enemy("enemy1"), enemy("enemy2")

enemy1.display()
enemy2.display()

enemy1.move_left()
enemy1.move_down()
enemy2.move_right()
enemy2.move_up()

'''
while(True):
    
    enemy1.move_left()
    enemy2.move_right()
    enemy1.move_down()
    enemy2.move_up()
'''