from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ChatMessage
from openai import OpenAI

import json

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

@login_required(login_url='who:login')
def chat_page(request):
    messages = ChatMessage.objects.filter(
        user=request.user
    )

    return render( request,"gpt/chat.html", {"messages": messages })



@login_required(login_url='who:login')
def ask_gpt(request):

    if request.method != "POST":
        return JsonResponse(
            {"answer": "POST 요청만 허용됩니다."},
            status=405
        )

    try:

        data = json.loads(request.body)

        question = data.get("question", "")

        # 사용자 질문 저장

        ChatMessage.objects.create(
            user=request.user,
            role="user",
            content=question
        )

        response = client.responses.create(
            model="gpt-5-mini",
            input=question
        )

        answer = response.output_text
        # GPT 답변 저장

        ChatMessage.objects.create(
            user=request.user,
            role="assistant",
            content=answer
        )

        return JsonResponse({
            "answer": answer
        })

    except Exception as e:

        return JsonResponse({
            "answer": f"오류 발생 : {str(e)}"
        })



