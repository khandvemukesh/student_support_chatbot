import markdown
from django.shortcuts import render

from .graph import graph


def home(request):
    response = None
    error = None

    if request.method == "POST":
        message = request.POST.get("message", "").strip()

        if message:
            try:
                result = graph.invoke({
                    "message": message,
                    "response": ""
                })

                response = result.get("response", "")
                response = markdown.markdown(
                response
            )

            except Exception as e:
                print("CHATBOT ERROR:", repr(e))
                error = str(e)

    return render(
        request,
        "chatbot/home.html",
        {
            "response": response,
            "error": error,
        }
    )
