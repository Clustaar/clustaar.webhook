# clustaar.webhook
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`clustaar.webhook` is a framework to build webhooks for the [clustaar platform](https://clustaar.com).

More documentation is available for building webhooks on https://developers.clustaar.com
![Clustaar Logo](https://clustaar.com/wp-content/uploads/2016/07/logo-black-1.png)

## Example

Here is a webhook that will trigger an `handler` function each times it receives a `conversation.step_reached` event.

```python
from clustaar.webhook import Webhook, events
from clustaar.schemas.models import StepReachedResponse, ConversationSession

def handler(request, response, notification):
    session = ConversationSession(values={"name": "John"})
    return StepReachedResponse(actions=[], session=session)


app = Webhook()
app.on(events.CONVERSATION_STEP_REACHED, handler)
```
## Routing
### Event
Routing is achieved by specifying an event name to the `on()` method while configuring your webhook :
```python
app.on(events.CONVERSATION_STEP_REACHED, handler)
```

### Filters

If you want to add some condition to route events based on the request received you can use filters.

In this example, `handler` will receive the requests only when the event is of type `events.CONVERSATION_STEP_REACHED` and the value of the JSON key `data.step.id` equals `"507f191e810c19729de860ea"` :  
```python
from clustaar.webhook.filters import JSONKeyEquals
app.on(events.CONVERSATION_STEP_REACHED,
       handler,
       filter=JSONKeyEquals("data.step.id", "507f191e810c19729de860ea"))
```

#### JSONKeyEquals

Validates that a JSON key equals an expected value.
```python
data = {
    "user": {
        "id": 1
    }
}
filter = JSONKeyEquals("user.id", 1)
assert filter(data)
data["user"]["id"] = 2
assert not filter(data)
```

#### JSONKeyIn

Validates that a key is present in a defined set of values.
```python
data = {
    "user": {
        "id": 1
    }
}
filter = JSONKeyIn("user.id", [1, 2])
assert filter(data)
data["user"]["id"] = 2
assert filter(data)
data["user"]["id"] = 3
assert not filter(data)
```

#### JSONKeyExists

Validates that a JSON key is present.
```python
data = {
    "user": {
        "id": 1
    }
}
filter = JSONKeyExists("user.id")
assert filter(data)
del data["user"]["id"]
assert not filter(data)
```

#### StepID

Validates that the `data.step.id` correspond to the expected id.
```python
data = {
	"data": {
	    "step": {
	        "id": "507f191e810c19729de860ea"
	    }
    }
}
filter = StepID("507f191e810c19729de860ea")
assert filter(data)
del data["data"]["step"]["id"]
assert not filter(data)
```
If you pass a list of step IDs to the `StepID` filter it will validate the the `data.step.id` is present in the list.

## Security

### Request signature
If you want to validate the signature of the requests sent by clustaar, you need to provide a private key.  
This private key must be set in your bot's webhook configuration.

```python
app = Webhook(private_key="XXXXXXXXXX")
```

### Authentication
If you want to add some authentication to your application you can pass the HTTP basic authentication credentials that you defined in your webhook's configuration.

```python
app = Webhook(auth_username="XXXXXXXXXX", auth_password="YYYYYYYYY")
```
