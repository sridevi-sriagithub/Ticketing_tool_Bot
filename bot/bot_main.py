 
# from botbuilder.core import ActivityHandler, TurnContext

# class MainBot(ActivityHandler):
#     async def on_message_activity(self, turn_context: TurnContext):
#         text = turn_context.activity.text
#         await turn_context.send_activity(f"You said: {text}")


"""
Main Bot Logic
Handles incoming messages and bot interactions
"""
import logging
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes
from .cards import create_welcome_card, create_ticket_card

logger = logging.getLogger(__name__)


class MainBot(ActivityHandler):
    """
    Main bot class that handles all bot activities
    """
    
    async def on_message_activity(self, turn_context: TurnContext):
        """
        Handle incoming message activities
        """
        text = turn_context.activity.text.strip().lower()
        user_name = turn_context.activity.from_property.name
        
        logger.info(f"Received message from {user_name}: {text}")
        
        # Command routing
        if text in ['hello', 'hi', 'hey']:
            await self._handle_greeting(turn_context, user_name)
        
        elif text in ['help', 'commands']:
            await self._handle_help(turn_context)
        
        elif text.startswith('ticket'):
            await self._handle_ticket_command(turn_context, text)
        
        else:
            # Echo back with options
            response = f"You said: **{turn_context.activity.text}**\n\n"
            response += "Try these commands:\n"
            response += "- **hello** - Get a greeting\n"
            response += "- **help** - Show available commands\n"
            response += "- **ticket create** - Create a new ticket\n"
            response += "- **ticket list** - List your tickets"
            
            await turn_context.send_activity(MessageFactory.text(response))
    
    async def _handle_greeting(self, turn_context: TurnContext, user_name: str):
        """Handle greeting messages"""
        welcome_card = create_welcome_card(user_name)
        await turn_context.send_activity(MessageFactory.attachment(welcome_card))
    
    async def _handle_help(self, turn_context: TurnContext):
        """Handle help command"""
        help_text = """
        **Available Commands:**
        
        🔹 **hello** - Get a welcome message
        🔹 **help** - Show this help message
        🔹 **ticket create** - Create a new support ticket
        🔹 **ticket list** - View your tickets
        🔹 **ticket status [id]** - Check ticket status
        
        **Need more help?** Contact support at support@example.com
        """
        await turn_context.send_activity(MessageFactory.text(help_text))
    
    async def _handle_ticket_command(self, turn_context: TurnContext, text: str):
        """Handle ticket-related commands"""
        if 'create' in text:
            # Show ticket creation card
            ticket_card = create_ticket_card()
            await turn_context.send_activity(MessageFactory.attachment(ticket_card))
        
        elif 'list' in text:
            # TODO: Integrate with your Django backend to fetch tickets
            response = "**Your Recent Tickets:**\n\n"
            response += "1. #1001 - Login Issue (Open)\n"
            response += "2. #1002 - Bug Report (In Progress)\n"
            response += "3. #1003 - Feature Request (Closed)\n\n"
            response += "_This is sample data. Integration coming soon!_"
            await turn_context.send_activity(MessageFactory.text(response))
        
        else:
            await turn_context.send_activity(
                MessageFactory.text("Invalid ticket command. Try 'ticket create' or 'ticket list'")
            )
    
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Handle when new members are added to the conversation
        """
        for member in members_added:
            # Don't greet the bot itself
            if member.id != turn_context.activity.recipient.id:
                welcome_message = f"""
                👋 Welcome to the Ticketing Support Bot!
                
                I can help you with:
                - Creating support tickets
                - Checking ticket status
                - Getting help and information
                
                Type **help** to see all available commands.
                """
                await turn_context.send_activity(MessageFactory.text(welcome_message))
    
    async def on_conversation_update_activity(self, turn_context: TurnContext):
        """
        Handle conversation update events
        """
        logger.info("Conversation updated")
        await super().on_conversation_update_activity(turn_context)