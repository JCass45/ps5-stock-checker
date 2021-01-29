import os
from pprint import pprint
from notifier.twilio_notifier import TwilioNotifier

notifier = TwilioNotifier()
notifier.notify(
    "353863454148",
)
