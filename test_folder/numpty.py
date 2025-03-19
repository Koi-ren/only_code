#stop
a = [1,2,3,4,5,6,3,2,2,3,3,2,1,3]
#tr
b = [2,3,4,2,1,4,4]
#tl
c = [2,5,7,9,0,7,5,3,2]

al = len(a)
bl = len(b)
cl = len(c)

if((al>bl) and (al>cl)):
  print('stop')
elif((bl>al) and (bl>cl)):
  print('tr')
elif((cl>al) and (cl>bl)):
  print('tl')

k = 0
def vartest():
    global k
    num_list = list(range(1, 11))
    for num in num_list:
        k += num
 
vartest()
print("new k = ", k)

t = 0
def vartest(value):
    num_list = list(range(1, 11))
    for num in num_list:
        value += num   
    return num
 
t = vartest(t)
print("new t = ", t)

# 세 개의 배열을 초기화합니다.
a = []
b = []
c = []

# 사용자로부터 a 배열에 저장할 정수를 입력받습니다.
print("a 배열에 저장할 정수를 입력하세요 (완료되면 '끝'을 입력):")
while True:
    input_str = input()
    if input_str == '끝':
        break
    a.append(int(input_str))

# 사용자로부터 b 배열에 저장할 정수를 입력받습니다.
print("b 배열에 저장할 정수를 입력하세요 (완료되면 '끝'을 입력):")
while True:
    input_str = input()
    if input_str == '끝':
        break
    b.append(int(input_str))

# 사용자로부터 c 배열에 저장할 정수를 입력받습니다.
print("c 배열에 저장할 정수를 입력하세요 (완료되면 '끝'을 입력):")
while True:
    input_str = input()
    if input_str == '끝':
        break
    c.append(int(input_str))

# 가장 많은 원소를 가진 배열을 찾습니다.
max_length = max(len(a), len(b), len(c))

# 결과를 출력합니다.
if max_length == len(a):
    print("**a 배열이 가장 많은 원소를 가지고 있습니다:**", a)
elif max_length == len(b):
    print("**b 배열이 가장 많은 원소를 가지고 있습니다:**", b)
else:
    print("**c 배열이 가장 많은 원소를 가지고 있습니다:**", c)

