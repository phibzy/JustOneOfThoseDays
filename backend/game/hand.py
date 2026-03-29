"""
Abstraction of a player's hand.

Current implementation:
    - List of cards
    - List of ranges
"""

from typing import Any, List, Tuple

import bisect

from backend.game.card import Card


class Hand:
    """
    Manages a player's card collection and guess ranges.

    Attributes:
        cards      - List of cards
        ranges     - List of ranges (tuples) that can be used for guesses
        num_cards  - Number of cards in hand
        num_ranges - Number of guess ranges
    """

    def __init__(self) -> None:
        self.__boundaries: dict[float, int] = {0: 1, 100: 1}
        self.__cards: List[Card] = []
        self.__ranges: List[Tuple[float, float]] = [(0, 100)]
        self.__num_cards: int = 0
        self.__num_ranges: int = 1

    @property
    def boundaries(self) -> dict:
        return self.__boundaries

    @property
    def cards(self) -> List[Card]:
        return self.__cards

    @property
    def ranges(self) -> List[Tuple[float, float]]:
        return self.__ranges

    @property
    def num_cards(self) -> int:
        return self.__num_cards

    @property
    def num_ranges(self) -> int:
        return self.__num_ranges

    def card_index(self, index: int) -> Card:
        return self.__cards[index]

    def gain_card(self, new_card: Card) -> None:
        """Adds card to player's faceup cards if they guess correctly."""
        bisect.insort(self.__cards, new_card)

        if new_card.value not in self.__boundaries:
            if self.__num_ranges > 1:
                insert_index = (
                    bisect.bisect(
                        sorted(list(self.__boundaries.keys())), new_card.value
                    )
                    - 1
                )

                self.__ranges[insert_index] = (
                    new_card.value,
                    self.__ranges[insert_index][1],
                )

                if insert_index != 0:
                    self.__ranges.insert(
                        insert_index,
                        (self.__ranges[insert_index - 1][1], new_card.value),
                    )
                else:
                    self.__ranges.insert(0, (0, new_card.value))
            else:
                self.__ranges.append((new_card.value, self.__ranges[0][1]))
                self.__ranges[0] = (self.__ranges[0][0], new_card.value)

            self.__boundaries[new_card.value] = 1
            self.__num_ranges += 1

        self.__num_cards += 1

    def guessed_range(self, index: int) -> Tuple[float, float]:
        return self.__ranges[index]

    def get_cards_list(self) -> List[dict]:
        """Return cards as list of dicts."""
        return [{"desc": c.desc, "value": c.value} for c in self.__cards]

    def get_ranges_list(self) -> List[dict]:
        """Return ranges as list of dicts."""
        return [
            {"index": i + 1, "low": r[0], "high": r[1]}
            for i, r in enumerate(self.__ranges)
        ]

    def to_dict(self) -> dict:
        """Return hand data as a dictionary."""
        return {
            "cards": self.get_cards_list(),
            "ranges": self.get_ranges_list(),
            "num_cards": self.__num_cards,
            "num_ranges": self.__num_ranges,
        }
