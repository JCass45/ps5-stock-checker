from dataclasses import dataclass
import calendar


@dataclass()
class CreditCard:
    number: str
    expiration_month: int
    expiration_year: int
    cvv: int

    def month_name(self):
        return calendar.month_name[self.expiration_month]