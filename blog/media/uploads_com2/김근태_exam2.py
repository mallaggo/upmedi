class Student:
    def __init__(self,name,kor,eng,math,avg):
        self.name=name
        self.kor=kor
        self.eng=eng
        self.math=math
        self.avg=avg
    def calc_avg(self):
        sum=kor+eng+math
        avg=sum/len(sum)
        
    def display(self):
        print(f"이름 : {self.name}, 평균 : {self.avg}")
        
    def save_to_file(self):
        openfile=open("student.txt","w")
        
    def 