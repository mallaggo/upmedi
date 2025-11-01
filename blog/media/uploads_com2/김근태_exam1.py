import random

print("1부터 100사이의 숫자를 맞춰보세요!")
com=random.randint(1,100)
me=0
i=0
while True:
    i=i+1
    me=int(input("숫자를 입력하세요 : "))
    if me<com:
        print('더 큰 숫자입니다.')
    elif me>com:
        print('더 작은 숫자입니다.')
    else :
        print(f'정답입니다! {i}번 만에 맞췄어요')
        break
