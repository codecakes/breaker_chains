import typing
from collections import Counter

KEYWORD_TYPE: typing.Union = typing.Union[str, None]
_KINGDOMS = {
    'LAND': 'panda',
    'WATER': 'octopus',
    'ICE': 'mammoth',
    'AIR': 'owl',
    'FIRE': 'dragon',
    'SPACE': 'gorilla',
}


def run():
    pass


def extract_keyword(message: str, receiving_kingdom: str) -> KEYWORD_TYPE:
    msg_counts = Counter(message)
    emblem = _KINGDOMS.get(receiving_kingdom.upper(), '')
    assert emblem == 'panda'
    emblem_counts = Counter(emblem)
    emblem_counts.subtract(msg_counts)
    return emblem if not any(emblem_counts.elements()) else None
