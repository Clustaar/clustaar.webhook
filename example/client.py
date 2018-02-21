import requests
import sys


STEP_REACHED = """
{
    "botID": "4321",
    "timestamp": 1514998709,
    "topic": "conversation.step_reached",
    "data": {
        "type": "step_reached_event",
        "channel": "facebook",
        "interlocutor": {
            "id": "123",
            "location": {
                "lat": 1.0, "long": 2.4
            }
        },
        "session": {
            "values": {"name": "tintin"}
        },
        "step": {
            "actions": [
                {
                    "type": "pause_bot_action"
                }
            ],
            "id": "1234",
            "name": "A step",
            "userData": "{}"
        }
    }
}
"""


def step_reached():
    response = requests.post("http://localhost:8000/", STEP_REACHED)
    print(response.status_code)
    print(response.content)

locals()[sys.argv[1]]()
