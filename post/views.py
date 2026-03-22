from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def post_list(request):
    search = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-id')

    if search:
        posts = posts.filter(title__icontains=search)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'board/list.html', {
        'posts': posts,
        'search': search
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    return render(request, 'board/detail.html', {
        'post': post,
        'comments': comments,
        'form': CommentForm()
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   # 핵심
            post.save()
            return redirect('post:post_list')
    else:
        form = PostForm()

    return render(request, 'board/create.html', {'form': form})


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user   # 핵심
            comment.save()

    return redirect('post:post_detail', pk=pk)

