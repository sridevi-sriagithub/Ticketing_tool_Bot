 
from botbuilder.core import ActivityHandler, TurnContext

class MainBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text
        await turn_context.send_activity(f"You said: {text}")
