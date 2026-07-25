from difflib import get_close_matches
from blog.models import MyProduct
from django.db.models import Value
from django.db.models.functions import Replace


SEARCH_PRODUCT_TOOL = {
    "type": "function",
    "name": "search_product",
    "description": (
    "우리 쇼핑몰 데이터베이스(MyProduct)에 등록된 상품을 검색한다. "
    "사용자가 상품명, 카테고리, 가격, 재고 등 상품을 찾거나 조회하는 요청을 하면 반드시 이 Tool을 호출한다. "
    "등록되지 않은 상품을 추측하거나 일반적인 상품 추천을 하지 않는다."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "keyword": {
                "type": "string",
                "description": "상품명"
            },

            "category": {
                "type": "string",
                "description": "카테고리명"
            },

            "min_price": {
                "type": "integer",
                "description": "최소 가격"
            },

            "max_price": {
                "type": "integer",
                "description": "최대 가격"
            },
            "stock": {
            "type": "integer",
            "description": "재고가 이 값 이하인 상품 검색"
            }

        }
    }
}


def search_product(keyword=None, category=None, min_price=None, max_price=None, stock=None):


    products = MyProduct.objects.select_related("category")

    # 기본값은 사용자가 입력한 검색어
    real_name = keyword

    if keyword:
        products = products.annotate(
            clean_name=Replace("name", Value(" "), Value(""))
        ).filter(
            clean_name__icontains=keyword.replace(" ", "")
        )

        # 정확히 찾지 못하면 유사도 검색
        if not products.exists():

            names = list(
                MyProduct.objects.values_list("name", flat=True)
            )

            match = get_close_matches(
                keyword.replace(" ", ""),
                [name.replace(" ", "") for name in names],
                n=1,
                cutoff=0.5
            )



            if match:
                for name in names:
                    if name.replace(" ", "") == match[0]:
                        real_name = name
                        break

                products = MyProduct.objects.select_related(
                    "category"
                ).filter(
                    name=real_name
                )

    if category:
        products = products.filter(category__name__icontains=category)

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    if stock is not None:
        products = products.filter(stock__lte=stock)

    result = []

    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category.name,
            "price": p.price,
            "stock": p.stock,
        })

    if not result:
        return {
            "success": False,
            "message": "등록된 상품이 없습니다.",
            "corrected_keyword": real_name,
            "data": []
        }

    return {
        "success": True,
        "message": f"{len(result)}개의 상품을 찾았습니다.",
        "corrected_keyword": real_name,
        "data": result
    }