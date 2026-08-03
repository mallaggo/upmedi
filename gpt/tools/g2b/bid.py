import requests
from datetime import datetime, timedelta
from django.conf import settings
from urllib.parse import unquote


BID_TOOL = {
    "type": "function",
    "name": "search_bid",
    "description": (
        "나라장터 물품 입찰공고를 검색한다. "
        "입찰공고, 입찰, 공고 조회 요청에 사용한다. "
        "종합쇼핑몰 계약상품 검색에는 사용하지 않는다."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "검색할 품명(예: 노트북, 모니터, 복합기)"
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



def search_bid(
    context=None,
    keyword=None,
    page=1,
    rows=10,
):

    # 최근 30일
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    url = (
        "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/"
        "getBidPblancListInfoThngPPSSrch"
    )

    params = {
        "serviceKey": unquote(settings.NARA_API_KEY),
        "pageNo": page,
        "numOfRows": rows,
        "type": "json",

        # 조회구분 : 공고게시일시
        "inqryDiv": "1",

        # 조회기간
        "inqryBgnDt": start_date.strftime("%Y%m%d0000"),
        "inqryEndDt": end_date.strftime("%Y%m%d2359"),

        # 공고명 검색
        "bidNtceNm": keyword,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    result = response.json()

    body = result.get("response", {}).get("body", {})

    items = body.get("items", [])

    # 결과가 1건이면 dict로 오는 경우가 있어서 처리
    if isinstance(items, dict):
        items = [items]

    data = []

    for item in items:
        data.append({
            "bid_no": item.get("bidNtceNo"),
            "title": item.get("bidNtceNm"),
            "agency": item.get("ntceInsttNm"),
            "demand": item.get("dminsttNm"),
            "method": item.get("cntrctCnclsMthdNm"),
            "close_date": item.get("bidClseDt"),
            "open_date": item.get("opengDt"),
            "detail_url": item.get("bidNtceDtlUrl"),
        })

    return {
        "success": True,
        "keyword": keyword,
        "count": len(data),
        "data": data,
    }