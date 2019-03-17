import typing
from collections import Counter, namedtuple, defaultdict, deque
from random import shuffle, choice

KEYWORD_TYPE: typing.Union = typing.Union[str, None]
ALLY = typing.DefaultDict[str, bool]
ALLEGIANCE = typing.DefaultDict[str, ALLY]


class MsgPacket(typing.NamedTuple):
    sender: str
    msg: str
    receiver: str


msgPacket: MsgPacket = namedtuple('MsgPacket', ['sender', 'msg', 'receiver'])

_KINGDOMS = {
    'LAND': 'panda',
    'WATER': 'octopus',
    'ICE': 'mammoth',
    'AIR': 'owl',
    'FIRE': 'dragon',
    'SPACE': 'gorilla',
}

_REVERSE_KINGDOMS = {
    emblem: kingdom for kingdom, emblem in _KINGDOMS.items()
}

_MESSAGES = [
    "Summer is coming",
    "a1d22n333a4444p",
    "oaaawaala",
    "zmzmzmzaztzozh",
    "Go, risk it all",
    "Let's swing the sword together",
    "Die or play the tame of thrones",
    "Ahoy! Fight for me with men and money",
    "Drag on Martin!",
    "When you play the tame of thrones, you win or you die.",
    "What could we say to the Lord of Death? Game on?",
    "Turn us away, and we will burn you first",
    "Death is so terribly final, while life is full of possibilities.",
    "You Win or You Die",
    "His watch is Ended",
    "Sphinx of black quartz, judge my dozen vows",
    "Fear cuts deeper than swords, My Lord.",
    "Different roads sometimes lead to the same castle.",
    "A DRAGON IS NOT A SLAVE.",
    "Do not waste paper",
    "Go ring all the bells",
    "Crazy Fredrick bought many very exquisite pearl, emerald and diamond jewels.",
    "The quick brown fox jumps over a lazy dog multiple times.",
    "We promptly judged antique ivory buckles for the next prize.",
    "Walar Morghulis: All men must die.",
]


