from dataclasses import dataclass, field, asdict
from datetime import date, timedelta


@dataclass
class Card:
    id: str
    question: str
    answer: str
    interval_days: int = 1
    next_review: date = field(default_factory=date.today)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["next_review"] = self.next_review.isoformat()
        return data


class Deck:
    def __init__(self, cards: list[Card] | None = None):
        self.cards = cards or []

    def __contains__(self, card_id: str) -> bool:
        return any(card.id == card_id for card in self.cards)

    def __getitem__(self, card_id: str) -> Card:
        return next(card for card in self.cards if card.id == card_id)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def delete(self, card_id: str) -> Card:
        card = self[card_id]
        self.cards.remove(card)
        return card

    def list(self) -> list[Card]:
        return self.cards


def review(card: Card, remembered: bool) -> None:
    card.interval_days = card.interval_days * 2 if remembered else 1
    card.next_review = date.today() + timedelta(days=card.interval_days)