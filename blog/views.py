from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from .models import Video,Post


def index(request):
    videos = Video.objects.all().order_by("-created_at")  # 최신순
    return render(request, "index.html", {"videos": videos})

@login_required
def my_page(request):
    return render(request, "my_page.html")

@permission_required("app_name.change_modelname")
def edit_page(request):
    return render(request, "edit_page.html")

@login_required(login_url='who:login')
def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, "video_detail.html", {"video": video})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

@login_required(login_url='who:login')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})