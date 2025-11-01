from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from .models import Post, Subject


@login_required
def my_page(request):
    return render(request, "my_page.html")


@permission_required("app_name.change_modelname")
def edit_page(request):
    return render(request, "edit_page.html")


def index(request):
    comwhal1 = Subject.objects.filter(category__name='컴퓨터활용능력1급')
    comwhal2 = Subject.objects.filter(category__name='컴퓨터활용능력2급')
    language = Subject.objects.filter(category__name='프로그래밍언어')
    return render(request, 'index.html', {
        'comwhal1': comwhal1,
        'comwhal2': comwhal2,
        'language': language,
    })


def video_detail(request, pk):
    video = get_object_or_404(Subject, pk=pk)
    return render(request, 'video_detail.html', {'video': video})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


@login_required(login_url='who:login')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def gallery(request):
    comwhal1 = Subject.objects.filter(category__name='comwhal1')
    comwhal2 = Subject.objects.filter(category__name='comwhal2')
    language = Subject.objects.filter(category__name='language')
    return render(request, 'gallery.html', {
        'comwhal1': comwhal1,
        'comwhal2': comwhal2,
        'language': language,
    })

