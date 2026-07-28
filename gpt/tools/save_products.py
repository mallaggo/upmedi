import os
from django.conf import settings
from django.core.files import File
from blog.models import MyCategory, MyProduct



SAVE_PRODUCTS_TOOL = {
    "type": "function",
    "name": "save_products",
    "description": "read_excel_products가 읽은 상품을 데이터베이스에 저장합니다.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
}




def save_products(context=None):
    DEFAULT_IMAGE = os.path.join(
        settings.MEDIA_ROOT,
        "products",
        "default.jpg"
    )

    excel = context.get("read_excel_products")

    if not excel:
        return {
            "success": False,
            "message": "먼저 read_excel_products를 실행하세요."
        }

    products = excel.get("data", [])

    insert_count = 0
    update_count = 0
    errors = []

    for product in products:

        try:

            # ------------------------
            # 카테고리
            # ------------------------
            category_name = product.get("category", "").strip()

            if not category_name:
                category_name = "미분류"

            category, _ = MyCategory.objects.get_or_create(
                name=category_name
            )

            # ------------------------
            # 상품 생성
            # ------------------------
            product_obj, created = MyProduct.objects.get_or_create(
                category=category,
                name=product["name"],
                defaults={
                    "price": product["price"],
                    "stock": product.get("stock", 0),
                    "short_desc": product.get("short_desc", ""),
                }
            )

            if created:

                # 기본 이미지 등록
                if (
                    not product_obj.image
                    and os.path.exists(DEFAULT_IMAGE)
                ):
                    with open(DEFAULT_IMAGE, "rb") as f:
                        product_obj.image.save(
                            os.path.basename(DEFAULT_IMAGE),
                            File(f),
                            save=False
                        )

                product_obj.save()

                insert_count += 1

            else:

                # ------------------------
                # 기존 상품 수정
                # ------------------------
                product_obj.category = category
                product_obj.price = product["price"]
                product_obj.stock = product.get("stock", 0)
                product_obj.short_desc = product.get("short_desc", "")

                product_obj.save()

                update_count += 1

        except Exception as e:

            errors.append(
                f'{product.get("name", "")}: {str(e)}'
            )

    return {
        "success": len(errors) == 0,
        "message": (
            f"신규 {insert_count}건, "
            f"수정 {update_count}건 처리했습니다."
        ),
        "insert_count": insert_count,
        "update_count": update_count,
        "errors": errors,
    }