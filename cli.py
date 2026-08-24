import argparse
import uuid
from datetime import date

from cards import Card, review
from storage import load, save


CSV_FILE = "cards.csv"


def add(args):
    deck = load(CSV_FILE)

    deck.add(
        Card(
            id=str(uuid.uuid4()),
            question=args.question,
            answer=args.answer,
        )
    )

    save(deck, CSV_FILE)


def list_cards(args):
    deck = load(CSV_FILE)

    for card in deck.list():
        print(f"{card.id} | {card.question} | повторить: {card.next_review}")


def delete(args):
    deck = load(CSV_FILE)

    if args.card_id not in deck:
        print("Карточка не найдена")
        return

    deck.delete(args.card_id)
    save(deck, CSV_FILE)


def train(args):
    deck = load(CSV_FILE)

    for card in deck.list():
        if card.next_review > date.today():
            continue

        print(card.question)
        input("Нажмите Enter, чтобы увидеть ответ")
        print(card.answer)

        answer = input("Удалось вспомнить? 1 — да, 2 — нет\n> ")
        review(card, remembered=answer.strip() == "1")

    save(deck, CSV_FILE)


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(required=True)

add_parser = subparsers.add_parser("add")
add_parser.add_argument("question")
add_parser.add_argument("answer")
add_parser.set_defaults(func=add)

list_parser = subparsers.add_parser("list")
list_parser.set_defaults(func=list_cards)

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("card_id")
delete_parser.set_defaults(func=delete)

train_parser = subparsers.add_parser("train")
train_parser.set_defaults(func=train)

args = parser.parse_args()
args.func(args)