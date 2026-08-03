from django.conf import settings

SHOPPING_TOOL = {
    "type": "function",
    "name": "search_shopping",
    "description": (
        "나라장터 종합쇼핑몰의 계약상품을 검색한다. "
    "이미 계약되어 판매 중인 상품을 조회할 때만 사용한다. "
    "입찰공고 조회에는 사용하지 않는다."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "검색할 품명"
            },
            "company": {
                "type": "string",
                "description": "계약업체명"
            },
            "product_id": {
                "type": "string",
                "description": "물품식별번호"
            },
            "page": {
                "type": "integer",
                "description": "페이지 번호",
                "default": 1
            },
            "rows": {
                "type": "integer",
                "description": "조회 건수",
                "default": 10
            }
        }
    }
}


def search_shopping(
    context=None,
    keyword=None,
    company=None,
    product_id=None,
    page=1,
    rows=10,
):
    return {
        "success": True,
        "message": "search_shopping 함수 호출 성공",
        "count": 0,
        "data": []
    }