import os
from twilio.rest import Client


class TwilioNotifier:
    FROM_NUMBER = "+447723472295"

    def __init__(
        self,
        username: str = os.getenv("TWILIO_ACCOUNT_SID"),
        password: str = os.getenv("TWILIO_AUTH_TOKEN"),
        from_number: str = FROM_NUMBER,
    ):
        self._client = Client(username, password)
        self._from_number = from_number

    def notify(self, to_number: str, message: str):
        self._client.calls.create(
            twiml=f"<Response><Say>{message}</Say</Response>",
            to=self._normalise_phone_number(to_number),
            from_=self._from_number,
        )

    def _normalise_phone_number(self, phone_number: str):
        normalised = phone_number.strip()
        if not phone_number.startswith("+"):
            normalised = "+" + normalised
        return normalised