class Student:
    def __init__(self,name,kor,eng,math):
        self.name=name
        self.kor=kor
        self.eng=eng
        self.math=math

    def calc_avg(self):
        self.avg=(self.kor+self.eng+self.math)/3

    def display_info(self):
        print(f"{self.name},{self.avg}")

    def save_to_file(self):
        with open("score.txt","w",encoding="UTF-8") as f:
            f.write(f"{self.name},{self.avg}")

y_name = input()
y_kor = int(input())
y_eng = int(input())
y_math = int(input())

S1=Student(y_name,y_kor,y_eng,y_math)
S1.calc_avg()
S1.display_info()
S1.save_to_file()
