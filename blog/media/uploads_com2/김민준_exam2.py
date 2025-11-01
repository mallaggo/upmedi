class Student:
    def __int__(self,name,kor,eng,math):
        self.name=name
        self.kor=kor
        self.eng=eng
        self.math=math
        self.avg=0

    def calc_avg(self):
        self.avg= (self.kor+self.eng+self.math)/3
        return self.avg


    def display_info(self):
        print("\n== 학생성적 ===")
        print(f"이름: {self.name}")

    def save_to_file(self):
        with open("score,txt","w",encoding="utf-8") as f:
            f.write(f"{self.name},{self.avg}")

tname=input("이름 : ")
tkor=int(input("국어점수 : "))
teng=int(input("영어점수 : "))
tmath=int(input("수학점수 : "))

s1=Student(tname,tkor,teng,tmath)
s1.calc_avg()
s1.display_info()
s1.save_to_file()
