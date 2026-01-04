from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject,MyProduct, MyCategory
from django.contrib import messages
# app/views.py


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



def product_list(request, category_id=None):
    # 카테고리 목록(좌측/상단 필터용)
    categories = MyCategory.objects.all().order_by("name")

    # 기본 쿼리셋
    qs = MyProduct.objects.select_related("category")

    # 카테고리 필터
    active_category = None
    if category_id is not None:
        active_category = get_object_or_404(MyCategory, id=category_id)
        qs = qs.filter(category=active_category)

    # 정렬 옵션(쿼리스트링 ?sort=)
    sort = request.GET.get("sort", "new")
    sort_map = {
        "new": "-id",
        "price_asc": "price",
        "price_desc": "-price",
        "name": "name",
    }
    qs = qs.order_by(sort_map.get(sort, "-id"))

    context = {
        "products": qs,
        "categories": categories,
        "active_category": active_category,
        "sort": sort,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, p_id):
    product = get_object_or_404(MyProduct, id=p_id)

    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)



def cart_add(request, p_id):
    # POST만 허용 (GET으로 들어오면 상세로 돌려보냄)
    if request.method != "POST":
        return redirect("blog:product_detail", p_id=p_id)

    product = get_object_or_404(MyProduct, id=p_id)

    # qty 받기 (없으면 1)
    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    # 최소 1개
    if qty < 1:
        qty = 1

    # 재고 체크
    if product.stock <= 0:
        messages.error(request, "품절 상품입니다.")
        return redirect("blog:product_detail", p_id=p_id)

    # 요청 수량이 재고보다 크면 재고로 제한
    if qty > product.stock:
        qty = product.stock
        messages.info(request, f"재고가 부족하여 수량을 {product.stock}개로 조정했어요.")

    # 세션 장바구니 가져오기
    cart = request.session.get("cart", {})  # { "3": {"qty":2, "price":15000, "name":"..."}, ... }
    pid = str(product.id)

    # 이미 담긴 상품이면 수량 누적, 아니면 새로 추가
    current_qty = cart.get(pid, {}).get("qty", 0)
    new_qty = current_qty + qty

    # 누적 수량도 재고를 넘지 않게 제한
    if new_qty > product.stock:
        new_qty = product.stock
        messages.info(request, f"재고 한도 내에서 {product.stock}개까지만 담을 수 있어요.")

    cart[pid] = {
        "qty": new_qty,
        "price": int(product.price),  # 가격 스냅샷(원 단위 정수)
        "name": product.name,         # 장바구니 화면에서 편하게 쓰려고(선택)
    }

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"장바구니에 담겼어요: {product.name} x {new_qty}")

    # 담은 뒤 어디로 보낼지: 상세로 돌아가거나 장바구니로 이동 (지금은 상세로)
    return redirect("blog:cart_list")


def cart_list(request):
    cart = request.session.get("cart", {})  # {"3": {"qty":2, "price":15000, "name":"..."}, ...}

    # cart가 비어있으면 바로 템플릿으로
    if not cart:
        return render(request, "cart/cart_list.html", {"items": [], "total": 0})

    product_ids = [int(pid) for pid in cart.keys()]
    products = MyProduct.objects.filter(id__in=product_ids)
    products_map = {p.id: p for p in products}

    items = []
    total = 0

    # 세션에 있는 순서대로 보여주고 싶으면 cart.keys() 순회
    for pid_str, data in cart.items():
        pid = int(pid_str)
        product = products_map.get(pid)
        if not product:
            # DB에서 삭제된 상품이면 세션에서 제거
            cart.pop(pid_str, None)
            request.session["cart"] = cart
            request.session.modified = True
            continue

        qty = int(data.get("qty", 1))
        price = int(data.get("price", product.price))  # 스냅샷 가격 우선, 없으면 DB 가격
        subtotal = price * qty
        total += subtotal

        items.append({
            "product": product,
            "pid": pid,
            "name": data.get("name", product.name),
            "price": price,
            "qty": qty,
            "subtotal": subtotal,
            "max_qty": product.stock if product.stock and product.stock > 0 else 1,
        })

    return render(request, "cart/cart_list.html", {"items": items, "total": total})


def cart_update(request, p_id):
    if request.method != "POST":
        return redirect("blog:cart_list")

    cart = request.session.get("cart", {})
    pid = str(p_id)

    if pid not in cart:
        return redirect("blog:cart_list")

    # 수량 파싱
    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    if qty < 1:
        qty = 1

    # 재고 체크
    product = MyProduct.objects.filter(id=p_id).first()
    if not product:
        cart.pop(pid, None)
        request.session["cart"] = cart
        request.session.modified = True
        return redirect("blog:cart_list")

    if product.stock <= 0:
        messages.error(request, "품절 상품은 수량을 변경할 수 없어요.")
        return redirect("blog:cart_list")

    if qty > product.stock:
        qty = product.stock
        messages.info(request, f"재고가 부족하여 수량을 {product.stock}개로 조정했어요.")

    cart[pid]["qty"] = qty
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("blog:cart_list")


def cart_remove(request, p_id):
    if request.method != "POST":
        return redirect("blog:cart_list")

    cart = request.session.get("cart", {})
    cart.pop(str(p_id), None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("blog:cart_list")
