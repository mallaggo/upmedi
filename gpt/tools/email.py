from who.mail import send_mail_message
from django.contrib.auth import get_user_model

EMAIL_TOOL = {
    "type": "function",
    "name": "send_email",
    "description":
        "여러 사람에게 메일을 보내고 필요한 경우 첨부파일을 함께 보낸다. "
        "첨부파일이 있는 경우 create_excel_file 등의 도구가 반환한 filepath 값을 attachment에 전달하여 메일을 보낸다.",
    "parameters": {
        "type": "object",
        "properties": {
            "to": {
                "type": "array",
                "description": "수신자 목록(사용자 이름 또는 이메일 주소)",
                "items": {
                    "type": "string",
                    "description": "사용자 이름 또는 이메일 주소"
                }
            },
            "subject": {
                "type": "string",
                "description": "메일 제목"
            },
            "body": {
                "type": "string",
                "description": "메일 내용"
            },
            "attachment": {
                "type": "string",
                "description": "첨부파일 경로. create_excel_file이 반환한 filepath 값을 사용한다. 첨부파일이 없으면 생략한다."
            }
        },
        "required": [
            "to",
            "subject",
            "body"
        ]
    }
}


User = get_user_model()

def send_email(
    to,
    subject,
    body,
    attachment="",
    context=None,
):
    try:

        # 최종 수신자 이메일 목록
        emails = []

        for receiver in to:

            receiver = receiver.strip()

            # 이메일 주소면 그대로 사용
            if "@" in receiver:
                emails.append(receiver)
                continue

            # username으로 사용자 조회
            user = User.objects.filter(username__iexact=receiver).first()

            if user is None:
                return {
                    "success": False,
                    "message": f"'{receiver}' 사용자를 찾을 수 없습니다."
                }

            if not user.email:
                return {
                    "success": False,
                    "message": f"'{receiver}' 사용자의 이메일이 등록되어 있지 않습니다."
                }

            emails.append(user.email)

        # 메일 발송
        send_mail_message(
            to=emails,
            subject=subject,
            text_content=body,
            attachment=attachment,
        )
        return {
            "success": True,
            "message": "메일 전송 성공"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
