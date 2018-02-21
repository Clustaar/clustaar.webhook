from clustaar.webhook import Webhook, events
from clustaar.schemas.models import StepReachedResponse, ConversationSession


def handler(request, response, notification):
    print(notification.topic)
    session = ConversationSession(values={"name": "John"})
    return StepReachedResponse(actions=[], session=session)


app = Webhook()
app.on(events.CONVERSATION_STEP_REACHED, handler)
