# """
# Adaptive Cards for Microsoft Teams Bot
# Rich UI components for better user interaction
# """
# from botbuilder.schema import Attachment, HeroCard, CardImage, CardAction, ActionTypes


# def create_welcome_card(user_name: str) -> Attachment:
#     """
#     Create a welcome card with action buttons
#     """
#     card = HeroCard(
#         title=f"👋 Hello, {user_name}!",
#         text="Welcome to the Ticketing Support Bot. I'm here to help you manage your support tickets.",
#         images=[
#             CardImage(
#                 url="https://via.placeholder.com/350x150/4A90E2/ffffff?text=Support+Bot"
#             )
#         ],
#         buttons=[
#             CardAction(
#                 type=ActionTypes.im_back,
#                 title="Create Ticket",
#                 value="ticket create"
#             ),
#             CardAction(
#                 type=ActionTypes.im_back,
#                 title="View My Tickets",
#                 value="ticket list"
#             ),
#             CardAction(
#                 type=ActionTypes.im_back,
#                 title="Help",
#                 value="help"
#             )
#         ]
#     )
#     return Attachment(
#         content_type="application/vnd.microsoft.card.hero",
#         content=card
#     )


# def create_ticket_card() -> Attachment:
#     """
#     Create a ticket creation card
#     """
#     card = HeroCard(
#         title="🎫 Create New Ticket",
#         text="To create a ticket, please provide the following information:",
#         buttons=[
#             CardAction(
#                 type=ActionTypes.open_url,
#                 title="Open Ticket Form",
#                 value="https://your-domain.com/create-ticket"  # Replace with your URL
#             ),
#             CardAction(
#                 type=ActionTypes.im_back,
#                 title="Cancel",
#                 value="help"
#             )
#         ]
#     )
#     return Attachment(
#         content_type="application/vnd.microsoft.card.hero",
#         content=card
#     )


# def create_adaptive_card_welcome() -> dict:
#     """
#     Create an advanced Adaptive Card (for future use)
#     More interactive than Hero Cards
#     """
#     return {
#         "contentType": "application/vnd.microsoft.card.adaptive",
#         "content": {
#             "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
#             "type": "AdaptiveCard",
#             "version": "1.4",
#             "body": [
#                 {
#                     "type": "TextBlock",
#                     "text": "Ticketing Support Bot",
#                     "weight": "bolder",
#                     "size": "large",
#                     "wrap": True
#                 },
#                 {
#                     "type": "TextBlock",
#                     "text": "Manage your support tickets easily",
#                     "wrap": True,
#                     "spacing": "small"
#                 },
#                 {
#                     "type": "Image",
#                     "url": "https://via.placeholder.com/400x200/4A90E2/ffffff?text=Support",
#                     "size": "stretch"
#                 }
#             ],
#             "actions": [
#                 {
#                     "type": "Action.Submit",
#                     "title": "Create Ticket",
#                     "data": {"action": "create_ticket"}
#                 },
#                 {
#                     "type": "Action.Submit",
#                     "title": "View Tickets",
#                     "data": {"action": "view_tickets"}
#                 }
#             ]
#         }
#     }

from botbuilder.schema import Attachment, HeroCard, CardImage, CardAction, ActionTypes

# def create_welcome_card(user_name: str) -> Attachment:
#     card = HeroCard(
#         title=f"👋 Hello, {user_name}!",
#         text="Welcome to the Ticketing Support Bot.",
#         images=[CardImage(url="https://via.placeholder.com/350x150")],
#         buttons=[
#             CardAction(type=ActionTypes.im_back, title="Create Ticket", value="ticket create"),
#             CardAction(type=ActionTypes.im_back, title="View Tickets", value="ticket list"),
#             CardAction(type=ActionTypes.im_back, title="Help", value="help"),
#         ],
#     )

#     return Attachment(
#         content_type="application/vnd.microsoft.card.hero",
#         content=card,
#     )


def create_ticket_card() -> Attachment:
    card = HeroCard(
        title="🎫 Create New Ticket",
        text="Click below to create a ticket",
        buttons=[
            CardAction(type=ActionTypes.im_back, title="Create Ticket", value="ticket create"),
            CardAction(type=ActionTypes.im_back, title="Cancel", value="help"),
        ],
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.hero",
        content=card,
    )

# bot/cards.py
from botbuilder.schema import Attachment, HeroCard, CardImage, CardAction, ActionTypes


def create_welcome_card(user_name: str) -> Attachment:
    card = HeroCard(
        title=f"👋 Hello, {user_name}!",
        text=(
            "I'm your Ticketing Bot.\n\n"
            "You can login, create tickets, list tickets and assign tickets."
        ),
        images=[
            CardImage(
                url="https://via.placeholder.com/350x150/4A90E2/ffffff?text=Ticket+Bot"
            )
        ],
        buttons=[
            CardAction(type=ActionTypes.im_back, title="Help", value="help"),
            CardAction(type=ActionTypes.im_back, title="Create Ticket", value="ticket create"),
            CardAction(type=ActionTypes.im_back, title="List Tickets", value="ticket list"),
        ],
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.hero",
        content=card,
    )
