from typing import Optional, Callable

from chat.ChatMessage import ChatMessage
from games.mafia.logic.MafiaAction import ANSWERS_DICT
from properties import COMMAND_PREFIX
from utils.ArgsDevider import splitArgs
from utils.Utils import dictUpdate, T

# T => number_of_votes
VOTED_COUNT_DICT = dict[T, int]


def extractFirstArg(msg: ChatMessage) -> str:
    bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
    args = splitArgs(bodyWithoutPrefix)
    return args[0]


def countOnlyNotNoneAnswers(votes: ANSWERS_DICT, keyExtractor: Callable[[ChatMessage], T]) -> VOTED_COUNT_DICT:
    votedCount: VOTED_COUNT_DICT = {}

    for mafia in votes:
        vote: Optional[ChatMessage] = votes[mafia]
        if vote is None:
            continue
        votedFor: T = keyExtractor(vote)
        dictUpdate(votedCount, votedFor, lambda k, v: 1 if v is None else v + 1)

    return votedCount
