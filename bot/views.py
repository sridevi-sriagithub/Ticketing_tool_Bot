 
# import json
# from django.http import HttpResponse
# from botbuilder.schema import Activity
# from .adapter import adapter
# from .bot_main import MainBot

# bot = MainBot()

# async def messages(request):
#     if request.method == "POST":
#         body = json.loads(request.body.decode("utf-8"))
#         activity = Activity().deserialize(body)
#         auth_header = request.headers.get("Authorization", "")

#         # response = await adapter.process_activity(activity, auth_header, bot.on_turn)
#         return HttpResponse(status=200)

#     return HttpResponse("Bot endpoint active", status=200)

"""
Django Views for Bot Endpoint
Handles incoming requests from Microsoft Bot Service
"""
import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from botbuilder.schema import Activity
from asgiref.sync import async_to_sync
from .adapter import adapter
from .bot_main import MainBot

logger = logging.getLogger(__name__)

# Initialize bot instance
bot = MainBot()


@csrf_exempt
@require_http_methods(["GET", "POST"])
def messages(request):
    """
    Main endpoint for bot messages
    Microsoft Bot Service will POST activity messages here
    """
    
    # Handle GET request (for bot verification)
    if request.method == "GET":
        return JsonResponse({
            "status": "active",
            "message": "Bot endpoint is running",
            "version": "1.0"
        })
    
    # Handle POST request (actual bot messages)
    try:
        # Parse incoming activity
        body = json.loads(request.body.decode("utf-8"))
        activity = Activity().deserialize(body)
        
        # Get authorization header
        auth_header = request.headers.get("Authorization", "")
        
        logger.info(f"Received activity: {activity.type} from {activity.from_property.name}")
        
        # Process the activity
        async_to_sync(adapter.process_activity)(
            activity, 
            auth_header, 
            bot.on_turn
        )
        
        return HttpResponse(status=200)
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request body: {e}")
        return JsonResponse(
            {"error": "Invalid JSON"}, 
            status=400
        )
    
    except Exception as e:
        logger.error(f"Error processing bot message: {e}", exc_info=True)
        return JsonResponse(
            {"error": "Internal server error"}, 
            status=500
        )


@csrf_exempt
def health_check(request):
    """
    Health check endpoint
    """
    return JsonResponse({
        "status": "healthy",
        "service": "bot",
        "version": "1.0"
    })


@csrf_exempt
def bot_info(request):
    """
    Bot information endpoint
    """
    import os
    return JsonResponse({
        "bot_name": "Ticketing Support Bot",
        "version": "1.0.0",
        "app_id_configured": bool(os.getenv("MICROSOFT_APP_ID")),
        "endpoints": {
            "messages": "/bot/api/messages",
            "health": "/bot/health",
            "info": "/bot/info"
        }
    })