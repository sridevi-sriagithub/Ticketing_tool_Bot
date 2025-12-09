 
# import os
# from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings

# APP_ID = os.getenv("MICROSOFT_APP_ID", "")
# APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")

# adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
# adapter = BotFrameworkAdapter(adapter_settings)
# # 
"""""
Bot Framework Adapter Configuration
Handles authentication and communication with Microsoft Bot Service
LOCAL TESTING MODE (NO AUTH)
"""
import logging
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings

logger = logging.getLogger(__name__)


# ✅ Error handler for the adapter
async def on_error(context, error):
    """
    Global error handler for bot adapter
    """
    logger.error(f"Bot error: {error}", exc_info=True)
    await context.send_activity("❌ Sorry, something went wrong. Please try again later.")


# ✅ LOCAL TESTING MODE — NO AUTHENTICATION
adapter_settings = BotFrameworkAdapterSettings(
    app_id=None,
    app_password=None
)

# ✅ Create the bot adapter
adapter = BotFrameworkAdapter(adapter_settings)

# ✅ Set error handler
adapter.on_turn_error = on_error
