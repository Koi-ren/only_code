#선언문
def get_max(a, b):
    result = a
    if result < b:
        result = b
    #print(result)
    return result

#main코드

x = 10
y = 20

t1 = get_max(x,y)

x = 100
y = 200

t2 = get_max(x,y)

print(t1, t2)