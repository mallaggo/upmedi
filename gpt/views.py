import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from openai import OpenAI
import json
from .executor import ToolExecutor
from .models import ChatMessage, ChatSession
from .tools import TOOL_SCHEMAS, TOOL_FUNCTIONS
from .context import ToolContext


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)
tool_executor = ToolExecutor(client)

INSTRUCTIONS = """
당신은 우리 쇼핑몰 ERP 시스템의 AI 비서이다.

사용자의 요청을 해결하기 위해 필요한 Tool만 사용한다.

==========================
[상품 검색 규칙]
==========================

1. 사용자가 우리 쇼핑몰의 상품을 조회하거나 검색하는 경우에는
반드시 search_product Tool을 사용한다.

예)
- 우리 쇼핑몰
- 우리 상품
- 내 상품
- 나의 상품
- 등록된 상품
- 재고
- 쇼핑몰 상품

2. 사용자가 나라장터 종합쇼핑몰의 계약상품을 검색하는 경우에는
반드시 search_shopping Tool을 사용한다.

예)
- 종합쇼핑몰
- 계약상품
- 물품식별번호
- 계약된 상품
- 나라장터 종합쇼핑몰 상품
- 조달청 종합쇼핑몰 상품

2-1. 사용자가 나라장터의 입찰공고를 조회하거나 검색하는 경우에는
반드시 search_bid Tool을 사용한다.

예)
- 입찰
- 입찰공고
- 입찰정보
- 공고 검색
- 공고 조회
- 나라장터 입찰
- 조달청 입찰
- 노트북 입찰
- 모니터 입찰
- 복합기 입찰
- 물품 입찰

2-2. 사용자가 "나라장터" 또는 "조달청"이라고만 말한 경우에는
종합쇼핑몰 상품을 의미하는지,
입찰공고를 의미하는지 명확하지 않으면
Tool을 호출하지 말고 반드시 아래와 같이 질문한다.

"나라장터 종합쇼핑몰 상품을 검색할까요?
아니면 입찰공고를 검색할까요?"

추측해서 Tool을 호출해서는 안 된다.

2-3.
나라장터 입찰공고 결과는 다음 형식으로 출력한다.

- 번호를 붙여 출력한다.
- 공고명을 가장 먼저 출력한다.
- 기관명, 계약방식, 마감일을 줄바꿈하여 출력한다.
- 상세보기 URL은 마지막 줄에 출력한다.
- 검색 결과가 많으면 처음 10건만 보여주고 총 건수를 함께 표시한다.


3. 검색 대상이 명확하지 않으면
Tool을 호출하지 말고 반드시 아래와 같이 질문한다.

"우리 쇼핑몰에서 검색할까요?
아니면 나라장터에서 검색할까요?"

추측해서 Tool을 호출해서는 안 된다.

4. Tool을 사용할 수 있는 상황에서는
일반 지식으로 상품 정보를 생성하거나
추측해서 답변하지 않는다.

반드시 Tool을 먼저 사용한다.

5. 등록되지 않은 상품을 추측하거나 만들어서 답변하지 않는다.

5-1. search_product의 검색 결과가 없으면

"등록된 상품이 없습니다."

라고만 답변한다.

5-2. search_bid의 검색 결과가 없으면

"조회된 입찰공고가 없습니다."

라고 답변한다.

==========================
[엑셀 규칙]
==========================

7. 엑셀 파일 생성을 요청한 경우에만
create_excel_file Tool을 사용한다.

==========================
[메일 규칙]
==========================

8. 메일 발송을 요청한 경우에만
send_email Tool을 사용한다.

9. 사용자가 사람 이름이나 아이디를 말하면
to 배열에 그대로 넣는다.

사용자가 이메일 주소를 말하면
이메일 주소를 그대로 넣는다.

여러 명이면 to 배열에 모두 넣는다.

==========================
[엑셀 상품 등록]
==========================

10. 엑셀 파일의 상품 등록을 요청한 경우에는
반드시 read_excel_products Tool을 먼저 호출한다.

11. read_excel_products의 결과가 success=True이면
반드시 save_products Tool을 호출하여
상품을 데이터베이스에 저장한다.

==========================
[Tool 실행 규칙]
==========================

12. 하나의 요청에 여러 작업이 포함되어 있으면
모든 작업이 완료될 때까지 필요한 Tool을 계속 호출한다.

예)

상품 검색
→ search_product

나라장터 종합쇼핑몰 상품 검색
→ search_shopping

나라장터 입찰공고 검색
→ search_bid

엑셀 생성
→ create_excel_file

메일 발송
→ send_email

엑셀 상품 등록
→ read_excel_products
→ save_products

13. 중간에 사용자에게 답변하지 않는다.

모든 Tool 호출이 끝난 후
최종 답변을 작성한다.

14. Tool을 호출하지 않고
작업이 완료된 것처럼 답변해서는 안 된다.

15. 가상의 다운로드 링크를 생성해서는 안 된다.

16. 메일을 보내지 않았는데
보냈다고 답변해서는 안 된다.

17. 같은 Tool을 동일한 인수로
두 번 이상 연속 호출해서는 안 된다.

18. Tool의 결과만을 근거로 답변한다.

19. Tool 결과가 success=False이면
다음 Tool을 호출하지 말고
오류 내용을 사용자에게 답변한다.

20. 사용자가 요청하지 않은 작업은 수행하지 않는다.

21. 답변은 간결하게 작성한다.
"""


