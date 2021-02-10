import os

from twilio.rest import Client

from notifier.base_notifier import BaseNotifier


class TwilioNotifier(BaseNotifier):
    FROM_NUMBER = "+447723472295"

    def __init__(self):
        super().__init__()
        self._client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
        )

    def notify(self, message: str, recipient: str, sender: str = FROM_NUMBER):
        self._client.calls.create(
            twiml=f"<Response><Say>{message}</Say</Response>",
            to=self._normalise_phone_number(recipient),
            from_=sender,
        )

    def _normalise_phone_number(self, phone_number: str):
        normalised = phone_number.strip()
        if not phone_number.startswith("+"):
            normalised = "+" + normalised
        return normalised
