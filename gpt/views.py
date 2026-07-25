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

규칙

1. 상품 조회 또는 상품 검색 요청은 반드시 search_product Tool을 사용한다.

2. 엑셀 파일 생성을 요청한 경우에만 create_excel_file Tool을 사용한다.

3. 메일 발송을 요청한 경우에만 send_email Tool을 사용한다.

4. 하나의 요청에 여러 작업이 포함되어 있으면 모든 작업이 완료될 때까지 필요한 Tool을 계속 호출한다.

예:
상품 검색 → search_product
엑셀 생성 → create_excel_file
메일 발송 → send_email

중간에 사용자에게 답변하지 않는다.
모든 Tool 호출이 끝난 후 최종 답변을 작성한다.

Tool을 호출하지 않고 작업이 완료된 것처럼 설명하거나,
가상의 다운로드 링크를 생성하거나,
메일을 보냈다고 답변해서는 안 된다.
같은 Tool을 동일한 인수로 두 번 이상 연속 호출해서는 안 된다.

5. Tool의 결과만을 근거로 답변한다.

6. Tool 검색 결과가 없으면
"등록된 상품이 없습니다."
라고만 답변한다.

7. 사용자가 메일을 보낼 때 사람 이름이나 아이디를 말하면 to 배열에 그대로 넣어라.
이메일 주소를 말하면 이메일 주소를 그대로 넣어라.
여러 명이면 to 배열에 모두 넣어라.

8. 등록되지 않은 상품을 추측하지 않는다.

9. 사용자가 요청하지 않은 작업은 수행하지 않는다.

10. 답변은 간결하게 작성한다.
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

            uploaded = client.files.create(
                file=(
                    uploaded_file.name,
                    uploaded_file.read(),
                    uploaded_file.content_type
                ),
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
        # context.remove("create_excel_file")

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



