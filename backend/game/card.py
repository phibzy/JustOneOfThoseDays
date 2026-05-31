"""
Class for representing cards in the game.
"""

from typing import Any


class Card:
    """
    Represents a single game card.

    Attributes:
        desc  - A description of the unfortunate scenario on said card
        value - The misery index value assigned to this card (float)
    """

    def __init__(self, desc: str, value: float) -> None:
        self.__desc = desc
        self.__value = value

    def __lt__(self, other_card: "Card") -> bool:
        return self.__value < other_card.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.__desc == other.desc and self.__value == other.value

    @property
    def desc(self) -> str:
        return self.__desc

    @property
    def value(self) -> float:
        return self.__value

    def to_dict(self, hide_value: bool = False) -> dict:
        """Return card data as a dictionary. Optionally hide the value."""
        result: dict = {"desc": self.desc}
        if not hide_value:
            result["value"] = self.value
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """Reconstruct a Card from a dictionary produced by to_dict."""
        return cls(data["desc"], data["value"])
