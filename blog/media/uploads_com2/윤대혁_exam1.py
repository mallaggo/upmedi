import random
com= random.randint(1,100)

X=1
print("1qnxj 100사이의 숫자를 맞춰보세요!")
while True:
    you = int(input("숫자를 입력하세요: "))
    if com > you:
        print("더 큰 숫자입니다")
        X += 1
    elif com < you:
        print("더 작은 숫자입니다")
        X += 1
    else:
        print(f"정답입니다! {X}번 만에 맞췄어요")
        break