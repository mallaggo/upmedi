import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_mail_message(
    to,
    subject,
    text_content,
    html_content=None,
    attachment=""
):
    """
    공통 메일 발송 함수

    Parameters
    ----------
    to : list[str]
    subject : str
    text_content : str
    html_content : str | None
    attachment : str
    """

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
    )

    if html_content:
        msg.attach_alternative(html_content, "text/html")

    if attachment:
        if os.path.exists(attachment):
            msg.attach_file(attachment)
        else:
            raise FileNotFoundError(f"첨부파일이 존재하지 않습니다.\n{attachment}")

    msg.send()

    return True