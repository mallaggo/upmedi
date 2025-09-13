from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "아이디",  #labels 안해주면 기본이 username의 레이블명이 이름으로 나옴
            "email": "이메일",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
        }



class LoginForm(forms.Form): #UserCreationForm 상속 받는 것보다 커스터 마이징은 유리, 대신 검사등의 해결은 손수 해야함
    username = forms.CharField(    #  대신 패스워드1 패스워드2 일치등의 검사 해결은 손수 해야함
        label="아이디",
        widget=forms.TextInput(attrs={"placeholder": "아이디 입력"})
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 입력"})
    )