class Ruler(object):
    __slots__ = ['_messages', 'ballot', '_ballot_picked', '_contenders', '_kingdoms', '_nominations', '_messages',
                 '_subject_kingdoms', '_msg_kingdom', 'allegiance_map', '_pledge_covered', '_rounds', 'winner_map']

    def __init__(self, contenders=None):
        self.ballot = deque([], maxlen=6)
        self._ballot_picked = set()
        self._contenders = [contender.upper() for contender in contenders] if contenders else []
        self._kingdoms = {}
        self._nominations = []
        self._messages = _MESSAGES  # read-only
        self._msg_kingdom = []
        self._pledge_covered = set()
        self.allegiance_map = defaultdict(list)
        self._subject_kingdoms = set()
        self._rounds = 0
        self.winner_map = Counter()

    def reset(self):
        self.ballot.clear()
        self._ballot_picked.clear()
        self._contenders.clear()
        self._kingdoms.clear()
        self._nominations.clear()
        self._msg_kingdom.clear()
        self._pledge_covered.clear()
        self.allegiance_map.clear()
        self._subject_kingdoms.clear()
        self.winner_map.clear()

    def _populate_kingdoms(self):
        self._kingdoms.update(_KINGDOMS)
        self._subject_kingdoms.update(set(self._kingdoms.keys()) - set(self._contenders))

    @staticmethod
    def _shuffle_choice(shuffle_list):
        shuffle(shuffle_list)
        return choice(shuffle_list)

    def add_contenders(self, contenders):
        self._contenders += contenders

    def _create_msgs(self):
        # totally random selection
        shuffle(self._contenders)
        for each_contender in self._contenders:
            for receiver in self._subject_kingdoms:
                for msg in self._messages:
                    self._msg_kingdom.append((each_contender, msg, receiver))

    def _begin_nomination(self):
        assert len(self._msg_kingdom)
        # totally random selection
        shuffle(self._msg_kingdom)
        [self.ballot.appendleft(create_msg_packet(each_contender, msg, receiver)) for each_contender, msg, receiver in self._msg_kingdom]

    def pick_nominations(self):
        self._begin_nomination()
        assert len(self.ballot)
        pick_times = min(6, len(self.ballot))
        [self._pick_one_random() for _ in range(pick_times)]
        assert len(self._ballot_picked)
        [self.ballot.appendleft(item) for item in self._ballot_picked]
        self._ballot_picked.clear()
        assert len(self._ballot_picked) == 0
        assert len(self.ballot)

    def _pick_one_random(self):
        if self.ballot:
            shuffle(self.ballot)
            pick = self.ballot.pop()
            self._ballot_picked.add(pick)
            self._nominations.append(pick)

    def tally_votes(self):
        """
        Rules to decide allegiance by a kingdom
            1.The receiving kingdom has to give allegiance to the sending kingdom if the message contains the letters of
            the animal in their emblem.
            2.If the receiving kingdom is competing to be the ruler, they will not give their allegiance even if the
            message they received is correct.
            3.  A kingdom cannot give their allegiance twice. If they have given their allegiance once,
            they will not give their allegiance again even if they get a second message and the message is correct.
        """
        for nomination in self._nominations:
            self._get_allegiance(nomination)

    def _get_allegiance(self, msg_packet: MsgPacket):
        sender = msg_packet.sender.upper()
        msg = msg_packet.msg.lower()
        receiver = msg_packet.receiver.upper()
        if receiver not in self._pledge_covered and self._is_valid_msg(sender, msg, receiver):
            self.allegiance_map[msg_packet.sender].append(receiver)
            self._pledge_covered.add(receiver)

    def _is_valid_msg(self, sender, msg, kingdom):
        return bool(extract_keyword(msg, kingdom)) and sender in self._contenders

    def _pre(self):
        self._populate_kingdoms()
        self._create_msgs()

    def _post(self):
        self.pick_nominations()
        self.tally_votes()

    def _run(self):
        self._pre()
        self._post()

    def get_winner(self):
        self._run()
        self.winner_map.update({king: len(self.allegiance_map[king]) for king in self.allegiance_map})
        winners = self.winner_map.most_common(2)
        if winners:
            self._rounds += 1
            #print(self.winner_map)
            self._print_results()
        # If there's a tie or no winners at all.
        while (len(winners) > 1 and winners[0][1] == winners[1][1]) or not winners:
            assert self._contenders
            assert self._msg_kingdom
            contenders = tuple([winners[0][0], winners[1][0]]) if winners else tuple(self._contenders)
            self.reset()
            self._rounds += 1
            assert self._rounds < 100
            assert contenders
            self.add_contenders(contenders)
            assert self._contenders
            self._run()
            assert self._msg_kingdom
            #print(self.allegiance_map)
            self.winner_map.update({king: len(self.allegiance_map[king]) for king in self.allegiance_map})
            winners = self.winner_map.most_common(2)
            self._print_results()

    def _print_results(self):
        print('Results after round {:d} ballot count'.format(self._rounds))
        for king in self._contenders:
            print('Allies for {:s} : {:d}'.format(king.capitalize(), self.winner_map[king]))

    @classmethod
    def declare_winner(cls, instance=None):
        winner = instance.winner_map.most_common()[0][0] if instance else None
        allies = ' '.join(sorted(instance.allegiance_map[winner])) if winner else None
        print('Who is the ruler of Southeros?\n{}'.format(winner))
        print('Allies of Ruler?\n{}'.format(allies))

    @classmethod
    def find_winner(cls):
        cls.declare_winner()
        contenders = input('Enter the kingdoms competing to be the ruler:\n').strip().split()
        instance = cls(contenders)
        instance.get_winner()
        cls.declare_winner(instance)


def extract_keyword(message: str, receiving_kingdom: str) -> KEYWORD_TYPE:
    msg_counts = Counter(message)
    emblem = _KINGDOMS.get(receiving_kingdom.upper(), '')
    emblem_counts = Counter(emblem)
    emblem_counts.subtract(msg_counts)
    return emblem if emblem and not any(emblem_counts.elements()) else None


def create_msg_packet(sender: str, msg: str, receiver: str) -> MsgPacket:
    return msgPacket(sender, msg, receiver)


if __name__ == '__main__':
    # ruler = Ruler(contenders=['Ice', 'Space', 'Air'])
    # # ruler = Ruler(contenders=['Ice', 'Space'])
    # # ruler = Ruler(contenders=['Ice'])
    # ruler._run()
    # # print(ruler._msg_kingdom)
    # # print(ruler.ballot)
    # # print(ruler._subject_kingdoms)
    # # print(ruler.allegiance_map)
    # ruler.get_winner()
    # ruler.declare_winner()
    Ruler.find_winner()
