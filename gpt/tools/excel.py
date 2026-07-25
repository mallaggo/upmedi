import os
from django.conf import settings
from openpyxl import Workbook


EXCEL_TOOL = {
    "type": "function",
    "name": "create_excel_file",
    "description": (
        "엑셀(.xlsx) 파일을 생성한다. "
        "다른 Tool의 결과(data)를 이용해서도 엑셀을 생성할 수 있다. "
        "headers에는 컬럼명을, rows에는 데이터 행을 전달한다."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string"
            },
            "headers": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "rows": {
                "type": "array",
                "items": {
                    "type": "array"
                }
            }
        },
        "required": [
            "filename",
            "headers",
            "rows"
        ]
    }
}


def create_excel_file(filename, headers, rows):

    # 파일명 보안 처리
    filename = os.path.basename(filename)

    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # media/excel 폴더
    excel_dir = os.path.join(settings.MEDIA_ROOT, "excel")
    os.makedirs(excel_dir, exist_ok=True)

    file_path = os.path.join(excel_dir, filename)

    # Workbook 생성
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # 헤더
    ws.append(headers)

    # 데이터
    for row in rows:
        ws.append(row)

    # 저장
    wb.save(file_path)


    return {
        "success": True,
        "filename": filename,
        "filepath": file_path,
        "download_url": f"/media/excel/{filename}",
        "message": "엑셀 파일이 생성되었습니다."
    }