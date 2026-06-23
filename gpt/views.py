from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ChatMessage,ChatSession
from openai import OpenAI
import json
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


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

@login_required(login_url='who:login')
def ask_gpt(request):

    if request.method != "POST":
        return JsonResponse(
            {"answer": "POST 요청만 허용됩니다."},
            status=405
        )

    try:

        question = request.POST.get(
            "question",
            ""
        )

        session_id = request.POST.get(
            "session_id"
        )

        uploaded_file = request.FILES.get(
            "file"
        )

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

            print("OpenAI file_id =", file_id)

        # 현재 선택된 대화방 조회

        session = ChatSession.objects.get(
            id=session_id,
            user=request.user
        )
        if not session.title:
            session.title = question[:20]

            session.save()


        # 사용자 질문 저장

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        if file_id:

            response = client.responses.create(
                model="gpt-5-mini",

                instructions="""
                   기본적으로 짧고 핵심만 답변하라.
                    사용자가 자세히 설명해달라고 요청하지 않으면
                    3문장 이내로 답변하라.
                    숫자, 합계, 개수, 결과는 먼저 제시하라.
                    불필요한 인사말과 장황한 설명은 생략하라.
                   """,

                input=[
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
            )

        else:

            response = client.responses.create(
                model="gpt-5-mini",
                instructions="""
                기본적으로 짧고 핵심만 답변하라.
                사용자가 자세히 설명해달라고 요청하지 않으면
                3문장 이내로 답변하라.
                숫자, 합계, 개수, 결과는 먼저 제시하라.
                불필요한 인사말과 장황한 설명은 생략하라.
                """,
                input=question
            )

        answer = response.output_text
        # GPT 답변 저장

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        return JsonResponse({
            "answer": answer,
            "title": session.title
        })

    except Exception as e:

        return JsonResponse({
            "answer": f"오류 발생 : {str(e)}"
        })



