"""
Class that represents a player.
Keeps track of what/how many cards they have.
"""

from typing import Any

from backend.game.card import Card
from backend.game.hand import Hand


class Player:
    """
    Represents a game player.

    Attributes:
        hand - Hand of cards faceup on table
        name - the player's name (string)
    """

    def __init__(self, name: str, is_cpu: bool = False) -> None:
        self.__hand = Hand()
        self.__name = name
        self.__is_cpu = is_cpu

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other: "Player") -> bool:
        return self.name < other.name

    @property
    def hand(self) -> Hand:
        return self.__hand

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def is_cpu(self) -> bool:
        return self.__is_cpu

    @is_cpu.setter
    def is_cpu(self, value: bool) -> None:
        self.__is_cpu = value

    @property
    def num_cards(self) -> int:
        return self.__hand.num_cards

    @property
    def num_ranges(self) -> int:
        return self.__hand.num_ranges

    @property
    def ranges(self):
        return self.__hand.ranges

    def card_index(self, index: int) -> Card:
        return self.__hand.card_index(index)

    def gain_card(self, new_card: Card) -> None:
        self.__hand.gain_card(new_card)

    def guessed_range(self, index: int):
        return self.__hand.guessed_range(index)

    def to_dict(self, include_hand: bool = False) -> dict:
        """Return player data as a dictionary."""
        result: dict = {
            "name": self.name,
            "num_cards": self.num_cards,
            "is_cpu": self.is_cpu,
        }
        if include_hand:
            result["hand"] = self.hand.to_dict()
        return result

    def serialize(self) -> dict:
        """Return a fully persistable representation of the player."""
        return {
            "name": self.name,
            "is_cpu": self.is_cpu,
            "cards": [{"desc": c.desc, "value": c.value} for c in self.hand.cards],
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Player":
        """Reconstruct a Player from its serialized representation."""
        player = cls(data["name"], data.get("is_cpu", False))
        for card_data in data.get("cards", []):
            player.gain_card(Card(card_data["desc"], card_data["value"]))
        return player