@login_required(login_url='who:login')
def chat_page(request, session_id=None):

    if session_id:
        session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

    else:

        session = ChatSession.objects.filter(
            user=request.user
        ).first()

        if not session:
            session = ChatSession.objects.create(
                user=request.user,
                title=""
            )

    messages = ChatMessage.objects.filter(
        session=session
    )

    sessions = ChatSession.objects.filter(
        user=request.user
    )

    return render(
        request,
        "gpt/chat.html",
        {
            "messages": messages,
            "sessions": sessions,
            "current_session": session,
        }
    )

@login_required(login_url='who:login')
def new_chat(request):
    session = ChatSession.objects.create(
        user=request.user,
        title=""
    )

    return redirect(
        'gpt:chat_session',
        session_id=session.id
    )

@login_required(login_url='who:login')
def delete_chat(request, session_id):

    session = get_object_or_404(
        ChatSession,
        id=session_id,
        user=request.user
    )

    session.delete()

    return redirect('gpt:chat')


def build_user_input(question, file_id):

    if file_id:

        return [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file_id
                    },
                    {
                        "type": "input_text",
                        "text": question
                    }
                ]
            }
        ]

    return question


def create_response(session, user_input):

    kwargs = {
        "model": "gpt-5",
        "instructions": INSTRUCTIONS,
        "tools": TOOL_SCHEMAS,
        "input": user_input,
    }

    if session.last_response_id:
        kwargs["previous_response_id"] = session.last_response_id

    return client.responses.create(**kwargs)



def save_answer(session, response):

    answer = response.output_text

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=answer
    )

    session.last_response_id = response.id
    session.save(update_fields=["last_response_id"])

    return answer



@login_required(login_url='who:login')
def ask_gpt(request):

    if request.method != "POST":
        return JsonResponse(
            {"answer": "POST 요청만 허용됩니다."},
            status=405
        )

    try:

        # -----------------------------
        # 사용자 입력
        # -----------------------------
        question = request.POST.get("question", "")
        session_id = request.POST.get("session_id")
        uploaded_file = request.FILES.get("file")

        file_id = None

        if uploaded_file:

            # -----------------------------
            # media/excel 폴더 저장
            # -----------------------------
            excel_dir = os.path.join(
                settings.MEDIA_ROOT,
                "excel"
            )

            os.makedirs(
                excel_dir,
                exist_ok=True
            )

            file_path = os.path.join(
                excel_dir,
                uploaded_file.name
            )

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)


            # -----------------------------
            # 저장된 파일을 OpenAI 업로드
            # -----------------------------
            with open(file_path, "rb") as f:

                uploaded = client.files.create(
                    file=f,
                    purpose="user_data"
                )

            file_id = uploaded.id

        # -----------------------------
        # 현재 대화방
        # -----------------------------
        session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        # -----------------------------
        # 제목 자동 생성
        # -----------------------------
        if not session.title:
            session.title = question[:20]
            session.save(update_fields=["title"])

        # -----------------------------
        # 사용자 질문 저장
        # -----------------------------
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        # -----------------------------
        # GPT 입력 생성
        # -----------------------------
        user_input = build_user_input(
            question,
            file_id
        )

        # -----------------------------
        # GPT 호출
        # -----------------------------

        context = ToolContext(session)

        if uploaded_file:
            context.set(
                "uploaded_filename",
                uploaded_file.name
            )

        response = create_response(
            session,
            user_input
        )

        response = tool_executor.run(
            response,
            context
        )

        answer = save_answer(
            session,
            response
        )

        # 추가
        excel = context.get("create_excel_file")
        download_url = None

        if excel and excel.get("success"):
            download_url = excel.get("download_url")

        # 반환
        return JsonResponse({
            "answer": answer,
            "title": session.title,
            "download_url": download_url
        })

    except Exception as e:

        return JsonResponse({
            "answer": f"오류 발생 : {str(e)}"
        })



