from clustaar.webhook import Webhook, events


def handler(request, response, event):
    return StepReachedResponse(actions=[])

webhook = Webhook(auth_username="user", auth_password="password", private_key="XXXXX")

webhook.on(events.CONVERSATION_STEP_REACHED, handler, filter=StepID(["a1"]))
webhook.on(events.CONVERSATION_STEP_REACHED, handler, StepUserDataKeyEquals("action", "subscribe"))
webhook.on("conversation.step_reached", handler, StepUserDataContains("subscribe"))
StepUserDataKeyExists
