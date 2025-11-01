class Student:
    def __init__(self,name,kor,eng,math):
        self.name=name
        self.kor=kor
        self.eng=eng
        self.math=math

    def calc_avg(self):
        self.avg=(self.kor+self.eng+self.math)/3

    def display_info(self):
        print(f"이름 :{self.name}")
        print(f"평균 :{self.avg}")

    def save_to_file(self):
        with open("score.txt","w",encoding="UTF-8") as f:
            f.write(f"{self.name},{self.avg}")

y_name = input("이름을 입력하세요 :")
y_kor = int(input("국어 점수를 입력하세요:"))
y_eng = int(input("영어 점수를 입력하세요 :"))
y_math = int(input("수학 점수를 입력하세요 :"))

S1=Student(y_name,y_kor,y_eng,y_math)
S1.calc_avg()
print("==학생 성적==")
S1.display_info()
S1.save_to_file()
