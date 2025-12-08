 
# import os
# from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings

# APP_ID = os.getenv("MICROSOFT_APP_ID", "")
# APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")

# adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
# adapter = BotFrameworkAdapter(adapter_settings)
# # 
"""
Bot Framework Adapter Configuration
Handles authentication and communication with Microsoft Bot Service
"""
import os
import logging
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity

logger = logging.getLogger(__name__)


# Get credentials from environment variables
APP_ID = os.getenv("MICROSOFT_APP_ID", "")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")

# Log configuration (hide password for security)
logger.info(f"Bot Adapter initialized with APP_ID: {APP_ID[:8]}..." if APP_ID else "No APP_ID configured")


# Error handler for the adapter
async def on_error(context, error):
    """
    Global error handler for bot adapter
    """
    logger.error(f"Bot error: {error}", exc_info=True)
    
    # Send a message to the user
    await context.send_activity("Sorry, something went wrong. Please try again later.")


# Create adapter settings
adapter_settings = BotFrameworkAdapterSettings(
    app_id=APP_ID,
    app_password=APP_PASSWORD
)

# Create the bot adapter
adapter = BotFrameworkAdapter(adapter_settings)

# Set error handler
adapter.on_turn_error = on_error