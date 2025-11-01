import random

print("===숫자 맞추기 게임 ===")
print("1부터 100사이의 숫자를 맞춰보세요!")

#
answer = random.randint(1,100)
count = 0 

while True:
    guess = int(input("숫자를 입력하세요: "))
    count +=1

    if guess < answer:
        print("더 큰 숫자입니다.")
    elif guess > answer:
        print("더 작은 숫자입니다.")
    else:
        print(f"정답입니다! {count}번 만에 맞췄어요")
        break