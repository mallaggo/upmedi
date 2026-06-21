from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from openai import OpenAI

import json

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

@login_required(login_url='who:login')
def chat_page(request):
    return render(request, "gpt/chat.html")


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

        response = client.responses.create(
            model="gpt-5-mini",
            input=question
        )

        return JsonResponse({
            "answer": response.output_text
        })

    except Exception as e:

        return JsonResponse({
            "answer": f"오류 발생 : {str(e)}"
        })