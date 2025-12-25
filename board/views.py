from django.shortcuts import render,get_object_or_404, redirect
from .models import Com2,Com2_movie,Com1_movie,Com1_board
from .forms import Com2Form,Com1Form
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='who:login')
def com2_list(request):

    com2_movie_list = Com2_movie.objects.all().order_by('-created_at')
    document_list = Com2.objects.all().order_by('-created_at')

    # 페이지네이터: 한 페이지에 10개씩
    paginator = Paginator(document_list, 10)

    # 현재 페이지 번호 가져오기 (?page=2 이런 식으로 들어옴)
    page_number = request.GET.get('page')

    # 해당 페이지의 객체들
    page_obj = paginator.get_page(page_number)

    # 템플릿으로 전달
    return render(request, 'community2/com2_list.html', {'com2_movie_list': com2_movie_list,'page_obj': page_obj})



def com2_detail(request, pk):
    doc = get_object_or_404(Com2, pk=pk)
    return render(request, 'community2/com2_detail.html', {'doc': doc})

# def validate_file_size(value):
#     max_size = 5 * 1024 * 1024  # 5MB
#     if value.size > max_size:
#         raise ValidationError(f'파일 크기는 최대 {max_size / (1024*1024)}MB까지 허용됩니다.')

def com2_upload(request):
    if request.method == 'POST':
        form = Com2Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('board:com2_list')
    else:
        form = Com2Form()
    return render(request, 'community2/com2_upload.html', {'form': form})


@login_required(login_url='who:login')
def com1_list(request):

    com1_movie_list = Com1_movie.objects.all().order_by('-created_at')
    com1_board_list = Com1_board.objects.all().order_by('-created_at')

    # 페이지네이터: 한 페이지에 10개씩
    paginator = Paginator(com1_board_list, 10)

    # 현재 페이지 번호 가져오기 (?page=2 이런 식으로 들어옴)
    page_number = request.GET.get('page')

    # 해당 페이지의 객체들
    page_obj = paginator.get_page(page_number)

    # 템플릿으로 전달
    return render(request, 'comwhal1/com1_list.html', {'com1_movie_list': com1_movie_list,'page_obj': page_obj})

def com1_detail(request, pk):
    doc = get_object_or_404(Com1_board, pk=pk)
    return render(request, 'comwhal1/com1_detail.html', {'doc': doc})


def com1_upload(request):
    if request.method == 'POST':
        form = Com1Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('board:com1_list')
    else:
        form = Com1Form()
    return render(request, 'comwhal1/com1_upload.html', {'form': form})


def py_list(request):

    # document_list = Com2.objects.all().order_by('-created_at')
    #
    # paginator = Paginator(document_list, 10)
    #
    # page_number = request.GET.get('page')
    #
    # page_obj = paginator.get_page(page_number)

    # 템플릿으로 전달
    return render(request, 'pystudy/pytable.html', )