 
import json
from django.http import HttpResponse
from botbuilder.schema import Activity
from .adapter import adapter
from .bot_main import MainBot

bot = MainBot()

async def messages(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization", "")

        response = await adapter.process_activity(activity, auth_header, bot.on_turn)
        return HttpResponse(status=200)

    return HttpResponse("Bot endpoint active", status=200)
