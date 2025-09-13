from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.loader import render_to_string

from .forms import SignUpForm,LoginForm
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 인증 전까지 로그인 불가
            user.save()

            token = str(user.email_verification_token)
            verification_link = request.build_absolute_uri(f"/who/verify-email/{token}/")

            # HTML 이메일 내용 렌더링
            subject = "이메일 인증 안내"
            from_email = settings.EMAIL_HOST_USER
            to = [user.email]

            context = {"user": user, "verification_link": verification_link}
            text_content = render_to_string("registration/email_verification.txt", context)  # 텍스트 버전
            html_content = render_to_string("registration/email_verification.html", context)  # HTML 버전

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return render(request, "registration/email_verification_sent.html")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        user.email_verified = True
        user.is_active = True
        user.save()
        return render(request, "registration/email_verification_success.html")
    except CustomUser.DoesNotExist:
        return render(request, "registration/email_verification_fail.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password) # is_active=False인 유저는 인증에 성공하지 않음 (Django 기본 동작)
                                                                                #즉, 이메일 인증을 안 한 유저라면 authenticate 결과가 None이 됨
            if user is not None:
                login(request, user)  #이제부터 request.user 사용 가능
                return redirect("blog:index")  # 로그인 성공 시 이동할 페이지
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("who:login")  # 네임스페이스 필요 없으면 단순 "login"
