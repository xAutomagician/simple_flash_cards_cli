import csv
from datetime import date

from cards import Card, Deck


def load(filename: str) -> Deck:
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            cards = [
                Card(
                    id=row["id"],
                    question=row["question"],
                    answer=row["answer"],
                    interval_days=int(row["interval_days"]),
                    next_review=date.fromisoformat(row["next_review"]),
                )
                for row in reader
            ]

        return Deck(cards)

    except FileNotFoundError:
        return Deck()


def save(deck: Deck, filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "question",
                "answer",
                "interval_days",
                "next_review",
            ],
        )

        writer.writeheader()

        for card in deck.list():
            writer.writerow(card.to_dict())
